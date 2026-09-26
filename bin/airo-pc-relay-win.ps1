# bin/airo-pc-relay-win.ps1 — Native Windows PC Action Relay for AIRO Hermes
$ErrorActionPreference = "Continue"

$VPS_HOST = "43.157.241.228"
$VPS_USER = "ubuntu"
$SSH_KEY = "/home/egitaristorandas/.ssh/airo_tencent_vps.pem"
$POLL_INTERVAL = 1.5

$BRAVE_PATH = "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
$CHROME_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$EDGE_PATH = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

$STATE_DIR = "$env:USERPROFILE\.local\state\airo-second-brain\pc-action-bridge"
$LOG_FILE = "$STATE_DIR\relay-win.log"
$PID_FILE = "$STATE_DIR\relay-win.pid"

if (-not (Test-Path $STATE_DIR)) {
    New-Item -ItemType Directory -Path $STATE_DIR -Force | Out-Null
}

# Write PID
$PID | Out-File -FilePath $PID_FILE -Encoding ascii -Force

# Compile Win32 Desktop Launcher to explicitly target physical monitor (WinSta0\Default)
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WinDesktopLauncher {
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct STARTUPINFO {
        public Int32 cb;
        public string lpReserved;
        public string lpDesktop;
        public string lpTitle;
        public Int32 dwX;
        public Int32 dwY;
        public Int32 dwXSize;
        public Int32 dwYSize;
        public Int32 dwXCountChars;
        public Int32 dwYCountChars;
        public Int32 dwFillAttribute;
        public Int32 dwFlags;
        public Int16 wShowWindow;
        public Int16 cbReserved2;
        public IntPtr lpReserved2;
        public IntPtr hStdInput;
        public IntPtr hStdOutput;
        public IntPtr hStdError;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct PROCESS_INFORMATION {
        public IntPtr hProcess;
        public IntPtr hThread;
        public Int32 dwProcessId;
        public Int32 dwThreadId;
    }

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool CreateProcess(
        string lpApplicationName,
        string lpCommandLine,
        IntPtr lpProcessAttributes,
        IntPtr lpThreadAttributes,
        bool bInheritHandles,
        uint dwCreationFlags,
        IntPtr lpEnvironment,
        string lpCurrentDirectory,
        ref STARTUPINFO lpStartupInfo,
        out PROCESS_INFORMATION lpProcessInformation
    );

    public static int LaunchOnDesktop(string cmd) {
        STARTUPINFO si = new STARTUPINFO();
        si.cb = Marshal.SizeOf(si);
        si.lpDesktop = @"WinSta0\Default";
        PROCESS_INFORMATION pi = new PROCESS_INFORMATION();
        bool ok = CreateProcess(null, cmd, IntPtr.Zero, IntPtr.Zero, false, 0, IntPtr.Zero, null, ref si, out pi);
        return ok ? pi.dwProcessId : -1;
    }
}
"@

function Log-Message($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LOG_FILE -Value $line -Encoding UTF8
}

Log-Message "=================================================="
Log-Message "AIRO Native Windows PC Relay started (PID: $PID)"
Log-Message "Active desktop target: WinSta0\Default (Physical Monitor)"
Log-Message "=================================================="

$claimBashScript = @"
PENDING="`$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/pending"
IN_PROG="`$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress"
mkdir -p "`$PENDING" "`$IN_PROG"
for f in `$PENDING/*.json; do
  [ -f "`$f" ] || continue
  fname=`$(basename "`$f")
  mv "`$f" "`$IN_PROG/`$fname"
  cat "`$IN_PROG/`$fname"
  break
done
"@

while ($true) {
    try {
        # Claim oldest task atomically via WSL SSH
        $res = wsl.exe -e bash -c "ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 $VPS_USER@$VPS_HOST '$claimBashScript'" 2>$null
        $jsonStr = ($res -join "`n").Trim()

        if ($jsonStr -and $jsonStr.StartsWith("{") -and $jsonStr.EndsWith("}")) {
            $packet = $jsonStr | ConvertFrom-Json
            $actionId = $packet.action_id
            $type = $packet.type
            $payload = $packet.payload

            Log-Message "⚡ CLAIMED TASK: $actionId (type=$type)"

            if ($type -eq "open_url" -and $payload.url) {
                $targetUrl = $payload.url
                $title = if ($payload.title) { $payload.title } else { "No Title" }

                $browserCmd = ""
                if (Test-Path $BRAVE_PATH) {
                    $browserCmd = "`"$BRAVE_PATH`" `"$targetUrl`""
                } elseif (Test-Path $CHROME_PATH) {
                    $browserCmd = "`"$CHROME_PATH`" `"$targetUrl`""
                } elseif (Test-Path $EDGE_PATH) {
                    $browserCmd = "`"$EDGE_PATH`" `"$targetUrl`""
                } else {
                    $browserCmd = "cmd.exe /c start `"`" `"$targetUrl`""
                }

                $spawnedPid = [WinDesktopLauncher]::LaunchOnDesktop($browserCmd)
                Log-Message "🚀 EXECUTED open_url: '$title' -> $targetUrl (PID: $spawnedPid)"

                # Mark done on VPS
                $markDoneScript = @"
IN_PROG="`$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/$actionId.json"
DONE="`$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/done/$actionId.json"
mkdir -p "`$HOME/.local/state/airo-second-brain/pc-action-bridge/queue/done"
if [ -f "`$IN_PROG" ]; then
  mv "`$IN_PROG" "`$DONE"
fi
"@
                wsl.exe -e bash -c "ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 $VPS_USER@$VPS_HOST '$markDoneScript'" 2>$null
                Log-Message "✅ TASK COMPLETED: $actionId"
            }
        }
    } catch {
        Log-Message "Polling error: $_"
    }

    Start-Sleep -Seconds $POLL_INTERVAL
}

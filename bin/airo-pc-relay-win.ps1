# bin/airo-pc-relay-win.ps1 — Native Windows PC Computer Use & Desktop Relay for AIRO Hermes
# Architecture: Zero-dependency .NET / Win32 API Engine (PowerShell Host)
$ErrorActionPreference = "Continue"

$VPS_HOST = "43.157.241.228"
$VPS_USER = "ubuntu"
$SSH_KEY = "/home/egitaristorandas/.ssh/airo_tencent_vps.pem"
$POLL_INTERVAL = 1.5

$BRAVE_PATH = "C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
$CHROME_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$EDGE_PATH = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

$STATE_DIR = "$env:USERPROFILE\.local\state\airo-second-brain\pc-action-bridge"
$SCREEN_DIR = "$STATE_DIR\screenshots"
$LOG_FILE = "$STATE_DIR\relay-win.log"
$PID_FILE = "$STATE_DIR\relay-win.pid"
$TG_ENV_FILE = "$STATE_DIR\telegram.env"

if (-not (Test-Path $STATE_DIR)) {
    New-Item -ItemType Directory -Path $STATE_DIR -Force | Out-Null
}
if (-not (Test-Path $SCREEN_DIR)) {
    New-Item -ItemType Directory -Path $SCREEN_DIR -Force | Out-Null
}

# Write PID
$PID | Out-File -FilePath $PID_FILE -Encoding ascii -Force

# Load Telegram credentials for direct screenshot uploads
if (-not (Test-Path $TG_ENV_FILE)) {
    try {
        $wslEnv = wsl.exe -e bash -c "cat ~/.config/airo/airo-hermes-telegram.env 2>/dev/null"
        if ($wslEnv) {
            $wslEnv | Out-File -FilePath $TG_ENV_FILE -Encoding utf8 -Force
        }
    } catch {}
}

$BOT_TOKEN = $env:AIRO_HERMES_TELEGRAM_BOT_TOKEN
$OWNER_CHAT_ID = $env:OWNER_TELEGRAM_ID
if (Test-Path $TG_ENV_FILE) {
    Get-Content $TG_ENV_FILE | ForEach-Object {
        if ($_ -match '^\s*([^#=]+)=(.*)$') {
            $k = $matches[1].Trim()
            $v = $matches[2].Trim('"', "'", " ")
            if ($k -eq "AIRO_HERMES_TELEGRAM_BOT_TOKEN" -and -not $BOT_TOKEN) { $BOT_TOKEN = $v }
            if ($k -eq "OWNER_TELEGRAM_ID" -and -not $OWNER_CHAT_ID) { $OWNER_CHAT_ID = $v }
        }
    }
}
if (-not $BOT_TOKEN) {
    try {
        $secEnv = wsl.exe -e bash -c 'grep -E "^AIRO_HERMES_TELEGRAM_BOT_TOKEN=" ~/.config/airo/airo-hermes-telegram.env 2>/dev/null | cut -d= -f2-'
        $BOT_TOKEN = ($secEnv -join "").Trim('"', "'", " ")
    } catch {}
}
if (-not $OWNER_CHAT_ID) {
    try {
        $secChat = wsl.exe -e bash -c 'grep -E "^OWNER_TELEGRAM_ID=" ~/.config/airo/airo-hermes-telegram.env 2>/dev/null | cut -d= -f2-'
        $OWNER_CHAT_ID = ($secChat -join "").Trim('"', "'", " ")
    } catch {}
}

# Add .NET Assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Compile Win32 Desktop Launcher & Native Actuators
Add-Type -ReferencedAssemblies "System.Drawing" @"
using System;
using System.Drawing;
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

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool SetCursorPos(int X, int Y);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool LockWorkStation();

    [DllImport("user32.dll")]
    public static extern IntPtr GetDesktopWindow();

    [DllImport("user32.dll")]
    public static extern IntPtr GetWindowDC(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern IntPtr ReleaseDC(IntPtr hWnd, IntPtr hDC);

    [DllImport("gdi32.dll")]
    public static extern bool BitBlt(IntPtr hObject, int nXDest, int nYDest, int nWidth, int nHeight, IntPtr hObjectSource, int nXSrc, int nYSrc, int dwRop);

    [DllImport("gdi32.dll")]
    public static extern IntPtr CreateCompatibleBitmap(IntPtr hDC, int nWidth, int nHeight);

    [DllImport("gdi32.dll")]
    public static extern IntPtr CreateCompatibleDC(IntPtr hDC);

    [DllImport("gdi32.dll")]
    public static extern bool DeleteDC(IntPtr hDC);

    [DllImport("gdi32.dll")]
    public static extern bool DeleteObject(IntPtr hObject);

    [DllImport("gdi32.dll")]
    public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);

    [DllImport("user32.dll")]
    public static extern int GetSystemMetrics(int nIndex);

    public const int SRCCOPY = 0x00CC0020;
    public const uint MOUSEEVENTF_LEFTDOWN   = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP     = 0x0004;
    public const uint MOUSEEVENTF_RIGHTDOWN  = 0x0008;
    public const uint MOUSEEVENTF_RIGHTUP    = 0x0010;
    public const uint MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    public const uint MOUSEEVENTF_MIDDLEUP   = 0x0040;

    public static int LaunchOnDesktop(string cmd) {
        STARTUPINFO si = new STARTUPINFO();
        si.cb = Marshal.SizeOf(si);
        si.lpDesktop = @"WinSta0\Default";
        PROCESS_INFORMATION pi = new PROCESS_INFORMATION();
        bool ok = CreateProcess(null, cmd, IntPtr.Zero, IntPtr.Zero, false, 0, IntPtr.Zero, null, ref si, out pi);
        return ok ? pi.dwProcessId : -1;
    }

    public static Bitmap CaptureDesktop() {
        int x = GetSystemMetrics(76); // SM_XVIRTUALSCREEN
        int y = GetSystemMetrics(77); // SM_YVIRTUALSCREEN
        int width = GetSystemMetrics(78); // SM_CXVIRTUALSCREEN
        int height = GetSystemMetrics(79); // SM_CYVIRTUALSCREEN
        if (width <= 0 || height <= 0) {
            x = 0; y = 0;
            width = GetSystemMetrics(0); // SM_CXSCREEN
            height = GetSystemMetrics(1); // SM_CYSCREEN
        }

        IntPtr deskWnd = GetDesktopWindow();
        IntPtr deskDC = GetWindowDC(deskWnd);
        IntPtr memDC = CreateCompatibleDC(deskDC);
        IntPtr memBmp = CreateCompatibleBitmap(deskDC, width, height);
        IntPtr oldBmp = SelectObject(memDC, memBmp);

        BitBlt(memDC, 0, 0, width, height, deskDC, x, y, SRCCOPY);

        SelectObject(memDC, oldBmp);
        DeleteDC(memDC);
        ReleaseDC(deskWnd, deskDC);

        Bitmap bmp = Image.FromHbitmap(memBmp);
        DeleteObject(memBmp);
        return bmp;
    }
}
"@

function Log-Message($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    Write-Host $line
    Add-Content -Path $LOG_FILE -Value $line -Encoding UTF8
}

function Send-SpecialHotkey($keys) {
    $k = $keys.ToLower().Trim()
    if ($k -eq "win+d" -or $k -eq "super+d") {
        (New-Object -ComObject Shell.Application).ToggleDesktop()
        return
    }
    $map = @{
        "ctrl+s"    = "^s"
        "ctrl+c"    = "^c"
        "ctrl+v"    = "^v"
        "ctrl+a"    = "^a"
        "ctrl+z"    = "^z"
        "ctrl+y"    = "^y"
        "ctrl+w"    = "^w"
        "ctrl+f"    = "^f"
        "ctrl+p"    = "^p"
        "alt+f4"    = "%{F4}"
        "alt+tab"   = "%{TAB}"
        "enter"     = "{ENTER}"
        "esc"       = "{ESC}"
        "escape"    = "{ESC}"
        "tab"       = "{TAB}"
        "space"     = " "
        "backspace" = "{BACKSPACE}"
        "delete"    = "{DELETE}"
        "up"        = "{UP}"
        "down"      = "{DOWN}"
        "left"      = "{LEFT}"
        "right"     = "{RIGHT}"
    }
    $wsh = New-Object -ComObject WScript.Shell
    if ($map.ContainsKey($k)) {
        $wsh.SendKeys($map[$k])
    } else {
        $wsh.SendKeys($keys)
    }
}

Log-Message "=================================================="
Log-Message "AIRO Native Windows PC Computer Use Relay started (PID: $PID)"
Log-Message "Active desktop target: WinSta0\Default (Physical Monitor)"
Log-Message "Actuators: App, Browser, Keyboard, Mouse, Screenshot, Audio, Lock"
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

            # ─── 1. OPEN_URL (Browser / YouTube) ───────────────────────────
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

            # ─── 2. OPEN_APP (Native Desktop Software) ────────────────────
            } elseif ($type -eq "open_app") {
                $appKey = ($payload.app).ToLower().Trim()
                $displayName = if ($payload.display_name) { $payload.display_name } else { $appKey }
                $appArgs = if ($payload.args) { " " + $payload.args } else { "" }

                $appCmd = ""
                switch ($appKey) {
                    "powerpoint" {
                        $p = "C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE"
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "powerpnt.exe$appArgs" }
                    }
                    "excel" {
                        $p = "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "excel.exe$appArgs" }
                    }
                    "word" {
                        $p = "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "winword.exe$appArgs" }
                    }
                    "spotify" {
                        $p = "$env:LOCALAPPDATA\Microsoft\WindowsApps\Spotify.exe"
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "spotify.exe$appArgs" }
                    }
                    "vscode" {
                        $p = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe"
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "code$appArgs" }
                    }
                    "notepad"    { $appCmd = "notepad.exe$appArgs" }
                    "calc"       { $appCmd = "calc.exe" }
                    "chrome"     { $appCmd = if (Test-Path $CHROME_PATH) { "`"$CHROME_PATH`"$appArgs" } else { "chrome.exe$appArgs" } }
                    "brave"      { $appCmd = if (Test-Path $BRAVE_PATH) { "`"$BRAVE_PATH`"$appArgs" } else { "brave.exe$appArgs" } }
                    "edge"       { $appCmd = if (Test-Path $EDGE_PATH) { "`"$EDGE_PATH`"$appArgs" } else { "msedge.exe$appArgs" } }
                    "explorer"   { $appCmd = "explorer.exe$appArgs" }
                    "terminal"   { $appCmd = "wt.exe$appArgs" }
                    default      { $appCmd = "$appKey$appArgs" }
                }

                $spawnedPid = [WinDesktopLauncher]::LaunchOnDesktop($appCmd)
                if ($spawnedPid -le 0) {
                    try {
                        Start-Process $appCmd
                        Log-Message "🚀 EXECUTED open_app: '$displayName' via Start-Process $appCmd"
                    } catch {
                        cmd.exe /c start "" $appCmd
                        Log-Message "🚀 EXECUTED open_app: '$displayName' via cmd start $appCmd"
                    }
                } else {
                    Log-Message "🚀 EXECUTED open_app: '$displayName' via $appCmd (PID: $spawnedPid)"
                }

            # ─── 3. TYPE_TEXT (Keyboard Actuator) ──────────────────────────
            } elseif ($type -eq "type_text") {
                $rawText = [string]$payload.text
                if ($rawText) {
                    $escaped = ""
                    for ($i = 0; $i -lt $rawText.Length; $i++) {
                        $ch = $rawText[$i]
                        if ($ch -in @('+', '^', '%', '~', '(', ')', '{', '}', '[', ']')) {
                            $escaped += "{$ch}"
                        } else {
                            $escaped += $ch
                        }
                    }
                    $wsh = New-Object -ComObject WScript.Shell
                    $wsh.SendKeys($escaped)
                    Log-Message "⌨️ EXECUTED type_text: '$rawText'"
                }

            # ─── 4. SEND_HOTKEY (Keyboard Shortcut Actuator) ───────────────
            } elseif ($type -eq "send_hotkey") {
                $hotkeys = [string]$payload.keys
                if ($hotkeys) {
                    Send-SpecialHotkey $hotkeys
                    Log-Message "⌨️ EXECUTED send_hotkey: '$hotkeys'"
                }

            # ─── 5. MOUSE_CLICK & MOUSE_MOVE (Mouse Actuator) ──────────────
            } elseif ($type -eq "mouse_click" -or $type -eq "mouse_move") {
                if ($null -ne $payload.x -and $null -ne $payload.y) {
                    [WinDesktopLauncher]::SetCursorPos([int]$payload.x, [int]$payload.y)
                }

                if ($type -eq "mouse_click") {
                    $btn = if ($payload.button) { ($payload.button).ToLower() } else { "left" }
                    $isDbl = if ($payload.double_click) { $true } else { $false }

                    $downFlag = [WinDesktopLauncher]::MOUSEEVENTF_LEFTDOWN
                    $upFlag = [WinDesktopLauncher]::MOUSEEVENTF_LEFTUP
                    if ($btn -eq "right") {
                        $downFlag = [WinDesktopLauncher]::MOUSEEVENTF_RIGHTDOWN
                        $upFlag = [WinDesktopLauncher]::MOUSEEVENTF_RIGHTUP
                    } elseif ($btn -eq "middle") {
                        $downFlag = [WinDesktopLauncher]::MOUSEEVENTF_MIDDLEDOWN
                        $upFlag = [WinDesktopLauncher]::MOUSEEVENTF_MIDDLEUP
                    }

                    [WinDesktopLauncher]::mouse_event($downFlag, 0, 0, 0, [UIntPtr]::Zero)
                    [WinDesktopLauncher]::mouse_event($upFlag, 0, 0, 0, [UIntPtr]::Zero)

                    if ($isDbl) {
                        Start-Sleep -Milliseconds 120
                        [WinDesktopLauncher]::mouse_event($downFlag, 0, 0, 0, [UIntPtr]::Zero)
                        [WinDesktopLauncher]::mouse_event($upFlag, 0, 0, 0, [UIntPtr]::Zero)
                    }

                    Log-Message "🖱️ EXECUTED mouse_click: button=$btn (double=$isDbl)"
                } else {
                    Log-Message "🖱️ EXECUTED mouse_move to ($($payload.x),$($payload.y))"
                }

            # ─── 6. CAPTURE_SCREENSHOT (Visual Perception Actuator) ────────
            } elseif ($type -eq "capture_screenshot") {
                $ts = Get-Date -Format "yyyyMMdd_HHmmss"
                $imgPath = "$SCREEN_DIR\screen_$ts.jpg"

                $bmp = [WinDesktopLauncher]::CaptureDesktop()
                $bmp.Save($imgPath, [System.Drawing.Imaging.ImageFormat]::Jpeg)
                $bmp.Dispose()
                Log-Message "📸 EXECUTED capture_screenshot: saved to $imgPath"

                $sendTg = if ($null -ne $payload.send_to_telegram) { [bool]$payload.send_to_telegram } else { $true }
                $targetChatId = if ($payload.chat_id) { $payload.chat_id } else { $OWNER_CHAT_ID }

                if ($sendTg -and $BOT_TOKEN -and $targetChatId) {
                    $timeStr = (Get-Date).ToString("HH:mm:ss")
                    $caption = "📸 Tangkapan layar PC Owner ($timeStr)"
                    curl.exe -s -F "chat_id=$targetChatId" -F "caption=$caption" -F "photo=@$imgPath" "https://api.telegram.org/bot$BOT_TOKEN/sendPhoto" | Out-Null
                    Log-Message "📤 Screenshot uploaded directly to Telegram chat $targetChatId"
                }

            # ─── 7. SYSTEM_CONTROL (OS Control Actuator) ───────────────────
            } elseif ($type -eq "system_control") {
                $cmd = ($payload.command).ToLower().Trim()
                $wsh = New-Object -ComObject WScript.Shell
                switch ($cmd) {
                    "lock" {
                        [WinDesktopLauncher]::LockWorkStation()
                        Log-Message "🔒 EXECUTED system_control: LockWorkStation"
                    }
                    "mute" {
                        $wsh.SendKeys([string][char]173)
                        Log-Message "🔇 EXECUTED system_control: Toggle Mute"
                    }
                    "volume_up" {
                        $wsh.SendKeys([string][char]175)
                        Log-Message "🔊 EXECUTED system_control: Volume Up"
                    }
                    "volume_down" {
                        $wsh.SendKeys([string][char]174)
                        Log-Message "🔉 EXECUTED system_control: Volume Down"
                    }
                    default {
                        Log-Message "⚠️ Unknown system_control command: $cmd"
                    }
                }
            }

            $doneCmd = "mv ~/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/$actionId.json ~/.local/state/airo-second-brain/pc-action-bridge/queue/done/$actionId.json"
            wsl.exe -e ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 "$VPS_USER@$VPS_HOST" $doneCmd 2>$null
            Log-Message "✅ TASK COMPLETED: $actionId"
        }
    } catch {
        Log-Message "Polling error: $_"
    }

    Start-Sleep -Seconds $POLL_INTERVAL
}

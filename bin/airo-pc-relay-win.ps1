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

            # Expiration Check (15 minutes = 900 seconds)
            $isExpired = $false
            $taskEpoch = 0
            if ($packet.created_at_epoch) {
                $taskEpoch = [int64]$packet.created_at_epoch
            } elseif ($actionId -match '^act-(\d+)-') {
                $taskEpoch = [int64]$matches[1]
            } elseif ($packet.created_at) {
                try {
                    $taskEpoch = [DateTimeOffset]::Parse($packet.created_at).ToUnixTimeSeconds()
                } catch {}
            }

            if ($taskEpoch -gt 0) {
                $nowEpoch = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
                $ageSec = $nowEpoch - $taskEpoch
                if ($ageSec -gt 900) {
                    $isExpired = $true
                    Log-Message "⏳ TASK EXPIRED ($ageSec s old > 900s limit): $actionId. Skipping execution."
                    $expireCmd = "mkdir -p ~/.local/state/airo-second-brain/pc-action-bridge/queue/dead && mv ~/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/$actionId.json ~/.local/state/airo-second-brain/pc-action-bridge/queue/dead/$actionId.json"
                    wsl.exe -e ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 "$VPS_USER@$VPS_HOST" $expireCmd 2>$null
                    continue
                }
            }

            try {

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
                        # Auto-sync presentation file from VPS if specified in args and missing locally
                        if ($appArgs -like "*.pptx*") {
                            $targetPptx = $appArgs.Trim('"', "'", " ")
                            if (-not (Test-Path $targetPptx)) {
                                $targetDir = Split-Path $targetPptx -Parent
                                if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }
                                $leafName = Split-Path $targetPptx -Leaf
                                $vpsPptxPath = "~/.local/state/airo-second-brain/pc-action-bridge/files/$leafName"
                                Log-Message "📥 Syncing presentation from VPS: $vpsPptxPath -> $targetPptx"
                                $wslDest = wsl.exe -e wslpath -u "$targetPptx"
                                $scpRemote = "$($VPS_USER)@$($VPS_HOST):$vpsPptxPath"
                                wsl.exe -e scp -i $SSH_KEY -o StrictHostKeyChecking=no "$scpRemote" "$wslDest" 2>$null
                            }
                        }
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "powerpnt.exe$appArgs" }
                    }
                    "excel" {
                        $p = "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"
                        # Auto-sync spreadsheet file from VPS if specified in args and missing locally
                        if ($appArgs -like "*.xlsx*") {
                            $targetXlsx = $appArgs.Trim('"', "'", " ")
                            if (-not (Test-Path $targetXlsx)) {
                                $targetDir = Split-Path $targetXlsx -Parent
                                if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }
                                $leafName = Split-Path $targetXlsx -Leaf
                                $vpsXlsxPath = "~/.local/state/airo-second-brain/pc-action-bridge/files/$leafName"
                                Log-Message "📥 Syncing spreadsheet from VPS: $vpsXlsxPath -> $targetXlsx"
                                $wslDest = wsl.exe -e wslpath -u "$targetXlsx"
                                $scpRemote = "$($VPS_USER)@$($VPS_HOST):$vpsXlsxPath"
                                wsl.exe -e scp -i $SSH_KEY -o StrictHostKeyChecking=no "$scpRemote" "$wslDest" 2>$null
                            }
                        }
                        $appCmd = if (Test-Path $p) { "`"$p`"$appArgs" } else { "excel.exe$appArgs" }
                    }
                    "word" {
                        $p = "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"
                        # Auto-sync document file from VPS if specified in args and missing locally
                        if ($appArgs -like "*.docx*") {
                            $targetDocx = $appArgs.Trim('"', "'", " ")
                            if (-not (Test-Path $targetDocx)) {
                                $targetDir = Split-Path $targetDocx -Parent
                                if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir -Force | Out-Null }
                                $leafName = Split-Path $targetDocx -Leaf
                                $vpsDocxPath = "~/.local/state/airo-second-brain/pc-action-bridge/files/$leafName"
                                Log-Message "📥 Syncing document from VPS: $vpsDocxPath -> $targetDocx"
                                $wslDest = wsl.exe -e wslpath -u "$targetDocx"
                                $scpRemote = "$($VPS_USER)@$($VPS_HOST):$vpsDocxPath"
                                wsl.exe -e scp -i $SSH_KEY -o StrictHostKeyChecking=no "$scpRemote" "$wslDest" 2>$null
                            }
                        }
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

            # ─── 8. LIVE_PPT_BUILD (Live On-Screen PowerPoint COM Actuator) ──
            } elseif ($type -eq "live_ppt_build") {
                Log-Message "🖥️ Starting LIVE On-Screen PowerPoint build..."
                $ppt = New-Object -ComObject PowerPoint.Application
                $ppt.Visible = -1 # msoTrue
                $ppt.WindowState = 3 # ppWindowMaximized
                $pres = $ppt.Presentations.Add(-1)

                try {
                    $ppt.Activate()
                } catch {}

                $slides = $payload.slides
                $slideIdx = 1
                foreach ($s in $slides) {
                    $layout = if ($slideIdx -eq 1) { 1 } else { 2 } # 1=Title, 2=Text
                    $slide = $pres.Slides.Add($slideIdx, $layout)

                    $slideTitle = [string]$s.title
                    if ($slideTitle) {
                        $slide.Shapes.Title.TextFrame.TextRange.Text = $slideTitle
                    }
                    Start-Sleep -Milliseconds 800

                    if ($slideIdx -eq 1) {
                        $subtitle = if ($s.subtitle) { [string]$s.subtitle } else { "AIRO Hermes Live Presentation" }
                        if ($slide.Shapes.Count -ge 2) {
                            $slide.Shapes.Item(2).TextFrame.TextRange.Text = $subtitle
                        }
                        Start-Sleep -Milliseconds 1000
                    } else {
                        $points = $s.points
                        if ($points -and $slide.Shapes.Count -ge 2) {
                            $bodyText = ($points -join [Environment]::NewLine)
                            $slide.Shapes.Item(2).TextFrame.TextRange.Text = $bodyText
                        }
                        Start-Sleep -Milliseconds 1200
                    }
                    $slideIdx++
                }

                try {
                    $pres.Windows.Item(1).Activate()
                } catch {}

                Log-Message "✅ LIVE PowerPoint build complete on screen ($($slides.Count) slides)!"

            # ─── 9. LIVE_EXCEL_BUILD (Live On-Screen Excel COM Actuator) ─────
            } elseif ($type -eq "live_excel_build") {
                Log-Message "🖥️ Starting LIVE On-Screen Excel build..."
                $excel = New-Object -ComObject Excel.Application
                $excel.Visible = $true
                $excel.WindowState = -4137 # xlMaximized
                $wb = $excel.Workbooks.Add()
                $ws = $wb.Sheets.Item(1)

                try {
                    $excel.ActiveWindow.Activate()
                } catch {}

                $title = if ($payload.title) { [string]$payload.title } else { "AIRO Live Spreadsheet" }
                $sheetName = if ($payload.sheet_name) { [string]$payload.sheet_name } else { "Executive Summary" }
                try {
                    $ws.Name = $sheetName.Substring(0, [Math]::Min(31, $sheetName.Length))
                } catch {}

                # 1. Title Banner
                $titleCell = $ws.Cells.Item(1, 1)
                $titleCell.Value2 = $title
                $titleCell.Font.Name = "Segoe UI"
                $titleCell.Font.Size = 14
                $titleCell.Font.Bold = $true
                $titleCell.Font.Color = 3154966 # Navy (#161E30)

                $subCell = $ws.Cells.Item(2, 1)
                $subCell.Value2 = "Disusun secara otomatis oleh AIRO Hermes Autonomous Operating System"
                $subCell.Font.Name = "Segoe UI"
                $subCell.Font.Size = 9
                $subCell.Font.Italic = $true
                $subCell.Font.Color = 8421504 # Gray

                Start-Sleep -Milliseconds 600

                $headers = $payload.headers
                $rows = $payload.rows
                $startRow = 4

                # 2. Render Headers with Navy Fill & White Font
                for ($col = 0; $col -lt $headers.Count; $col++) {
                    $cell = $ws.Cells.Item($startRow, $col + 1)
                    $cell.Value2 = [string]$headers[$col]
                    $cell.Font.Name = "Segoe UI"
                    $cell.Font.Size = 11
                    $cell.Font.Bold = $true
                    $cell.Font.Color = 16777215 # White
                    $cell.Interior.Color = 3154966 # Dark Navy (#161E30)
                    $cell.HorizontalAlignment = -4108 # xlCenter
                    $cell.VerticalAlignment = -4108 # xlCenter
                    Start-Sleep -Milliseconds 150
                }

                # 3. Render Data Rows with visual pacing and zebra striping
                $currentRow = $startRow + 1
                for ($r = 0; $r -lt $rows.Count; $r++) {
                    $rowData = $rows[$r]
                    $isEven = ($r % 2 -eq 1)
                    $fillColor = if ($isEven) { 16579832 } else { 16777215 } # #F8FAFC vs White

                    for ($c = 0; $c -lt $headers.Count; $c++) {
                        $val = if ($c -lt $rowData.Count) { $rowData[$c] } else { "" }
                        $cell = $ws.Cells.Item($currentRow, $c + 1)
                        $cell.Value2 = [string]$val
                        $cell.Font.Name = "Segoe UI"
                        $cell.Font.Size = 10
                        $cell.Interior.Color = $fillColor
                        
                        # Number alignment
                        if ($val -match '^[\d,.]+$') {
                            $cell.HorizontalAlignment = -4152 # xlRight
                        } else {
                            $cell.HorizontalAlignment = -4131 # xlLeft
                        }
                    }
                    $currentRow++
                    Start-Sleep -Milliseconds 350
                }

                # 4. Auto-fit columns
                $ws.Columns.AutoFit() | Out-Null

                Log-Message "✅ LIVE Excel build complete on screen ($($rows.Count) rows)!"

            # ─── 10. LIVE_WORD_BUILD (Live On-Screen Word COM Actuator) ──────
            } elseif ($type -eq "live_word_build") {
                Log-Message "🖥️ Starting LIVE On-Screen Word build..."
                $word = New-Object -ComObject Word.Application
                $word.Visible = $true
                $word.WindowState = 1 # wdWindowStateMaximize
                $doc = $word.Documents.Add()

                try {
                    $word.Activate()
                } catch {}

                $sel = $word.Selection

                # Title
                $title = if ($payload.title) { [string]$payload.title } else { "Dokumen Eksekutif AIRO" }
                $sel.Font.Name = "Segoe UI"
                $sel.Font.Size = 22
                $sel.Font.Bold = 1
                $sel.Font.Color = 3154966 # Dark Navy
                $sel.TypeText($title)
                $sel.TypeParagraph()
                Start-Sleep -Milliseconds 600

                # Subtitle
                if ($payload.subtitle) {
                    $sel.Font.Size = 12
                    $sel.Font.Bold = 0
                    $sel.Font.Italic = 1
                    $sel.Font.Color = 8421504 # Gray
                    $sel.TypeText([string]$payload.subtitle)
                    $sel.TypeParagraph()
                }

                # Metadata
                $sel.Font.Size = 9
                $sel.Font.Bold = 0
                $sel.Font.Italic = 1
                $sel.Font.Color = 8421504
                $sel.TypeText("Created by AIRO Hermes | Executive OS • 2026")
                $sel.TypeParagraph()
                $sel.TypeParagraph()
                Start-Sleep -Milliseconds 500

                # Sections
                $sections = $payload.sections
                $secIdx = 1
                foreach ($sec in $sections) {
                    $secTitle = if ($sec.title) { [string]$sec.title } else { "Bagian $secIdx" }
                    
                    # Section Heading
                    $sel.Font.Size = 14
                    $sel.Font.Bold = 1
                    $sel.Font.Italic = 0
                    $sel.Font.Color = 3154966
                    $sel.TypeText("$secIdx. $secTitle")
                    $sel.TypeParagraph()
                    Start-Sleep -Milliseconds 400

                    # Content paragraph
                    if ($sec.content) {
                        $sel.Font.Size = 11
                        $sel.Font.Bold = 0
                        $sel.Font.Color = 0 # Black
                        $sel.TypeText([string]$sec.content)
                        $sel.TypeParagraph()
                        Start-Sleep -Milliseconds 500
                    }

                    # Bullet points
                    if ($sec.points) {
                        foreach ($pt in $sec.points) {
                            $sel.Font.Size = 10.5
                            $sel.Font.Bold = 0
                            $sel.Font.Color = 3355443
                            $sel.TypeText("•  $pt")
                            $sel.TypeParagraph()
                            Start-Sleep -Milliseconds 250
                        }
                    }

                    $sel.TypeParagraph()
                    $secIdx++
                }

                Log-Message "✅ LIVE Word build complete on screen ($($sections.Count) sections)!"
            }

            $doneCmd = "mv ~/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/$actionId.json ~/.local/state/airo-second-brain/pc-action-bridge/queue/done/$actionId.json"
            wsl.exe -e ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 "$VPS_USER@$VPS_HOST" $doneCmd 2>$null
            Log-Message "✅ TASK COMPLETED: $actionId"
            } catch {
                $errMsg = $_.Exception.Message
                Log-Message "❌ EXECUTION FAILED for $actionId : $errMsg"
                if ($BOT_TOKEN -and $OWNER_CHAT_ID) {
                    $alertText = [System.Uri]::EscapeDataString("⚠️ [AIRO PC Relay] Gagal menjalankan aksi ($type): $errMsg")
                    curl.exe -s "https://api.telegram.org/bot$BOT_TOKEN/sendMessage?chat_id=$OWNER_CHAT_ID&text=$alertText" | Out-Null
                }
                $failCmd = "mkdir -p ~/.local/state/airo-second-brain/pc-action-bridge/queue/dead && mv ~/.local/state/airo-second-brain/pc-action-bridge/queue/in_progress/$actionId.json ~/.local/state/airo-second-brain/pc-action-bridge/queue/dead/$actionId.json"
                wsl.exe -e ssh -i $SSH_KEY -o StrictHostKeyChecking=no -o ConnectTimeout=6 "$VPS_USER@$VPS_HOST" $failCmd 2>$null
            }
        }
    } catch {
        Log-Message "Polling error: $_"
    }

    Start-Sleep -Seconds $POLL_INTERVAL
}

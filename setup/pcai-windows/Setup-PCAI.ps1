$ErrorActionPreference = 'Stop'
$secure = $null
$plain = $null
$guard = $null
$temporary = $null
function Put-File($path, [byte[]]$bytes) {
    if ((Test-Path -LiteralPath $path) -and ([Convert]::ToBase64String([IO.File]::ReadAllBytes($path)) -eq [Convert]::ToBase64String($bytes))) { return }
    $script:temporary = $path + '.' + [guid]::NewGuid().ToString('N') + '.tmp'
    [IO.File]::WriteAllBytes($script:temporary, $bytes)
    Move-Item -LiteralPath $script:temporary -Destination $path -Force
    $script:temporary = $null
}
try {
    Write-Host 'PCAI DeepSeek setup for OpenCode'
    Write-Host 'Connect your PCAI VPN before opening OpenCode.'
    $package = $env:PCAI_PACKAGE_DIR
    $ca = Join-Path $package 'pcai-ai-essentials-ca.crt'
    $template = Join-Path $package 'pcai-settings.json'
    $launchSource = Join-Path $package 'OpenCode-PCAI.cmd'
    if (!(Test-Path -LiteralPath $ca) -or !(Test-Path -LiteralPath $template) -or !(Test-Path -LiteralPath $launchSource)) { throw 'Extract the whole ZIP first, then run Setup PCAI.cmd from the extracted folder.' }
    if ((Get-FileHash -LiteralPath $ca -Algorithm SHA256).Hash -ne '431955C40FBB33012FF7FE8BABAB41FFC60807531B7DE68486F2621F62234E5E') { throw 'The PCAI certificate differs from the approved package. Ask IT for a fresh copy.' }
    $cfg = Get-Content -LiteralPath $template -Raw | ConvertFrom-Json
    if ($cfg.provider.'pcai-deepseek'.options.baseURL -ne 'https://deepseekv41flash.project-user-shahriln.serving.htp-ai-ai-application.awanheitech.local/v1' -or $cfg.provider.'pcai-deepseek'.options.apiKey -ne '{file:./api-token}') { throw 'The package settings are incomplete. Ask IT for a fresh copy.' }
    $candidates = @((Join-Path $env:LOCALAPPDATA 'Programs\OpenCode\OpenCode.exe'), (Join-Path $env:LOCALAPPDATA 'OpenCode\OpenCode.exe'), (Join-Path $env:LOCALAPPDATA 'Programs\@opencode-aidesktop\OpenCode.exe'), (Join-Path $env:ProgramFiles 'OpenCode\OpenCode.exe'))
    $app = $candidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
    if (!$app) {
        Add-Type -AssemblyName System.Windows.Forms
        $picker = New-Object System.Windows.Forms.OpenFileDialog
        $picker.Title = 'Select the installed OpenCode Desktop application'
        $picker.Filter = 'OpenCode Desktop|OpenCode.exe;opencode-desktop.exe'
        if ($picker.ShowDialog() -ne [Windows.Forms.DialogResult]::OK) { throw 'Setup cancelled. Install OpenCode Desktop first, then run setup again.' }
        $app = $picker.FileName
        $picker.Dispose()
    }
    if ([IO.Path]::GetFileName($app) -notin @('OpenCode.exe', 'opencode-desktop.exe')) { throw 'Select the installed OpenCode Desktop application, not its installer or CLI.' }
    $version = [Diagnostics.FileVersionInfo]::GetVersionInfo($app)
    if ($version.ProductMajorPart -ge 2 -or $version.FileMajorPart -ge 2) { throw 'This package is for OpenCode v1. Ask IT for a package matching your installed v2 application.' }
    $dir = Join-Path $env:USERPROFILE '.config\opencode\pcai'
    $tokenPath = Join-Path $dir 'api-token'
    Write-Host 'Your token is stored only in your Windows account. It is not added to this sharing package.'
    if (Test-Path -LiteralPath $tokenPath) { Write-Host 'Press Enter to keep your existing token, or paste a replacement.' }
    $secure = Read-Host 'Paste your PCAI API token' -AsSecureString
    if ($secure.Length -gt 0) {
        $plain = [Net.NetworkCredential]::new('', $secure).Password.Trim()
        if (!$plain -or $plain -match '\s') { throw 'Paste only the API token, without spaces or a Bearer prefix, then run setup again.' }
    } elseif (!(Test-Path -LiteralPath $tokenPath) -or (Get-Item -LiteralPath $tokenPath).Length -eq 0) { throw 'No token was entered. Run setup again when you have your API token.' }
    [void][IO.Directory]::CreateDirectory($dir)
    $acl = New-Object Security.AccessControl.DirectorySecurity
    $acl.SetAccessRuleProtection($true, $false)
    $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
    $rule = [Security.AccessControl.FileSystemAccessRule]::new($sid, 'FullControl', 'ContainerInherit,ObjectInherit', 'None', 'Allow')
    $acl.AddAccessRule($rule)
    Set-Acl -LiteralPath $dir -AclObject $acl
    $guard = [IO.File]::Open((Join-Path $dir 'setup.lock'), [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    $utf8 = [Text.UTF8Encoding]::new($false)
    if ($plain) { Put-File $tokenPath ($utf8.GetBytes($plain)) }
    Put-File (Join-Path $dir 'pcai.json') ([IO.File]::ReadAllBytes($template))
    Put-File (Join-Path $dir 'pcai-ai-essentials-ca.crt') ([IO.File]::ReadAllBytes($ca))
    Put-File (Join-Path $dir 'OpenCode-PCAI.cmd') ([IO.File]::ReadAllBytes($launchSource))
    Put-File (Join-Path $dir 'desktop-path.txt') ($utf8.GetBytes($app))
    $desktop = [Environment]::GetFolderPath('Desktop')
    if (!$desktop) { throw 'Windows could not locate your Desktop folder. Ask IT to check your Windows profile.' }
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut((Join-Path $desktop 'OpenCode PCAI.lnk'))
    $shortcut.TargetPath = Join-Path $dir 'OpenCode-PCAI.cmd'
    $shortcut.WorkingDirectory = $env:USERPROFILE
    $shortcut.Description = 'OpenCode with PCAI DeepSeek and the approved CA certificate'
    $shortcut.IconLocation = $app + ',0'
    $shortcut.Save()
    Write-Host ''
    Write-Host 'SETUP COMPLETE'
    Write-Host 'Save your work and fully quit OpenCode, including its tray instance.'
    Write-Host 'Then double-click OpenCode PCAI on your Desktop and send Hello.'
    Write-Host 'Use that shortcut each time. You can delete the extracted sharing folder.'
    Write-Host 'Existing OpenCode configuration files were not edited.'
} catch {
    Write-Host ('Setup did not finish: ' + $_.Exception.Message)
    exit 1
} finally {
    $plain = $null
    if ($secure) { $secure.Dispose() }
    if ($guard) { $guard.Dispose() }
    if ($temporary -and (Test-Path -LiteralPath $temporary)) { Remove-Item -LiteralPath $temporary -Force }
}

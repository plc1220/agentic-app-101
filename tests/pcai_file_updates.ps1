param([string]$SourcePath,[string]$InlinePath,[string]$Scratch)
$ErrorActionPreference='Stop'
foreach ($path in @($SourcePath,$InlinePath)) {
    $tokens=$null; $errors=$null
    $ast=[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $path),[ref]$tokens,[ref]$errors)
    if ($errors.Count) { $errors | ForEach-Object { Write-Host $_.Message }; throw ('Parse failed: '+$path) }
    Write-Host ('PowerShell parsed: '+[IO.Path]::GetFileName($path))
}
$tokens=$null; $errors=$null
$ast=[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $SourcePath),[ref]$tokens,[ref]$errors)
$fn=$ast.Find({param($node) $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq 'Put-File'},$true)
. ([scriptblock]::Create($fn.Extent.Text))
[void][IO.Directory]::CreateDirectory($Scratch)
$file=Join-Path $Scratch 'settings.json'
$bytes=[Text.Encoding]::UTF8.GetBytes('first setup')
Put-File $file $bytes
if ([IO.File]::ReadAllText($file) -ne 'first setup') { throw 'First write failed' }
$stamp=(Get-Item $file).LastWriteTimeUtc
Put-File $file $bytes
if ((Get-Item $file).LastWriteTimeUtc -ne $stamp) { throw 'Unchanged rerun rewrote file' }
Put-File $file ([Text.Encoding]::UTF8.GetBytes('updated setup'))
if ([IO.File]::ReadAllText($file) -ne 'updated setup') { throw 'Update failed' }
if (Get-ChildItem $Scratch -Filter '*.tmp') { throw 'Temporary files remained' }
Write-Host 'Actual Put-File function passed first write, unchanged rerun and update checks.'

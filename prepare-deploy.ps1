Write-Host "Preparing deployment bundle..."

$deployDir = Join-Path $PSScriptRoot "deploy_bundle"
if (Test-Path $deployDir) {
    Remove-Item -Recurse -Force $deployDir
}
New-Item -ItemType Directory -Path $deployDir | Out-Null

# Copy web files to the bundle ROOT (the app is served at /, with
# /bibles and /visuals alongside -- see wrangler.toml [assets])
Copy-Item -Path (Join-Path $PSScriptRoot "web\*") -Destination $deployDir -Recurse
Write-Host "[OK] Copied web/ contents to bundle root"

# Copy bibles JSON files
$biblesDir = Join-Path $deployDir "bibles"
New-Item -ItemType Directory -Path $biblesDir | Out-Null
Get-ChildItem -Path (Join-Path $PSScriptRoot "bibles") -Directory | ForEach-Object {
    $code = $_.Name
    $targetDir = Join-Path $biblesDir $code
    New-Item -ItemType Directory -Path $targetDir | Out-Null
    Copy-Item -Path (Join-Path $_.FullName "*.json") -Destination $targetDir
}
Write-Host "[OK] Copied bibles/"

# Copy visuals (skip XML)
Copy-Item -Path (Join-Path $PSScriptRoot "visuals") -Destination $deployDir -Recurse -Exclude "*.xml"
Write-Host "[OK] Copied visuals/"

$fileCount = @(Get-ChildItem -Path $deployDir -Recurse -File).Count
Write-Host ""
Write-Host "[OK] Ready! Total files: $fileCount"
Write-Host "Location: $deployDir"

# packaging/build_exes.ps1
# 產出單一免安裝資料夾 dist\IChing\（主程式 + Data Editor 共用 _internal）與 zip

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

python -m pip install pyinstaller

python -m PyInstaller --noconfirm --clean packaging\iching.spec
python -m PyInstaller --noconfirm --clean packaging\iching_data_editor.spec

$DistDir = Join-Path $Root "dist\IChing"
$MainExe = Join-Path $DistDir "IChing.exe"
if (-not (Test-Path $MainExe)) {
    throw "Build failed: $MainExe not found"
}

$EditorSrc = Join-Path $Root "dist\IChingDataEditor"
$EditorExeSrc = Join-Path $EditorSrc "IChingDataEditor.exe"
if (-not (Test-Path $EditorExeSrc)) {
    throw "Build failed: $EditorExeSrc not found"
}

# 主程式 _internal 是超集；只複製 Editor exe 到同一層共用 _internal
$EditorExeDest = Join-Path $DistDir "IChingDataEditor.exe"
Copy-Item -Path $EditorExeSrc -Destination $EditorExeDest -Force

# 移除舊的獨立 DataEditor 子目錄（若存在）
$LegacyEditorDir = Join-Path $DistDir "DataEditor"
if (Test-Path $LegacyEditorDir) {
    Remove-Item $LegacyEditorDir -Recurse -Force
}

# 刪除 dist 內暫存／多餘輸出，只保留 IChing 資料夾與 portable zip
$ExtraEditor = Join-Path $Root "dist\IChingDataEditor"
if (Test-Path $ExtraEditor) {
    Remove-Item $ExtraEditor -Recurse -Force
}

Get-ChildItem (Join-Path $Root "dist") -Force | Where-Object {
    $_.Name -notin @("IChing", "IChing-portable.zip")
} | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force
}

$Zip = Join-Path $Root "dist\IChing-portable.zip"
if (Test-Path $Zip) {
    Remove-Item $Zip -Force
}
Compress-Archive -Path (Join-Path $DistDir "*") -DestinationPath $Zip -Force

Write-Host "Done."
Write-Host "  App:    $DistDir\IChing.exe"
Write-Host "  Editor: $DistDir\IChingDataEditor.exe"
Write-Host "  Zip:    $Zip"
Write-Host "One folder, shared _internal. Copy or unzip on any Windows PC."
Write-Host "User data: %APPDATA%\IChing\data\"

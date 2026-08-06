# packaging/build_exes.ps1
# 以 PyInstaller 產出主程式與 Data Editor

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

python -m pip install -U pyinstaller PySide6

$Dist = Join-Path $Root "dist"
$Build = Join-Path $Root "build"
New-Item -ItemType Directory -Force -Path $Dist | Out-Null

# 主程式
python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name IChing `
  --paths $Root `
  --add-data "data\hexagrams.json;data" `
  --add-data "data\hexagram_map.py;data" `
  --hidden-import data.hexagram_map `
  --hidden-import core.paths `
  main.py

# Data Editor
python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name IChingDataEditor `
  --paths $Root `
  --add-data "data\hexagrams.json;data" `
  --add-data "data\hexagram_map.py;data" `
  --hidden-import data.hexagram_map `
  --hidden-import core.paths `
  --hidden-import tools.data_editor.main_window `
  --hidden-import tools.data_editor.store `
  tools\data_editor\main.py

Write-Host "Done. Exe folders:"
Write-Host "  $Dist\IChing\IChing.exe"
Write-Host "  $Dist\IChingDataEditor\IChingDataEditor.exe"

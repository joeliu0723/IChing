# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec — 主程式 IChing（onedir，免安裝資料夾）

from pathlib import Path

block_cipher = None
root = Path(SPECPATH).parent.resolve()
assets_ui = root / "assets" / "ui"

a = Analysis(
    [str(root / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "data" / "hexagrams.json"), "data"),
        (str(root / "data" / "hexagram_map.py"), "data"),
        (str(assets_ui / "hero_banner_desktop.png"), "assets/ui"),
        (str(assets_ui / "ornamental_divider.svg"), "assets/ui"),
    ],
    hiddenimports=[
        "data.hexagram_map",
        "core.paths",
        "core.hexagram",
        "core.hexagram_lookup",
        "core.history_manager",
        "core.controller",
        "core.presenter",
        "ui.main_window",
        "ui.history_page",
        "ui.pages.interpretation_page",
        "ui.widgets.collapsible_groupbox",
        "ui.widgets.brand_hero",
        "ui.widgets.content_viewer",
        "PySide6.QtSvg",
        "PySide6.QtSvgWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "unittest", "pytest"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="IChing",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="IChing",
)

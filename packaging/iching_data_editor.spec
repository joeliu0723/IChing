# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec — Data Editor（onedir，可併入 dist\IChing\DataEditor）

from pathlib import Path

block_cipher = None
root = Path(SPECPATH).parent.resolve()

a = Analysis(
    [str(root / "tools" / "data_editor" / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "data" / "hexagrams.json"), "data"),
        (str(root / "data" / "hexagram_map.py"), "data"),
    ],
    hiddenimports=[
        "data.hexagram_map",
        "core.paths",
        "tools.data_editor",
        "tools.data_editor.main_window",
        "tools.data_editor.store",
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
    name="IChingDataEditor",
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
    name="IChingDataEditor",
)

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MAMAVIDA.py'],
    pathex=[],
    binaries=[],
    datas=[('logos y archivos/dict_form_raw.txt', 'logos y archivos'), ('logos y archivos/dict_form_label.txt', 'logos y archivos'), ('logos y archivos/LOGO_5.png', 'logos y archivos'), ('logos y archivos/LOGO_ESCUELA.png', 'logos y archivos'), ('logos y archivos/logo_ui_idiscc-removebg.png', 'logos y archivos'), ('logos y archivos/LOGO_5.ico', 'logos y archivos')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MAMAVIDA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['LOGO_5.ico'],
)

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['convert.py'],          # Tên file script chính của bạn
    pathex=[],               # Nếu cần, thêm đường dẫn thư mục chứa script ở đây
    binaries=[],
    datas=[],                # Nếu có thêm file dữ liệu cần đóng gói, thêm ở đây
    hiddenimports=[],        # Nếu có thư viện import động, thêm ở đây
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
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
    name='convert',           # Tên file exe đầu ra
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,             # True để hiện console, False nếu muốn ẩn console window
    disable_windowed_traceback=False,
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
    upx=True,
    upx_exclude=[],
    name='convert',
)


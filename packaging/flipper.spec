# -*- mode: python ; coding: utf-8 -*-
# Build on a Mac, from the repo root:
#   pyinstaller --noconfirm packaging/flipper.spec

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all("PySide6")
datas += [("src/flipper/modules/config/ConfigPanel.qml", "flipper/modules/config")]

a = Analysis(
    ["src/flipper/app.py"],
    pathex=["src"],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="Flipper",
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="Flipper",
)
app = BUNDLE(
    coll,
    name="Flipper.app",
    bundle_identifier="com.jmw.flipper",
)


# -*- mode: python ; coding: utf-8 -*-
# Build on a Mac, from the repo root:
#   pyinstaller --noconfirm packaging/flipper.spec

from pathlib import Path

from PyInstaller.utils.hooks import collect_all

# Paths in a spec are relative to this file, which lives in packaging/.
root = Path(SPECPATH).resolve().parent

datas, binaries, hiddenimports = collect_all("PySide6")
datas += [(
    str(root / "src/flipper/modules/config/ConfigPanel.qml"),
    "flipper/modules/config",
)]

a = Analysis(
    [str(root / "src/flipper/app.py")],
    pathex=[str(root / "src")],
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


# -*- mode: python ; coding: utf-8 -*-
import importlib
import sys

from pathlib import Path

sys.path.insert(0, Path().absolute().as_posix())
from core.constants import APP_VERSION

block_cipher = None


a = Analysis(['core\\app.py'],
             pathex=['D:\\Work\\Miss Poe\\Costings'],
             binaries=[],
             datas=[('resources\\*.ico', 'resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name=f'Poe Excel Automator {APP_VERSION}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='resources\\MissPoeVectorExcel.ico',
          console=True)

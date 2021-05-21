# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['E:/PycharmProjects/ThermalCalc/main.py'],
             pathex=['E:\\PycharmProjects\\ThermalCalc'],
             binaries=[],
             datas=[
			 ('E:\PycharmProjects\ThermalCalc\materials\*', "materials"),
			 ('E:\PycharmProjects\ThermalCalc\POWERPNT_CXLFW6i2uP.png', '.'),
			 ('E:\PycharmProjects\ThermalCalc\POWERPNT_nmj5jX9473.png', '.')
			 ],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='E:/PycharmProjects/ThermalCalc/slab.ico')

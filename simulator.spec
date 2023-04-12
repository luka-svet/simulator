# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None


a = Analysis(['simulator.pyw'],
             pathex=['C:\\Users\\DrPai\\OneDrive\\Documents\\Šola\\KU Leuven\\PhD\\Working files\\Mathematical model resistance evolution\\Simulator'],
             binaries=[],
             datas=[('./data/images/defaulttheme.atlas', './data/images/'), ('./data/images/defaulttheme-0.png', './data/images/'), ('./bin/ui/dynamic_classes.kv', './bin/ui/'), ('./bin/ui/main_layout.kv', './bin/ui/'), ('./bin/ui/text.xml', './bin/ui/'), ('./bin/ui/treatment_adaptive.kv', './bin/ui/'), ('./bin/ui/treatment_classic.kv', './bin/ui/'), ('./bin/ui/treatment_user.kv', './bin/ui/'), ('./bin/ui/icon.ico', './bin/ui/')],
             hiddenimports=['win32timezone', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='simulator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
		  clean=True,
          console=False, icon='bin\\ui\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('C:\\Users\\DrPai\\AppData\\Local\\Programs\\Python\\Python311\\share\\sdl2\\bin'),
               Tree('C:\\Users\\DrPai\\AppData\\Local\\Programs\\Python\\Python311\\share\\glew\\bin'),
               strip=False,
               upx=True,
               upx_exclude=[],
               name='simulator')

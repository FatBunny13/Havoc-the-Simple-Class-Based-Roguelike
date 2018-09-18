# -*- mode: python -*-

block_cipher = None


a = Analysis(['libtcod.dll', 'libtcodgui.dll', 'SDL2.dll', 'engine.py'],
             pathex=['C:\\Users\\Alfonso Abraham\\Documents\\Havoc\\Havoc-the-Simple-Class-Based-Roguelike-master'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='libtcod',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='libtcod')

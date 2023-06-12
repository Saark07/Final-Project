# specfile.spec

# Import the required module
import sys
from PyQt5.Qt import *

# Define the main script
a = Analysis(['FinalProject.py'],
             pathex=[],
             binaries=[],
             datas=[('ui_files/page1.ui', 'ui_files'),
                    ('ui_files/page2.ui', 'ui_files'),
                    ('ui_files/page3.ui', 'ui_files'),
                    ('images/icon.png', 'images'),
                    ('images/icon.ico', 'images'),
                    ('images/robotic_arm.jpg', 'images'),
                    ('images/home_button.png', 'images'),
                    ('csv_files/paper_names_id.csv', 'csv_files'),
                    ('csv_files/reconstructed_edges.csv', 'csv_files')],

             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None)

# Create the executable
pyz = PYZ(a.pure, a.zipped_data,
          cipher=None)

# Create the EXE
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FinalProject',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='images/icon.ico',
          console=False)

# Delete unnecessary files
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FinalProject')


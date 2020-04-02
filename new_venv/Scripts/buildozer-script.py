#!C:\Users\kurku\PycharmProjects\test\new_venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'buildozer==1.0.1.dev0','console_scripts','buildozer'
__requires__ = 'buildozer==1.0.1.dev0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('buildozer==1.0.1.dev0', 'console_scripts', 'buildozer')()
    )

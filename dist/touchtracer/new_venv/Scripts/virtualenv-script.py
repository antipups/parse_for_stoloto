#!C:\Users\kurku\PycharmProjects\test\new_venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'virtualenv==20.0.13','console_scripts','virtualenv'
__requires__ = 'virtualenv==20.0.13'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('virtualenv==20.0.13', 'console_scripts', 'virtualenv')()
    )

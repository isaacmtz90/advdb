#!c:\Users\Isaac\Documents\NTHU\adbproy\advdb\server-flask\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'py2neo==2.0.8','console_scripts','neoget'
__requires__ = 'py2neo==2.0.8'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('py2neo==2.0.8', 'console_scripts', 'neoget')()
    )

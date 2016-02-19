import os, sys
from security import security

full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
app_dir = '/filemanager'
security.accounts = {"test": "test", "test2": "test2"}
security.admins = ["test2"]
exclude = []
log_debug = True

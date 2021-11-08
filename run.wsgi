activate_this = '/home/zabra79467/.local/share/virtualenvs/flaskpage-QKy0shMA/bin/activate_this.py'
with open(activate_this) as file_:
  exec(file_.read(), dict(__file__=activate_this))


import sys
sys.path.insert(0,"/var/www/flaskpage")

from app import app as application


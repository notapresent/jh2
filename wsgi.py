# -*- coding: utf-8 -*-
import os

app_env = os.environ.get('RBM2M_ENV', 'Production')

if app_env == 'Production':
    venv_path = os.path.join(os.path.dirname(__file__), 'venv')
    activate_this = os.path.join(venv_path, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

from rbm2m.webapp import create_app

app = create_app(app_env)

if __name__ == "__main__":
    app.run()

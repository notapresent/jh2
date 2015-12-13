# -*- coding: utf-8 -*-
import os

from rbm2m import middleware


base_dir = os.path.dirname(__file__)
venv_path = os.path.join(base_dir, 'venv')

app_env = os.environ.get('RBM2M_ENV', 'Production')

if app_env == 'Production' and os.path.isdir(venv_path):
    activate_this = os.path.join(venv_path, 'bin/activate_this.py')
    execfile(activate_this, dict(__file__=activate_this))

from rbm2m.webapp import create_app         # noqa

app = create_app(app_env)
app.wsgi_app = middleware.ReverseProxied(app.wsgi_app)

if __name__ == "__main__":
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', 8080))
    )

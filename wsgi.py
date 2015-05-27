# -*- coding: utf-8 -*-
import os
from rbm2m.webapp import create_app

app_env = os.environ.get('RBM2M_ENV', 'Production')
app = create_app(app_env)

if __name__ == "__main__":
    app.run()

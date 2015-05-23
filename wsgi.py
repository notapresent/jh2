# -*- coding: utf-8 -*-
from rbm2m import create_app
from rbm2m.config import app_environment


app = create_app(app_environment)

if __name__ == "__main__":
    app.run()

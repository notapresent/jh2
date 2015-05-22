# -*- coding: utf-8 -*-

from rbm2m import config, create_app

app = create_app(config.app_environment)

if __name__ == "__main__":
    app.run()

Requirements
============

* Python 2.7
* Mysql 5.1+
* Redis
* pip
* virtualenv
* supervisor
* libmysqlclient-dev or similar 


Configuration
=============

`RBM2M_ENV` - App environment, one of Development, Production, Testing 
`RBM2M_LOGIN` - management interface login 
`RBM2M_PASSWORD` - management interface password
`SQLALCHEMY_DATABASE_URI` - MySQL connection settings, for example `mysql+mysqldb://rbm2m:rbm2m@127.0.0.1/rbm2m?charset=utf8mb4`
`REDIS_URL` - Redis connection settings, for example `redis://@localhost:6379/0`
`MEDIA_DIR` - Directory for images, must be writable. Default value: `APP_DIR/media` 
`LOGS_DIR` - Directory for logs, must be writable. Default value: `APP_DIR/logs`

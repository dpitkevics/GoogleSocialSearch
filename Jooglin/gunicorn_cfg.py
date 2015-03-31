bind = 'localhost:8777'
pidfile = 'gunicorn_pid'
daemon = True
accesslog = '/var/log/jooglin/gunicorn_access.log'
errorlog = '/var/log/jooglin/gunicorn_error.log'
loglevel = 'info'
workers = 3
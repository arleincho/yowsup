# Sample Gunicorn configuration file.
import multiprocessing

#
# Server socket
#
bind = "127.0.0.1:8019"
# bind = 'unix:/tmp/gunicorn.api-nethub.sock'
backlog = 2048

#
# Worker processes
#
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'egg:gunicorn#tornado'
# worker_class = 'egg:gunicorn#gevent'
# worker_connections = 1000
timeout = 120
keepalive = 2

#
# Debugging
#
debug = True
spew = False

#
# Server mechanics
#
daemon = False
pidfile = "/var/python-apps/run/yowsup.lock"
umask = 0
# user = "www-data"
user = "_www"
group = None
tmp_upload_dir = "/var/python-apps/tmp/"

#
#   Logging
#
loglevel = 'debug'
errorlog = '/var/python-apps/log/yowsup-error.log'
accesslog = '/var/python-apps/log/yowsup-access.log'
# logconfig = '/var/python-apps/log/api2-log.log'


#
# Process naming
#
proc_name = "yowsup-unix"

#
# Server hooks
#

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

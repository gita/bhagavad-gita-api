import multiprocessing

# bind - The server socket to bind
bind = "0.0.0.0:8081"

# backlog - The maximum number of pending connections
# Generally in range 64-2048
backlog = 2048

# workers - The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
workers = multiprocessing.cpu_count() * 2 + 1

# worker_class - The type of workers to use
# A string referring to one of the following bundled classes:
# 1. sync
# 2. eventlet - Requires eventlet >= 0.9.7
# 3. gevent - Requires gevent >= 0.13
# 4. tornado - Requires tornado >= 0.2
#
# You’ll want to read http://docs.gunicorn.org/en/latest/design.html
# for information on when you might want to choose one of the other
# worker classes
worker_class = "uvicorn.workers.UvicornWorker"

# threads - The number of worker threads for handling requests. This will
# run each worker with the specified number of threads.
# A positive integer generally in the 2-4 x $(NUM_CORES) range
threads = 1

# worker_connections - The maximum number of simultaneous clients
# This setting only affects the Eventlet and Gevent worker types.
worker_connections = 1000

# max_requests - The maximum number of requests a worker will process
# before restarting
# Any value greater than zero will limit the number of requests a work
# will process before automatically restarting. This is a simple method
# to help limit the damage of memory leaks.
max_requests = 0

# max_requests_jitter - The maximum jitter to add to the max-requests setting
# The jitter causes the restart per worker to be randomized by
# randint(0, max_requests_jitter). This is intended to stagger worker
# restarts to avoid all workers restarting at the same time.
max_requests_jitter = 0

# timeout - Workers silent for more than this many seconds are killed
# and restarted
timeout = 30

# graceful_timeout - Timeout for graceful workers restart
# How max time worker can handle request after got restart signal.
# If the time is up worker will be force killed.
graceful_timeout = 30

# keep_alive - The number of seconds to wait for requests on a
# Keep-Alive connection
# Generally set in the 1-5 seconds range.
keep_alive = 2

# accesslog - The Access log file to write to.
# "-" means log to stdout.
accesslog = "-"

# errorlog - The Error log file to write to.
# "-" means log to stderr.
errorlog = "-"

# loglevel - The granularity of Error log outputs.
# Valid level names are:
# 1. debug
# 2. info
# 3. warning
# 4. error
# 5. critical
loglevel = "info"

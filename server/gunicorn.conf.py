# Gunicorn configuration for Render deployment
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
backlog = 2048

# Worker processes
workers = 1  # Keep low due to memory constraints
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Memory management
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "ecommerce-chatbot"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

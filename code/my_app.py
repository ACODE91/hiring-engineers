from flask import Flask
import logging
import sys
import time
from ddtrace import tracer
from ddtrace import config

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

config.flask['service_name'] = 'RubensFlaskApp'

@app.route('/')
@tracer.wrap(name='Home')
def api_entry():
    time.sleep(0.01)
    # Use the .trace method to create
    # a span named "my_trace" to trace
    # just these lines of code:
    with tracer.trace("my_span") as span:
        # Designate this span as a separate service:
        span.service="my_service"
        # Add metadata:
        span.set_tag('service_type','my_service_type')
        time.sleep(0.03)
    return 'Entrypoint to the Application'

@app.route('/api/apm')
@tracer.wrap(name='Trace')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
"my_app.py" 47L, 1238C

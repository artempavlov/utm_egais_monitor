from prometheus_client import start_http_server, Summary, Info
import random
import time

# Create a metric to track time spent and requests made.
#REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(38000)
    # Generate some requests.
    i = Info('j', 'counter')
    for j in range(1000):
        i.info({'j': str(j)})
        time.sleep(1)
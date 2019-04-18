import logging

from rest_server import app as application

log_stderr = logging.StreamHandler()
log_stderr.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(module)s] %(name)s  - %(funcName)s(): %(message)s')
log_stderr.setFormatter(formatter)
logging.basicConfig(level=10, handlers=[log_stderr])
logging.getLogger("converters").setLevel(logging.INFO)

if __name__ == '__main__':
    application.run()

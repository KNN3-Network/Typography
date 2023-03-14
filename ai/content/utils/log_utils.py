import logging
import os
LOG_FILE = os.path.join(os.path.split(os.path.realpath(__file__))[0],'../../logs/run.log')

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger = logging.getLogger(__name__)

handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(format))

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s %(levelname)s %(message)s')
logger.addHandler(handler)


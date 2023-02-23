import os
from fake_useragent import UserAgent

project_dir = os.path.join(os.path.dirname(__file__), '..')
log_dir = os.path.join(project_dir, 'log')

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

ua = UserAgent()
def set_rand_ua(header):
    header['User-Agent'] = ua.random
    
    
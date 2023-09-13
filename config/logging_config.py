import logging


# 配置日志记录器
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# 配置控制台日志处理器
console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)

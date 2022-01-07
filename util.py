import random
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s',
                    )

LOG = logging

def get_chance(percent, max=99):
    num = random.randint(0, max)
    LOG.info(f'Get chance of {percent}/{max + 1}: {num}')
    return num < percent
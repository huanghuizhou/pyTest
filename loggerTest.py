import logging


def get_logger(name):
    logging.basicConfig(filename='./111aaa.log')
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    # Standard output handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter('%(levelname)s - %(name)s:%(lineno)s: %(message)s'))
    log.addHandler(sh)
    return log


logger = get_logger(__file__)

def aaa():
    print(__file__)
    logger.debug("12222222222222222")

if __name__=="__main__":
    aaa()
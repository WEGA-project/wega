import logging


def float_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            return 0.00
        
      
    return wrapper
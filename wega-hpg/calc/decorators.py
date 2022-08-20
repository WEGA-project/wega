import  decimal
import logging


def decimal_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return decimal.Decimal(0.000)
        
      
    return wrapper
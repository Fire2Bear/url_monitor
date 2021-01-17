try:
    from .local_settings import *
except ImportError as e:
    print("No local settings module found")

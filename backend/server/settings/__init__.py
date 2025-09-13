from .base import *
import os


# Import settings depended on the enviroment
if os.getenv('DJANGO_ENV') == 'production':
    from .production import *
else:
    from .development import *
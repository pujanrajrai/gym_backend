from decouple import config

settings_key = config('settings_key', default='local')

if settings_key == "local":
    from .local import *
elif settings_key == "dev":
    from .dev import *
elif settings_key == "prod":
    from .prod import *

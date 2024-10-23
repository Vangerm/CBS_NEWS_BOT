logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(filename)s:%(lineno)d #%(levelname)-8s '
            '[%(asctime)s] -%(name)s - %(message)s'
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.FileHandler',
            'filename': 'loger/logs.log',
            'mode': 'w',
            'level': 'INFO',
            'formatter': 'default',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'user_handlers': {
            'level': 'INFO',
            'handlers': ['default']
        },
        'other_handlers': {
            'level': 'INFO',
            'handlers': ['default']
        }
    },
    'root': {
        'formatter': 'default',
        'handlers': ['default'],
        'level': 'INFO'
    }
}


CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S'
        },
        'monitor': {
            'format': '%(asctime)s %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'default':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'default'
        },
        'monitor':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'monitor'
        }
    },
    'loggers': {
        'Example': {
            'handlers':['default'],
            'propagate': False,
            'level':'DEBUG',
        },
        'Monitor': {
            'handlers':['monitor'],
            'propagate': False,
            'level':'INFO',
        }
    }
}

import logging
import logging.config


logging.config.dictConfig(CONFIG)

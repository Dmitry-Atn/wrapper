from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'wrapper.log',
            'mode': 'w',
            'formatter': 'default',
            'maxBytes': 10*1024*1024,
            'backupCount': 10
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi','file']
    }
})
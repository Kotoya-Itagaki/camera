import os
import sys
import yaml

from logging import getLogger, config, DEBUG, INFO


# logsフォルダの作成
if not os.path.exists('logs'):
    os.mkdir('logs')

# ログに関する設定
log_cfg = {
    "version": 1,
    "disable_existing_loggers": "false",
    "formatters": {
        "simple": {
            "format": "%(process)s: %(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s"
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "MainRotatingFileHandler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "mode": "a",
            "backupCount": 5,  # 5世代保持
            "maxBytes": 10485760,  # 1ファイル10MB
            "filename": f"./logs/.log",
            "encoding": "utf-8"
        },
    },
    "loggers": {
        "main": {
            "handlers": ["consoleHandler", "MainRotatingFileHandler"],
            "propagate": "no"
        },
        "image_capture": {
            "handlers": ["consoleHandler", "MainRotatingFileHandler"],
            "propagate": "no"
        },
        "camera_image": {
            "handlers": ["consoleHandler", "MainRotatingFileHandler"],
            "propagate": "no"
        },
    }
}


def get_logger(name, level=DEBUG):
    """ロガーの取得"""

    logger = getLogger(name)
    logger.setLevel(level)

    config.dictConfig(log_cfg)

    return getLogger(name)

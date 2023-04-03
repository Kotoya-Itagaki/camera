import os
import sys
import yaml

from logging import getLogger, config, DEBUG, INFO


# logsフォルダの作成
if not os.path.exists('logs'):
    os.mkdir('logs')

# コマンドライン引数の受け取り
args = sys.argv
file_dir = os.path.dirname(os.path.realpath(__file__))
config_file_name = os.path.join(file_dir, args[1]) 


def get_config(config_file_name):

    try:
        with open(config_file_name, encoding='utf-8') as yml:
            cfg = yaml.safe_load(yml)

    except FileNotFoundError:
        print(f'設定ファイルが読み込めませんでした。ファイル名:{config_file_name}')
        raise

    main_conf = cfg.get('main')

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
                "filename": f"./logs/__main_{main_conf.get('location')}.log",
                "encoding": "utf-8"
            },

            "FTPRotatingFileHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "mode": "a",
                "backupCount": 5,  # 5世代保持
                "maxBytes": 10485760,  # 1ファイル10MB
                "filename": f"./logs/__ftp_{main_conf.get('location')}.log",
                "encoding": "utf-8"
            },
            "MQTTRotatingFileHandler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "mode": "a",
                "backupCount": 5,  # 5世代保持
                "maxBytes": 10485760,  # 1ファイル10MB
                "filename": f"./logs/__mqtt_{main_conf.get('location')}.log",
                "encoding": "utf-8"
            }
        },
        "loggers": {
            "__main__": {
                "handlers": ["consoleHandler", "MainRotatingFileHandler"],
                "propagate": "no"
            },
            "delete_videos": {
                "handlers": ["consoleHandler", "MainRotatingFileHandler"],
                "propagate": "no"
            },
            "cli": {
                "handlers": ["consoleHandler", "MainRotatingFileHandler"],
                "propagate": "no"
            },
            "settings": {
                "handlers": ["consoleHandler", "MainRotatingFileHandler"],
                "propagate": "no"
            },
            "camera_image": {
                "handlers": ["consoleHandler", "MainRotatingFileHandler"],
                "propagate": "no"
            },
            "ftp_stor": {
                "handlers": ["consoleHandler", "FTPRotatingFileHandler"],
                "propagate": "no"
            },
            "mqtt": {
                "handlers": ["consoleHandler", "MQTTRotatingFileHandler"],
                "propagate": "no"
            }
        }
    }

    return log_cfg


def get_logger(name, level=DEBUG):
    """ロガーの取得"""

    logger = getLogger(name)
    logger.setLevel(level)
    
    if not logger.hasHandlers():
        config.dictConfig(get_config(config_file_name))
    
    return getLogger(name)

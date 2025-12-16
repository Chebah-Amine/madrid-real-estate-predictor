from app.config.config import config

config_name = 'default'


def set_config_name(cfg_name):
    global config_name
    config_name = cfg_name


def get_mongo_config():
    cfg = config[config_name].MONGODB_SETTINGS
    uri = (f"mongodb://"
           f"{cfg['username']}:{cfg['password']}"
           f"@{cfg['host']}:{cfg['port']}/?authSource=admin"
           ) \
        if cfg['username'] and cfg['password'] \
        else f"mongodb://{cfg['host']}:{cfg['port']}/"
    return uri, cfg['db'], cfg['collection']

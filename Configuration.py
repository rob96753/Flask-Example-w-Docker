import json
import os
from Constants import CONFIG_PATH_ENV_VAR, DONATIONS

def getConfigItem(key):
    item = None
    if not CONFIG_PATH_ENV_VAR in os.environ.keys():
        raise Exception(f'The Environment Must Contain  {CONFIG_PATH_ENV_VAR} As the Path to the Configuration File')
    try:
        configFilePath = os.environ.get(CONFIG_PATH_ENV_VAR)
        with open(os.path.join(configFilePath, DONATIONS), "r+") as cfp:
            config = json.load(cfp)
            if key in config.keys():
                item = config[key]
            else:
                raise ValueError(f'Exception in getConfigItem for {key}')
        return item
    except json.JSONDecodeError as jex:
        raise Exception("getConfigItem: JSON Decode Error {jex.msg} {jex.doc} {jex.pos}")
    except Exception as ex:
        raise Exception(f'Exception in getItem for {key} "{str(ex)}"')

def getList(key):
    listOfValues = {}
    cfp = None
    listfp = None

    if not CONFIG_PATH_ENV_VAR in os.environ.keys():
        raise Exception(f'The Environment Must Contain  {CONFIG_PATH_ENV_VAR} As the Path to the Configuration File')
    try:
        configFilePath = os.environ.get(CONFIG_PATH_ENV_VAR)
        with open(os.path.join(configFilePath, DONATIONS), "r+") as cfp:
            config = json.load(cfp)
            if key in config.keys():
                with open(os.path.join(configFilePath, config[key]), "r+") as listfp:
                    listOfValues = json.load(listfp)
            return listOfValues
    except json.JSONDecodeError as jex:
        raise Exception("getList: JSON Decode Error {jex.msg} {jex.doc} {jex.pos}")
    except Exception as ex:
        raise Exception(f'Exception in getList for {key} {str(ex)}')
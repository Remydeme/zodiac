import json

def CreateConfig(path):
    """
    load the config using path
    :param path: {str}
        path to config file
    :return:
        dictionnary that contains all the configs
    """
    with open(path, 'r') as config_file:
        config = json.load(config_file)
    return config
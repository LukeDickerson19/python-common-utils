from constants import *
import configparser



''' get_property()

    Description:
        getter function for values in the
            .properties file (path specified in PROPERTY_FILEPATH in constants.py)
            in the specified section
            with the specified key.

    Arguments:
        string ........... section ... the [Section] of the .properties file where the key is
        string ........... key ....... the string used to identify the desired value in the .properties file

    Returns:
        tuple ...
            string ....... value ..... the value associated with the specified section and key in the .properties file
                                       or None if [section] and/or key don't exist in the .properties file
            successful ... boolean ... flag if the function executed successfully without any errors

    '''
def get_property(
    section,
    key):

    try:
        config = configparser.RawConfigParser()
        config.read(PROPERTY_FILEPATH)
        value = eval(config.get(section, key))
        successful = True
    except Exception as e:
        value = None
        successful = False
    return value, successful



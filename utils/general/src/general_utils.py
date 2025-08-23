from constants import *
import configparser



class Properties:

    def __init__(
        self,
        properties_filepath):

        self.path = properties_filepath
        self.config = configparser.RawConfigParser()
        self.config.read(properties_filepath)

    ''' get()

        Description:
            getter function for values in the
                .properties file (path specified in PROPERTY_FILEPATH in constants.py)
                in the specified section
                with the specified key.

        Arguments:
            string ........... section ... the [Section] of the .properties file where the key is
            string ........... key ....... the string used to identify the desired value in the .properties file

        Returns:
            string ....... value ..... the value associated with the specified section and key in the .properties file
                                       or None if [section] and/or key don't exist in the .properties file

        '''
    def get(
        self,
        section,
        key):

        try:
            value = eval(self.config.get(section, key))
        except Exception as e:
            value = None
        return value

    def set(self, section, key, value):

        # TODO: see if the .set() fn does this automatically
        if section not in self.config.sections():
            self.config.add_section(section)

        config.set(section, key, value)

        # sources
        # https://stackoverflow.com/questions/49062073/how-to-add-section-and-values-to-ini-using-configparser-in-python
        # https://stackoverflow.com/questions/22068050/iterate-over-sections-in-a-config-file


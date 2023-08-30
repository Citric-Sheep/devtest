##############
# Libraries #
##############

import os

from dotenv import load_dotenv

####################
# Load .env files #
####################

env_data_path = os.path.abspath(os.path.join(__file__,
                                             "../../configuration/.env"))
load_dotenv(dotenv_path=env_data_path)


########################################
# Configuration of project attributes #
########################################

class ConfigurationProjectAttributes:
    def __init__(self,
                 project_name,
                 project_version):
        self.PROJECT_NAME: str = os.getenv(project_name)
        self.PROJECT_VERSION: str = os.getenv(project_version)


#################################
# Configuration of db instance #
#################################

class ConfigurationDbCredentials:
    def __init__(self,
                 db_user,
                 db_password,
                 db_server,
                 db_port,
                 db_name):
        self.DB_USER: str = os.getenv(db_user)
        self.DB_PASSWORD = os.getenv(db_password)
        self.DB_SERVER: str = os.getenv(db_server,
                                        "localhost")
        self.DB_PORT: str = os.getenv(db_port,
                                      5432)
        self.DB_NAME: str = os.getenv(db_name,
                                      "tdd")
        self.DB_URL = f"postgresql://" \
                      f"{self.DB_USER}:" \
                      f"{self.DB_PASSWORD}@" \
                      f"{self.DB_SERVER}:" \
                      f"{self.DB_PORT}/" \
                      f"{self.DB_NAME}"


class ConfigurationTestDbCredentials:
    def __init__(self,
                 db_user,
                 db_password,
                 db_server,
                 db_port,
                 db_name):
        self.DB_USER: str = os.getenv(db_user)
        self.DB_PASSWORD = os.getenv(db_password)
        self.DB_SERVER: str = os.getenv(db_server,
                                        "localhost")
        self.DB_PORT: str = os.getenv(db_port,
                                      5432)
        self.DB_NAME: str = os.getenv(db_name,
                                      "tdd")
        self.DB_URL = f"postgresql://" \
                      f"{self.DB_USER}:" \
                      f"{self.DB_PASSWORD}@" \
                      f"{self.DB_SERVER}:" \
                      f"{self.DB_PORT}/" \
                      f"{self.DB_NAME}"


##########################################
# Execution of configuration attributes #
##########################################

configure_project_attributes = ConfigurationProjectAttributes('PROJECT_NAME',
                                                              'PROJECT_VERSION')

configure_bd_credentials = ConfigurationDbCredentials('DB_USER',
                                                      'DB_PASSWORD',
                                                      'DB_SERVER',
                                                      'DB_PORT',
                                                      'DB_NAME')
configure_bd_test_credentials = ConfigurationTestDbCredentials('DB_TEST_USER',
                                                               'DB_TEST_PASSWORD',
                                                               'DB_TEST_SERVER',
                                                               'DB_TEST_PORT',
                                                               'DB_TEST_NAME')

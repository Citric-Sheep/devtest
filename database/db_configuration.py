##########################
# Libraries#
##########################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration import configuration

########################
# Database connection #
########################

db_sqlalchemy_url = configuration.configure_bd_credentials.DB_URL
db_sqlalchemy_engine = create_engine(db_sqlalchemy_url,
                                     pool_size=20)
db_sqlalchemy_session = sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=db_sqlalchemy_engine)

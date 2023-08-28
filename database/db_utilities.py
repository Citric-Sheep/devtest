##############
# libraries #
##############

from database.db_configuration import db_sqlalchemy_session


#########################
# Connection functions #
#########################

def db_connection():
    db_connect = db_sqlalchemy_session()
    try:
        yield db_connect
    finally:
        db_connect.close()

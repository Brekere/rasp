class BaseConfig(object):
    'Base configuracion'
    SECRET_KEY = 'Key5&6423v-daD2?s'
    DEBUG = True
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:ASB.13@192.168.0.13/industria4'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://asbsistemas:asbsistemas@192.168.0.11:3306/app4"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:asb.#21@192.168.0.21:3306/historic"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret!'
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'Desarrollo key'
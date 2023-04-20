class BaseConfig(object):
    'Base configuracion'
    SECRET_KEY = 'Key5&6423v-daD2?s'
    DEBUG = True
    TESTING = False
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:asbsistemas@localhost:5432/industria4"
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:ASB.13@192.168.0.19/industria4'
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:asbsistemas@localhost:5432/indutria4"
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://DESKTOP-AQ2ALR2/asb?driver=ODBC Driver 17 for SQL Server"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:asb.#21@localhost:3306/historic"
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
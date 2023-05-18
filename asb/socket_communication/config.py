
class DevConfig(object):   
    debug = True   
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://agg:db.#As4kL@localhost:3306/historic"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:asb.Mx#21@localhost:3306/historic"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:asb.#21@localhost:3306/historic"
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:ASB.13@192.168.0.13/industria4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

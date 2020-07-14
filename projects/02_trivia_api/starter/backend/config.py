# this function sets all config params of the application
#  
def config_db(app, database_name):

    database_path = "postgresql://postgres:123456789@localhost:5432/{}".format(
        database_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = 'udacity'
    app.config['CORS_HEADERS'] = 'Content-Type'

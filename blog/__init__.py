from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from blog import routes, models




'''config = configparser.ConfigParser()
    config.read(
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)), fileName))'''
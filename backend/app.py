from flask import Flask
from extensions import db
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models.user import User
from routes.auth_routes import auth
from flask_jwt_extended import JWTManager

load_dotenv()


app = Flask(__name__)

app.register_blueprint(auth)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/"
    f"{os.getenv('MYSQL_DB')}"
)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

db.init_app(app)

jwt = JWTManager(app)

@app.route('/')
def home():
    return "Flask Backend Running"

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask_smorest import Api
from models import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['API_TITLE'] = 'Product API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')

db.init_app(app)

api = Api(app)


from views import blp
api.register_blueprint(blp)

# print(app.url_map)

# with app.app_context():
#     db.create_all()
#     print('Database has been created!')

if __name__ == '__main__':
    app.run(debug=True) # This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.

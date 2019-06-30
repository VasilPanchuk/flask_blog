from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

@app.route('/')
def home():
    return 'ok', 200

if __name__ == '__main__':
    db.create_all()
    app.run()
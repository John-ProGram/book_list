# Rodar a aplicação

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/livros_database'
    
    # conecta o objeto db(que representa o SQLAlchemy) ao flask(app)
    # necessário quando você cria o db fora do app
    db.init_app(app)
    return app

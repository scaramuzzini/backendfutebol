from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50))
    ano_fundacao = db.Column(db.Integer)
    estadio = db.Column(db.String(100))
    titulos = db.Column(db.Integer)

class TimeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Time
        load_instance = True

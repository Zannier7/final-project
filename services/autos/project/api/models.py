# services/users/project/api/models.py

from sqlalchemy.sql import func
from project import db

class Auto(db.Model):

    __tablename__ = 'autos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(128), nullable=False)
    modelo = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(128), nullable=False)
    placa = db.Column(db.String(128), nullable=False)

    def __init__(self, marca, modelo, tipo, color, placa):
        self.marca = marca
        self.modelo = modelo
        self.tipo = tipo
        self.color = color
        self.placa = placa

    def to_json(self):
        return {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'tipo': self.tipo,
            'color': self.color,
            'placa': self.placa
        }
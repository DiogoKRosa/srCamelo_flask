from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class Usuario():
    def __init__(self, tipo, nome, cpf, email, telefone, senha, pais, uf, cidade, imagem):
        self.tipo = tipo
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.pais = pais
        self.uf = uf
        self.cidade = cidade
        self.imagem = imagem
    
    def save(self):
        mongo.db.usuarios.insert_one({
            'tipo': self.tipo,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'senha': self.senha,
            'pais': self.pais,
            'uf': self.uf,
            'cidade': self.cidade,
            'imagem': self.imagem
        })
    
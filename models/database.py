from flask_pymongo import PyMongo
from bson import ObjectId
from flask import jsonify

mongo = PyMongo()

class Usuario():
    def __init__(self, tipo, nome, cpf, email, telefone, senha, pais, uf, cidade, imagem_perfil, nome_fantasia, forma_pagamento, imagem_loja):
        self.tipo = tipo
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.pais = pais
        self.uf = uf
        self.cidade = cidade
        self.imagem_perfil = imagem_perfil,
        self.nome_fantasia = forma_pagamento,
        self.imagem_loja = imagem_loja
    
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
            'imagem_perfil': self.imagem_perfil,
            'nome_fantasia': self.nome_fantasia,
            'imagem_loja': self.imagem_loja
        })
        
    @staticmethod
    def trazerLogin(email):
        select = mongo.db.usuarios.find_one({'email': email})
        return select
    
class Produto():
    def __init__(self, id_vendedor, nome, preco, descricao, categoria):
        self.id_vendedor = id_vendedor
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria

    def save(self):
        mongo.db.produtos.insert_one({
            'id_vendedor': self.id_vendedor,
            'nome': self.nome,
            'preco': self.preco,
            'descricao': self.descricao,
            'categoria': self.categoria
        })
    
    @staticmethod
    def selectByVendedor(id_vendedor):
        select = mongo.db.produtos.find({'id_vendedor':id_vendedor})
        return select
    
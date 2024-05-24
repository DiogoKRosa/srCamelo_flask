from flask_pymongo import PyMongo
from bson import ObjectId, json_util
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
        self.imagem_perfil = imagem_perfil
        self.nome_fantasia = nome_fantasia
        self.forma_pagamento = forma_pagamento
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
            'forma_pagamento': self.forma_pagamento,
            'imagem_loja': self.imagem_loja
        })
        
    @staticmethod
    def trazerLogin(email):
        select = mongo.db.usuarios.find_one({'email': email})
        return select
    
    def editImagemLoja(id ,nomeImagem):
        filtro = {"_id": ObjectId(id)}
        update = {'$set':{"imagem_loja": nomeImagem}}
        mongo.db.usuarios.update_one(filtro, update)

    def editNomeFantasia( id,nomeFantasia):
        filtro = {"_id": ObjectId(id)}
        update = {'$set':{"nome_fantasia": nomeFantasia}}
        mongo.db.usuarios.update_one(filtro, update)

    def editFormaPagamento(id ,formaPagamento):
        filtro = {"_id": ObjectId(id)}
        update = {'$set':{"forma_pagamento": formaPagamento}}
        mongo.db.usuarios.update_one(filtro, update)
        
class Produto():
    def __init__(self, id_vendedor, id, nome, preco, descricao, categoria, imagem):
        self.id_vendedor = id_vendedor
        self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria
        self.imagem = imagem

    def save(self):
        mongo.db.produtos.insert_one({
            'id_vendedor': self.id_vendedor,
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'descricao': self.descricao,
            'categoria': self.categoria,
            'imagem': self.imagem
        })
    
    @staticmethod
    def selectByVendedor(id_vendedor):
        select = mongo.db.produtos.find({'id_vendedor':id_vendedor})
        return select
    
class Categoria():
    def __init__(self, categoria):
        self.categoria = categoria

    def save(self):
        mongo.db.categorias.insert_one({
            'categoria': self.categoria
        })
    
    @staticmethod
    def find():
        return mongo.db.categorias.find()

    

    
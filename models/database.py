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
    def trazerDados(id):
        return mongo.db.usuarios.find_one({'_id': ObjectId(id)})
    
    @staticmethod
    def trazerLogin(email):
        select = mongo.db.usuarios.find_one({'email': email})
        return select
    
    @staticmethod
    def trazerVendedores():
        return mongo.db.usuarios.find_one({'tipo': 'Vendedor'})
    
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
    
    def update(self, id, id_vendedor):
        mongo.db.produtos.update_one({'id': str(id), 'id_vendedor': id_vendedor},
                                       {'$set':{
                                           'nome': self.nome,
                                           'preco': self.preco,
                                           'descricao': self.descricao,
                                           'categoria': self.categoria,
                                           'imagem': self.imagem,
                                       }})
    @staticmethod
    def delete(id, id_vendedor):
        """ produto = mongo.db.produtos.find_one({'id_vendedor':id_vendedor, 'id': str(id)})
        print(produto) """
        mongo.db.produtos.delete_one({'id_vendedor':id_vendedor, 'id': str(id)})

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

class Pedido():
    def __init__(self, id, status, data, id_cliente, cliente, cliente_telefone, id_vendedor, vendedor, vendedor_telefone, total, produtos, forma_pagamento):
        self.id = id
        self.status = status
        self.data = data
        self.id_cliente = id_cliente
        self.cliente = cliente
        self.cliente_telefone = cliente_telefone
        self.id_vendedor = id_vendedor
        self.vendedor = vendedor
        self.vendedor_telefone = vendedor_telefone
        self.total = total
        self.produtos = produtos
        self.forma_pagamento = forma_pagamento
    
    def save(self):
        mongo.db.pedidos.insert_one({
            'id': self.id,
            'status': self.status,
            'data': self.data,
            'id_cliente': self.id_cliente,
            'cliente': self.cliente,
            'cliente_telefone': self.cliente_telefone,
            'id_vendedor': self.id_vendedor,
            'vendedor': self.vendedor,
            'vendedor_telefone': self.vendedor_telefone,
            'total': self.total,
            'produto': self.produtos,
            'forma_pagamento': self.forma_pagamento
        })

    @staticmethod
    def selectTodosPedidos():
        return mongo.db.pedidos.find()
    
    @staticmethod
    def selectPedidoAgora(id):
        return mongo.db.pedidos.find_one({'id': id})
    
    @staticmethod
    def selectPedido(id):
        return mongo.db.pedidos.find_one({'_id': ObjectId(id)})

    def updatePedidoforma(id, status, forma):
        filtro = {"_id": ObjectId(id)}
        update = {'$set':{'status': status,
                          'forma_pagamento': forma}}
        mongo.db.pedidos.update_one(filtro, update)
    
    def updatePedidostatus(id, status):
        filtro = {"_id": ObjectId(id)}
        update = {'$set': {'status': status}}
        mongo.db.pedidos.update_one(filtro, update)

    @staticmethod
    def selectCompras(id):
        return mongo.db.pedidos.find({'id_cliente':id, 'status':{'$ne': "Realizando"}}).sort("id", -1)
    
    @staticmethod
    def selectVendas(id):
        return mongo.db.pedidos.find({'id_vendedor':id, 'status':{'$ne':"Realizando"}}).sort("id", -1)
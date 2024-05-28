from flask import render_template, request, redirect, url_for, flash, session
from models.database import Usuario, Produto, Categoria
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from uuid import uuid4
import os

idTeste = '664414764e592646aae62ac3'
def init_app(app):
    """ @app.before_request
    def check_session():
        routes = ['index', 'cadastro_consumidor', 'cadastro_vendedor']
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        if 'user_id' not in session:
            return redirect(url_for('index')) """

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            user = Usuario.trazerLogin(email)
            print(user)
            if user and check_password_hash(user['senha'], senha):
                print('usuario_encontrado')
                session['user_id'] = json_util.dumps(user['_id'])
                print(session['user_id'])
                session['email'] = user['email']
                print(session['email'])
                if(user['tipo'] == 'Cliente'):
                    print('inicio_cliente')
                    return redirect(url_for('inicio_cliente'))
                elif(user['tipo'] == 'Vendedor'):
                    if Produto.selectByVendedor(session['user_id']):
                        print('primeiro_acesso')
                        return redirect(url_for('primeiro_acesso'))
                    else:
                        print('inicio_vendedor')
                        return redirect(url_for('inicio_vendedor'))
            else:
                flash("Usuário ou senha incorretos")
        return render_template('produtos.html')
    
    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')
    
    @app.route('/cadastro/consumidor', methods=['GET', 'POST'])
    def cadastro_consumidor():
        if request.method == 'POST':
            conferirEmail = Usuario.trazerLogin(request.form['email'])
            
            if(conferirEmail):
                flash("Já existe um cadastro com esse email")
                return redirect(url_for('cadastro_consumidor'))
            
            hashed_password = generate_password_hash(request.form['senha'], method='scrypt')
            novoUsu = Usuario(
                tipo = 'Cliente',
                nome = request.form['nome'],
                cpf = request.form['cpf'],
                email = request.form['email'],
                telefone = request.form['telefone'],
                senha = hashed_password,
                pais = request.form['pais'],
                uf = request.form['uf'],
                cidade = request.form['cidade'],
                imagem = ''
            )
            novoUsu.save()
            return redirect(url_for('index'))

        return render_template('cadastro_consumidor.html')
    
    @app.route('/cadastro/vendedor', methods=['GET', 'POST'])
    def cadastro_vendedor():
        if request.method == 'POST':
            conferirEmail = Usuario.trazerLogin(request.form['email'])
            
            if(conferirEmail):
                flash("Já existe um cadastro com esse email")
                return redirect(url_for('cadastro_vendedor'))
            
            hashed_password = generate_password_hash(request.form['senha'], method='scrypt')
            novoUsu = Usuario(
                tipo = 'Vendedor',
                nome = request.form['nome'],
                cpf = request.form['cpf'],
                email = request.form['email'],
                telefone = request.form['telefone'],
                senha = hashed_password,
                pais = request.form['pais'],
                uf = request.form['uf'],
                cidade = request.form['cidade'],
                imagem = ''
            )
            novoUsu.save()
            return redirect(url_for('index'))
        return render_template('cadastro_vendedor.html')
    
    @app.route('/inicio/cliente')
    def inicio_cliente():
        return render_template('inicio_consumidor.html')
    
    @app.route('/inicio/vendedor')
    def inicio_vendedor():
        return render_template('inicio_vendedor.html')
    
    @app.route('/primeiro-acesso', methods=['GET', 'POST'])
    def primeiro_acesso():
        if request.method == 'POST':
            imagem = request.files['imagem_loja']
            nomeImagem = str(uuid4())
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))

            Usuario.editImagemLoja(idTeste, nomeImagem)
            Usuario.editNomeFantasia(idTeste, request.form['nome_fantasia'])
            Usuario.editFormaPagamento(idTeste, request.form.getlist('forma_pagamento'))
            return redirect(url_for('produtos'))    
        return render_template('primeiro_acesso.html')
    
    @app.route('/primeiro-acesso/produtos', methods=['GET', 'POST'])
    def produtos():
        produtos = list(Produto.selectByVendedor(idTeste))
        categorias = list(Categoria.find())
        idBanco = [int(res['id']) for res in produtos]
        
        if request.method == 'POST':
            #Traz os Ids dos produtos do forms
            qtde = int(request.form['qtde'])
            i=0
            idPost =[]
            while i<=qtde:
                try:
                    idPost.append(int(request.form[f'id_produto-{i}']))
                    i+=1
                except:
                    i+=1

            #Separa os ids em três lista diferentes [adicionar, atualizar e deletar]
            adicionar = list(filter(lambda x: x not in idBanco, idPost))
            atualizar = list(filter(lambda x: x in idBanco, idPost))
            deletar = list(filter(lambda x: x not in idPost, idBanco))
            print(adicionar, atualizar, deletar)
            #Cadastra novo produto
            for x in adicionar:
                imagem = request.files[f'imagem_produto-{x}']
                nomeImagem = str(uuid4())
                imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))
                novo = Produto(id_vendedor=idTeste, 
                               id=request.form[f'id_produto-{x}'],
                               nome=request.form[f'nome_produto-{x}'],
                               preco=request.form[f'preco_produto-{x}'],
                               descricao=request.form[f'descricao_produto-{x}'],
                               categoria=request.form.get(f'categoria_produto-{x}'),
                               imagem=nomeImagem)
                novo.save()
            
            #Atualiza produto
            for x in atualizar:
                reg = list(filter(lambda y: y['id'] == str(x), produtos))
                imagem = request.files[f'imagem_produto-{x}']
                
                if imagem.filename == '':
                    nomeImagem = reg[0]['imagem']
                else:
                    nomeImagem = str(uuid4())
                    imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))

                att = Produto(id_vendedor=idTeste,
                              id=request.form[f'id_produto-{x}'],
                              nome=request.form[f'nome_produto-{x}'],
                              preco=request.form[f'preco_produto-{x}'],
                              descricao=request.form[f'descricao_produto-{x}'],
                              categoria=request.form.get(f'categoria_produto-{x}'),
                              imagem=nomeImagem)
                Produto.update(att, x, idTeste)
            
            
            #Deleta produto do banco
            for x in deletar:
                Produto.delete(x, idTeste)
            return redirect(url_for('inicio_vendedor'))

        return render_template('produtos.html', produtos=produtos, categorias=categorias)
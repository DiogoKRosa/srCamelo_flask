from flask import render_template, request, redirect, url_for, flash, session
from models.database import Usuario, Produto, Categoria, Pedido
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util, ObjectId
from uuid import uuid4
import os
from datetime import datetime

def init_app(app):
    @app.before_request
    def check_session():
        routes = ['index', 'cadastro','cadastro_consumidor', 'cadastro_vendedor']
        if request.endpoint in routes or request.path.startswith('/static/'):
            return
        if 'user_id' not in session:
            return redirect(url_for('index'))

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            user = Usuario.trazerLogin(email)
            #print(user)
            if user and check_password_hash(user['senha'], senha):
                #print('usuario_encontrado')
                oid = str(user['_id'])
                #print(oid)
                session['user_id'] = oid
                #print(session['user_id'])
                session['email'] = user['email']
                #print(session['email'])
                session['nome'] = user['nome']
                session['telefone'] = user['telefone']
                if(user['tipo'] == 'Cliente'):
                    print('inicio_cliente')
                    return redirect(url_for('inicio_cliente'))
                elif(user['tipo'] == 'Vendedor'):
                    if Produto.selectByVendedor(session['user_id']):
                        print('inicio_vendedor')
                        return redirect(url_for('inicio_vendedor'))
                    else:
                        print('primeiro_acesso')
                        return redirect(url_for('primeiro_acesso'))
                        
            else:
                flash("Usuário ou senha incorretos")
        return render_template('index.html')
    
    @app.route('/sair')
    def sair():
        session.clear()
        return redirect(url_for('index'))
    
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
                imagem_perfil= '',
                nome_fantasia = request.form['nome'],
                forma_pagamento = [],
                imagem_loja = ''
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
                imagem_perfil= '',
                nome_fantasia = request.form['nome'],
                forma_pagamento = [],
                imagem_loja = ''
            )
            novoUsu.save()
            return redirect(url_for('index'))
        return render_template('cadastro_vendedor.html')
    
    @app.route('/inicio/cliente')
    def inicio_cliente():
        return render_template('inicio_consumidor.html')
    
    @app.route('/vendedor/<id>', methods=['GET', 'POST'])
    def pagina_vendedor(id=None):
        vendedor = Usuario.trazerDados(id)
        #print(vendedor)
        produtos = Produto.selectByVendedor(id)
        #print(produtos)
        return render_template('pagina_vendedor.html',  titulo=vendedor['nome'], vendedor=vendedor, produtos=produtos)
    
    @app.route('/vendedor/<id>/pedido', methods=['GET', 'POST'])
    def pedido(id=None):
        vendedor = Usuario.trazerDados(id)
        produtos = Produto.selectByVendedor(id)

        if request.method == 'POST':
            lista_pedido = []
            for produto in produtos:
                id=produto['id']
                id_produto = request.form[f'produto-id-{id}']
                nome_produto = request.form[f'produto-nome-{id}']
                qtde_produto = request.form[f'produto-qtde-{id}']
                preco_produto = request.form[f'produto-preco-{id}']
                if int(qtde_produto) == 0:
                    continue
                else:
                    lista_pedido.append({'id':id_produto, 'nome':nome_produto, 'qtde':qtde_produto,'preco':preco_produto})
            dataagora = datetime.now()
            select = Pedido.selectTodosPedidos()
            count = 0
            for pedido in select:
                count = count + 1
            print(count)
            novo = Pedido(
                id = count,
                status = 'Realizando',
                data = dataagora.strftime('%d/%m/%Y'),
                id_cliente = session['user_id'],
                cliente = session['nome'],
                cliente_telefone = session['telefone'],
                id_vendedor = str(vendedor['_id']),
                vendedor = vendedor['nome'],
                vendedor_telefone = vendedor['telefone'],
                total = request.form['total-pedido'],
                produtos = lista_pedido,
                forma_pagamento = 'Pendente'
            )
            novo.save()

            idPedido = Pedido.selectPedidoAgora(count)
            return redirect(url_for('pagamento', id=vendedor['_id'], idPedido = idPedido['_id']))
        
        return render_template('pedido.html', titulo=vendedor['nome'], vendedor=vendedor, produtos=produtos)
    
    @app.route('/vendedor/<id>/pagamento/<idPedido>', methods=['GET', 'POST'])
    def pagamento(id=None, idPedido=None):
        idPedido = '665da76dc2a7a806ff3e0bb0'
        pedido = Pedido.selectPedido(idPedido)
        return render_template('pagamento.html', titulo='Pagamento', pedido=pedido)
    
    @app.route('/vendedor/<id>/pagamento/<idPedido>/pix', methods=['GET', 'POST'])
    def pix(id=None, idPedido=None):
        vendedor = Usuario.trazerDados(id)
        pedido = Pedido.selectPedido(idPedido)
        return render_template('pix.html', vendedor=vendedor, pedido=pedido)
    
    @app.route('/finalizado/<idPedido>/<forma>', methods=['GET', 'POST'])
    def atualizarPagamento(id=None, idPedido=None, forma=None):
        pedido = Pedido.updatePedidoforma(id=idPedido, status='Pendente', forma=forma)
        return render_template('finalizado.html')
    
    @app.route('/inicio/vendedor')
    def inicio_vendedor():
        vendedor = Usuario.trazerDados(session['user_id'])
        #print(vendedor)
        produtos = Produto.selectByVendedor(session['user_id'])
        #print(produtos)
        return render_template('inicio_vendedor.html', titulo=vendedor['nome'], vendedor=vendedor, produtos=produtos)
    
    @app.route('/dados/vendedor')
    def dados_vendedor():
        return render_template('dados_vendedor.html')

    @app.route('/primeiro-acesso', methods=['GET', 'POST'])
    def primeiro_acesso():
        if request.method == 'POST':
            imagem = request.files['imagem_loja']
            nomeImagem = str(uuid4())
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nomeImagem))

            Usuario.editImagemLoja(session['user_id'], nomeImagem)
            Usuario.editNomeFantasia(session['user_id'], request.form['nome_fantasia'])
            Usuario.editFormaPagamento(session['user_id'], request.form.getlist('forma_pagamento'))
            return redirect(url_for('produtos'))    
        return render_template('primeiro_acesso.html', titulo="Foto do Perfil")
    
    @app.route('/produtos', methods=['GET', 'POST'])
    @app.route('/primeiro-acesso/produtos', methods=['GET', 'POST'])
    def produtos():
        produtos = list(Produto.selectByVendedor(session['user_id']))
        
        try:
            Pid = produtos[-1]['id']
        except:
            Pid = 0

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
                novo = Produto(id_vendedor=session['user_id'], 
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

                att = Produto(id_vendedor=session['user_id'],
                              id=request.form[f'id_produto-{x}'],
                              nome=request.form[f'nome_produto-{x}'],
                              preco=request.form[f'preco_produto-{x}'],
                              descricao=request.form[f'descricao_produto-{x}'],
                              categoria=request.form.get(f'categoria_produto-{x}'),
                              imagem=nomeImagem)
                Produto.update(att, x, session['user_id'])
            
            
            #Deleta produto do banco
            for x in deletar:
                Produto.delete(x, session['user_id'])
            return redirect(url_for('inicio_vendedor'))
        
        return render_template('produtos.html', produtos=produtos, categorias=categorias, Pid=Pid)
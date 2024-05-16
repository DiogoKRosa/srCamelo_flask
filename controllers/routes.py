from flask import render_template, request, redirect, url_for, flash, session
from models.database import Usuario
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util

def init_app(app):
    @app.before_request
    def check_session():
        routes = ['index', 'cadastro_consumidor', 'cadastro_vendedor']
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
                    print('inicio_vendedor')
                    return redirect(url_for('inicio_vendedor'))
            else:
                flash("Usuário ou senha incorretos")
        return render_template('index.html')
    
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
    
    @app.route('/primeiro_acesso')
    def primeiro_acesso():
        return render_template('primeiro_acesso.html')

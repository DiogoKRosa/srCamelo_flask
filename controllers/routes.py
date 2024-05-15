from flask import render_template, request, redirect, url_for
from models.database import Usuario
from markupsafe import Markup
from werkzeug.security import generate_password_hash, check_password_hash

def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')
    
    @app.route('/cadastro/consumidor', methods=['GET', 'POST'])
    def cadastro_consumidor():
        if request.method == 'POST':
            conferirEmail = Usuario.trazerLogin(request.form['email'])
            
            if(conferirEmail):
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
    
    @app.route('/cadastro/vendedor')
    def cadastro_vendedor():
        return render_template('cadastro_vendedor.html')
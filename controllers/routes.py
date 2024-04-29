from flask import render_template

def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')
    
    @app.route('/cadastro/consumidor')
    def cadastro_consumidor():
        return render_template('cadastro_consumidor.html')
    
    @app.route('/cadastro/vendedor')
    def cadastro_vendedor():
        return render_template('cadastro_vendedor.html')
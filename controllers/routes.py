from flask import render_template

def init_app(app):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/cadastro')
    def cadastro():
        return render_template('cadastro.html')
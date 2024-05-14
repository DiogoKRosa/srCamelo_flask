from flask import render_template, request

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
            print(request.form['nome'])
            print(request.form['cpf'])
            print(request.form['email'])
            print(request.form['telefone'])
            print(request.form['senha'])
            print(request.form['pais'])
            print(request.form['uf'])
            print(request.form['cidade'])
        return render_template('cadastro_consumidor.html')
    
    @app.route('/cadastro/vendedor')
    def cadastro_vendedor():
        return render_template('cadastro_vendedor.html')
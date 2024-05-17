#Importando as denpendências que serão utilizadas
from flask import Flask, render_template
from controllers import routes
from models.database import mongo, Usuario, Produto

# Carregando o Flask na variável app
app = Flask(__name__, template_folder='views')
routes.init_app(app)

# Define a conecão do banco e o nome
app.config['MONGO_URI'] = 'mongodb://localhost:27017/srcamelo'

# Definindo a secret key para as flash messages
app.config['SECRET_KEY'] = 'srcamelo'

# Define o tempo de duração da sessão
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

#Define pasta que receberá arquivos de upload
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    mongo.init_app(app=app)
    with app.app_context():
        if 'usuarios' not in mongo.db.list_collection_names():
            usuario = Usuario(
                nome = '',
                cpf = '',
                email = '',
                telefone = '',
                senha = '',
                pais = '',
                uf = '',
                cidade = '',
                imagem_perfil = '',
                nome_fantasia = '',
                imagem_loja = ''
            )
            usuario.save()

        if 'produtos' not in mongo.db.list_collection_names():
            produto = Produto(
                id_vendedor='',
                nome='',
                preco=0,
                descricao='',
                categoria=''
            )
            produto.save()

    app.run(host='localhost', port=5000, debug=True)
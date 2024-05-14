#Importando as denpendências que serão utilizadas
from flask import Flask, render_template
from controllers import routes
from models.database import mongo, Usuario

# Carregando o Flask na variável app
app = Flask(__name__, template_folder='views')
routes.init_app(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/games'

# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    mongo.init_app(app=app)
    with app.app_context():
        if 'usuarios' not in mongo.db.list_collection_names():
            usuario = Usuario(
                tipo = '',
                nome = ''
            )
            usuario.save()

    app.run(host='localhost', port=5000, debug=True)
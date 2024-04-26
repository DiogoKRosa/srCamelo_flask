#Importando as denpendências que serão utilizadas
from flask import Flask, render_template
from controllers import routes

# Carregando o Flask na variável app
app = Flask(__name__, template_folder='views')

routes.init_app(app)

# Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_cors import CORS

# Criar a aplicação Flask
app = Flask(__name__)
CORS(app)

# Definir pasta para templates e arquivos estáticos
app.template_folder = "templates"
app.static_folder = "static"

# Configuração do banco de dados
database_url = os.environ.get("DATABASE_URL")
if database_url:
    print(f"Conectando ao banco de dados: {database_url}")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    print("AVISO: Variável DATABASE_URL não encontrada. Usando SQLite local.")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meme_videos.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar o banco de dados
db.init_app(app)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()
    
    # Adicionar alguns subreddits populares, se necessário
    from models import Subreddit
    
    # Verifica se já existem subreddits no banco antes de adicionar
    if Subreddit.query.count() == 0:
        popular_subreddits = [
            {"name": "memes", "category": "Humor", "description": "Memes gerais e populares"},
            {"name": "dankmemes", "category": "Humor", "description": "Memes irreverentes e populares"},
            {"name": "wholesomememes", "category": "Humor", "description": "Memes wholesome e positivos"},
            {"name": "ProgrammerHumor", "category": "Tecnologia", "description": "Humor para programadores"},
            {"name": "funny", "category": "Humor", "description": "Conteúdo engraçado geral"},
            {"name": "cats", "category": "Animais", "description": "Fotos e vídeos de gatos"},
            {"name": "dogs", "category": "Animais", "description": "Fotos e vídeos de cachorros"},
            {"name": "aww", "category": "Animais", "description": "Conteúdo fofo de animais"},
            {"name": "me_irl", "category": "Humor", "description": "Memes relatáveis"},
            {"name": "gaming", "category": "Games", "description": "Comunidade geral de jogos"}
        ]
        
        for subreddit_data in popular_subreddits:
            subreddit = Subreddit(**subreddit_data)
            db.session.add(subreddit)
        
        db.session.commit()
        print("Subreddits populares adicionados ao banco de dados!")
    
# Importar todas as rotas da web_app
from web_app import *
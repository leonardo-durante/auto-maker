from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    """Modelo para armazenar informações sobre os vídeos gerados"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    subreddit = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    feed_type = db.Column(db.String(20), nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # duração em segundos
    size = db.Column(db.Integer, nullable=True)  # tamanho em bytes
    post_count = db.Column(db.Integer, nullable=True)  # número de posts incluídos
    
    def __repr__(self):
        return f"<Video {self.filename} - r/{self.subreddit}>"
    
    def size_format(self):
        """Retorna o tamanho do arquivo em formato legível"""
        if not self.size:
            return "Desconhecido"
            
        size_bytes = self.size
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def creation_date_formatted(self):
        """Retorna a data de criação formatada"""
        if self.created_at:
            return self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        return "Data desconhecida"

class Subreddit(db.Model):
    """Modelo para armazenar informações sobre os subreddits populares"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    subscribers = db.Column(db.Integer, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Subreddit r/{self.name}>"
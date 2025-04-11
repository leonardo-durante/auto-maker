import os
import json
import glob
from datetime import datetime
import urllib.parse
from flask import render_template, send_from_directory, jsonify, request, redirect, url_for
from app import app
from models import db, Video, Subreddit

# Adiciona filtro para URL encode
@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    return urllib.parse.quote_plus(s)

# Carrega configuração
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    return {
        "subreddits": ["memes", "dankmemes", "wholesomememes"],
        "posts_limit": 10,
        "image_duration": 3,
        "run_interval_minutes": 60,
        "fps": 30,
        "add_music": True,
        "feed_types": ["hot", "new", "top", "rising"]
    }

@app.route('/')
def index():
    """Página inicial que lista todos os vídeos gerados"""
    # Carrega configuração
    config = load_config()
    
    # Busca subreddits do banco de dados para sugestões
    db_subreddits = Subreddit.query.all()
    
    # Verifica se há vídeos no banco de dados
    db_videos = Video.query.order_by(Video.created_at.desc()).all()
    
    # Se não houver vídeos no banco, importa os arquivos de vídeo existentes
    if not db_videos:
        # Encontra todas as pastas de saída
        output_folders = sorted(glob.glob("output_*"), reverse=True)
        
        # Coleta informações sobre os vídeos
        for folder in output_folders:
            try:
                # Extrai informações do nome da pasta
                folder_name = os.path.basename(folder)
                parts = folder_name.split('_')
                if len(parts) >= 3:
                    subreddit = parts[1]
                    timestamp_str = '_'.join(parts[2:])
                    
                    # Converte timestamp para um objeto datetime
                    try:
                        timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    except ValueError:
                        timestamp = datetime.utcnow()
                    
                    # Procura por arquivos de vídeo no diretório
                    video_files = glob.glob(f"{folder}/*.mp4")
                    for video_file in video_files:
                        video_name = os.path.basename(video_file)
                        
                        # Verifica se o vídeo já existe no banco
                        existing_video = Video.query.filter_by(path=video_file).first()
                        if not existing_video:
                            # Obtém o tamanho do arquivo
                            try:
                                size_bytes = os.path.getsize(video_file)
                            except:
                                size_bytes = 0
                            
                            # Cria um novo registro de vídeo
                            video = Video(
                                filename=video_name,
                                path=video_file,
                                subreddit=subreddit,
                                created_at=timestamp,
                                size=size_bytes
                            )
                            db.session.add(video)
            except Exception as e:
                print(f"Erro ao processar pasta {folder}: {str(e)}")
        
        # Salva as alterações no banco de dados
        try:
            db.session.commit()
            print("Vídeos existentes importados para o banco de dados!")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar vídeos no banco: {str(e)}")
        
        # Busca os vídeos novamente
        db_videos = Video.query.order_by(Video.created_at.desc()).all()
    
    return render_template("index.html", videos=db_videos, config=config, subreddits=db_subreddits)

@app.route('/video/<path:video_path>')
def serve_video(video_path):
    """Serve o arquivo de vídeo"""
    # Divide o caminho para obter diretório e nome do arquivo
    directory = os.path.dirname(video_path)
    filename = os.path.basename(video_path)
    
    return send_from_directory(directory, filename, as_attachment=request.args.get('download') == 'true')

@app.route('/run', methods=['POST'])
def run_generation():
    """Executa o gerador de vídeos com as configurações especificadas"""
    import subprocess
    import json
    
    # Obtém os parâmetros do formulário
    subreddit = request.form.get('subreddit', '')
    limit = request.form.get('limit', '10')
    feed_type = request.form.get('feed_type', 'hot')
    duration = request.form.get('duration', '3')
    
    # Se o subreddit foi especificado, atualiza o arquivo de configuração
    if subreddit:
        try:
            # Carrega a configuração atual
            config = load_config()
            
            # Verifica se este é um subreddit válido
            if subreddit.startswith('@'):
                # Usando um subreddit da biblioteca pré-definida
                category = subreddit[1:]
                db_subreddits = Subreddit.query.filter_by(category=category).all()
                if db_subreddits:
                    subreddits = [sub.name for sub in db_subreddits]
                    config['subreddits'] = subreddits
                    print(f"Usando subreddits da categoria {category}: {subreddits}")
                else:
                    # Fallback para subreddits padrão se a categoria não for encontrada
                    config['subreddits'] = ["memes", "dankmemes", "wholesomememes"]
                    print(f"Categoria {category} não encontrada, usando subreddits padrão")
            elif ',' in subreddit:
                # Permite múltiplos subreddits separados por vírgula
                subreddits = [s.strip() for s in subreddit.split(',')]
                config['subreddits'] = subreddits
            else:
                # Um único subreddit
                config['subreddits'] = [subreddit]
            
            # Atualiza as configurações
            config['posts_limit'] = int(limit)
            config['feed_types'] = [feed_type]
            config['image_duration'] = int(duration)
            
            # Salva a configuração de volta ao arquivo
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
                
            # Adiciona mensagem de log
            print(f"Configuração atualizada com subreddits: {config['subreddits']}")
        except Exception as e:
            print(f"Erro ao atualizar configuração: {str(e)}")
    
    # Executar o script run.py --once com os novos parâmetros
    cmd = ["python", "run.py", "--once"]
    
    # Executa o comando em segundo plano
    subprocess.Popen(cmd)
    
    return redirect(url_for('index'))

def get_file_size(file_path):
    """Obtém o tamanho do arquivo em formato legível"""
    try:
        size_bytes = os.path.getsize(file_path)
        
        # Converte para um formato legível
        if size_bytes < 1024:
            return f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    except:
        return "Desconhecido"

@app.route('/api/videos')
def get_videos():
    """API para obter a lista de vídeos em formato JSON"""
    # Busca vídeos do banco de dados
    db_videos = Video.query.order_by(Video.created_at.desc()).all()
    videos = []
    
    for video in db_videos:
        video_info = {
            "id": video.id,
            "path": video.path,
            "name": video.filename,
            "subreddit": video.subreddit,
            "date": video.creation_date_formatted(),
            "size": video.size_format(),
            "feed_type": video.feed_type or "desconhecido",
            "post_count": video.post_count or 0
        }
        videos.append(video_info)
    
    return jsonify(videos)

@app.route('/api/subreddits')
def get_subreddits():
    """API para obter a lista de subreddits salvos"""
    subreddits = Subreddit.query.all()
    result = []
    
    for sub in subreddits:
        result.append({
            "id": sub.id,
            "name": sub.name,
            "description": sub.description,
            "category": sub.category,
            "subscribers": sub.subscribers
        })
    
    return jsonify(result)

if __name__ == '__main__':
    # Certifique-se de que os diretórios necessários existem
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    
    # Inicia o servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
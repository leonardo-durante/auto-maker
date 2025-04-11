from RedditBot import RedditBot
import os
import shutil
import json
import logging
import datetime
import random
import requests
from moviepy.editor import *

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Carregar configurações do arquivo config.json
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {str(e)}")
        # Configurações padrão se não for possível carregar o arquivo
        return {
            "subreddits": ["memes"],
            "posts_limit": 10,
            "image_duration": 3,
            "run_interval_minutes": 60,
            "fps": 30,
            "add_music": True
        }

# Função para baixar músicas de fundo de domínio público
def download_background_music():
    # Criar pasta de música se não existir
    if not os.path.exists("music"):
        os.makedirs("music")
        logger.info("Pasta de música criada")
    
    # URLs de músicas de background de domínio público
    music_urls = [
        "https://www.chosic.com/wp-content/uploads/2021/05/Lofi-Study.mp3",
        "https://www.chosic.com/wp-content/uploads/2020/05/The-Epic-Hero-Epic-Cinematic-Keys-of-Moon-Music.mp3",
        "https://www.chosic.com/wp-content/uploads/2021/05/purrple-cat-equinox.mp3"
    ]
    
    # Tentar baixar cada música
    for i, url in enumerate(music_urls):
        music_path = f"music/background_{i}.mp3"
        
        # Verificar se o arquivo já existe
        if os.path.exists(music_path):
            logger.info(f"Música {i} já existe, pulando download")
            continue
        
        try:
            logger.info(f"Baixando música de fundo {i} de {url}")
            response = requests.get(url, timeout=30)
            with open(music_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Música de fundo {i} salva em {music_path}")
        except Exception as e:
            logger.error(f"Erro ao baixar música {i}: {str(e)}")
    
    # Retornar uma música aleatória da pasta
    music_files = [os.path.join("music", f) for f in os.listdir("music") 
                  if f.endswith((".mp3", ".ogg"))]
    
    if music_files:
        selected_music = random.choice(music_files)
        logger.info(f"Música selecionada: {selected_music}")
        return selected_music
    else:
        logger.warning("Nenhuma música de fundo disponível")
        return None

def create_video(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True):
    '''Cria vídeo a partir das imagens salvas na pasta'''
    
    image_folder='images'
    if not os.path.exists(image_folder):
        logger.error(f"Pasta de imagens {image_folder} não existe")
        return False
    
    # Verificar se existem imagens na pasta
    image_files = [os.path.join(image_folder, img) 
                  for img in os.listdir(image_folder) 
                  if img.endswith(".jpg")]
    
    if not image_files:
        logger.error(f"Nenhuma imagem encontrada na pasta {image_folder}")
        return False
    
    logger.info(f"Criando vídeo com {len(image_files)} imagens, {duration_per_image}s por imagem")
    
    try:
        # Criar os frames do vídeo
        frames = [ImageClip(f, duration=duration_per_image) for f in image_files]
        clip = concatenate_videoclips(frames, method='compose')
        
        # Adicionar música de fundo foi desativado temporariamente
        # porque está causando erros
        add_music = False
        
        # Criar pasta de saída se fornecida
        video_path = f"{name}.mp4"
        if output_folder:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            video_path = os.path.join(output_folder, f"{name}_memes.mp4")
        
        # Gerar o vídeo
        clip.write_videofile(video_path, fps=fps)
        logger.info(f"Vídeo salvo em {video_path}")
        
        # Limpar a pasta de imagens
        shutil.rmtree(image_folder)
        logger.info(f"Pasta de imagens {image_folder} limpa")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao criar vídeo: {str(e)}")
        return False

def main():
    # Carregar configurações
    config = load_config()
    subreddits = config.get("subreddits", ["memes"])
    posts_limit = config.get("posts_limit", 10)
    image_duration = config.get("image_duration", 3)
    fps = config.get("fps", 30)
    add_music = config.get("add_music", True)
    feed_types = config.get("feed_types", ["hot"])
    
    # Inicializar o bot do Reddit
    try:
        reddit = RedditBot()
    except Exception as e:
        logger.error(f"Erro ao inicializar RedditBot: {str(e)}")
        return
    
    # Data/hora atual para organização das pastas
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Processar cada subreddit
    for subreddit in subreddits:
        # Escolher um tipo de feed aleatoriamente para ter variedade
        feed_type = random.choice(feed_types)
        logger.info(f"Processando subreddit: {subreddit}, feed: {feed_type}")
        
        # Criar pasta de saída para este subreddit
        output_folder = f"output_{subreddit}_{timestamp}"
        os.makedirs(output_folder, exist_ok=True)
        
        # Baixar imagens do subreddit usando o feed selecionado
        if reddit.get_images(sub_name=subreddit, limit=posts_limit, feed_type=feed_type):
            # Criar vídeo para este subreddit
            create_video(
                duration_per_image=image_duration,
                output_folder=output_folder,
                name=subreddit,
                fps=fps,
                add_music=add_music
            )
            
            # Registrar vídeo no banco de dados
            try:
                from app import app, db
                from models import Video
                
                video_path = f"{output_folder}/{subreddit}_memes.mp4"
                video_size = os.path.getsize(video_path) if os.path.exists(video_path) else 0
                
                with app.app_context():
                    # Cria um novo registro no banco de dados
                    video = Video(
                        filename=f"{subreddit}_memes.mp4",
                        path=video_path,
                        subreddit=subreddit,
                        created_at=datetime.datetime.now(),
                        feed_type=feed_type,
                        duration=image_duration * posts_limit,
                        size=video_size,
                        post_count=posts_limit
                    )
                    db.session.add(video)
                    db.session.commit()
                    logger.info(f"Vídeo registrado no banco de dados com ID: {video.id}")
            except Exception as db_error:
                logger.error(f"Erro ao registrar vídeo no banco de dados: {str(db_error)}")
        else:
            logger.warning(f"Falha ao obter imagens do subreddit {subreddit} usando feed {feed_type}")
    
    logger.info("Processamento concluído para todos os subreddits")

if __name__=='__main__':
    main()
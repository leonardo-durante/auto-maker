# Este arquivo serve dois propósitos:
# 1. Executar o gerador de vídeos quando chamado diretamente
# 2. Fornecer o app Flask para o Gunicorn

# Importação para servidor web (usado pelo Gunicorn)
from web_app import app

# Importações para geração de vídeos
from RedditBot import RedditBot
import os
import shutil
import logging
from moviepy.editor import *

# Configuração do logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_video(duration_per_image=10, name='video', fps=30):
    '''creates video from the images saved in the folder'''

    # creating video
    image_folder='images'
    try:
        if not os.path.exists(image_folder):
            logger.error(f"Pasta {image_folder} não encontrada")
            return False
            
        image_files = [os.path.join(image_folder,img)
                        for img in os.listdir(image_folder)
                        if img.endswith(".jpg")]
                        
        if not image_files:
            logger.error("Nenhuma imagem encontrada na pasta")
            return False
            
        frames = [ImageClip(f, duration = duration_per_image) for f in image_files]
        clip = concatenate_videoclips(frames, method='compose')
        clip.write_videofile(f"{name}.mp4", fps = fps)

        shutil.rmtree(image_folder) # deletes the images folder as no longer useful
        return True
    except Exception as e:
        logger.error(f"Erro ao criar vídeo: {str(e)}")
        return False

def main():
    try:
        reddit = RedditBot()
        if reddit.get_images():
            create_video()
        else:
            logger.error("Falha ao obter imagens do Reddit")
    except Exception as e:
        logger.error(f"Erro ao executar o script: {str(e)}")

# O Gunicorn procura pelo objeto 'app' neste módulo
# O if name==main só será executado quando o script for chamado diretamente

if __name__=='__main__':
    main()

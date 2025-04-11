# Exemplos de Uso do Gerador de Vídeos de Memes

Este documento fornece exemplos práticos de como usar o Gerador de Vídeos de Memes do Reddit para diferentes casos de uso, desde a geração básica de vídeos até configurações avançadas.

## Índice

1. [Exemplos Básicos](#exemplos-básicos)
2. [Casos de Uso Comuns](#casos-de-uso-comuns)
3. [Configurações Avançadas](#configurações-avançadas)
4. [Exemplos de Integração](#exemplos-de-integração)
5. [Exemplos de Personalização](#exemplos-de-personalização)

## Exemplos Básicos

### Gerar um Vídeo de Memes Simples

O modo mais básico de usar a aplicação:

```bash
# Executar uma vez com as configurações padrão
python run.py --once
```

Isso irá:
1. Baixar 10 imagens dos subreddits definidos no `config.json`
2. Criar um vídeo para cada subreddit
3. Adicionar música de fundo
4. Salvar os vídeos em pastas com timestamp

### Usar a Interface Web

Para iniciar a interface web:

```bash
# Iniciar o servidor web
python run_flask.py
# ou para produção
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Em seguida, acesse `http://localhost:5000` no seu navegador para:
- Ver vídeos gerados anteriormente
- Configurar e gerar novos vídeos
- Compartilhar vídeos em redes sociais

### Configurar Execução Periódica

Para configurar o agendador que executará o gerador periodicamente:

```bash
# Iniciar o agendador
python run.py --scheduler
```

O intervalo entre execuções é controlado pelo parâmetro `run_interval_minutes` no `config.json`.

## Casos de Uso Comuns

### Gerar Vídeos de Diferentes Tipos de Memes

Para gerar vídeos de diferentes tipos de subreddits:

1. Edite o arquivo `config.json`:
   ```json
   {
     "subreddits": ["ProgrammerHumor", "sciencememes", "historymemes"],
     "posts_limit": 10,
     "image_duration": 3,
     "run_interval_minutes": 60,
     "fps": 30,
     "add_music": true,
     "feed_types": ["hot", "new", "top", "rising"]
   }
   ```

2. Execute o gerador:
   ```bash
   python run.py --once
   ```

### Criar um Vídeo Mais Longo

Para criar um vídeo mais longo com mais posts:

1. Edite o arquivo `config.json`:
   ```json
   {
     "subreddits": ["memes"],
     "posts_limit": 30,
     "image_duration": 3,
     "run_interval_minutes": 60,
     "fps": 30,
     "add_music": true,
     "feed_types": ["hot"]
   }
   ```

2. Execute o gerador:
   ```bash
   python run.py --once
   ```

### Criar um Vídeo com Conteúdo Mais Recente

Para criar um vídeo com posts mais recentes:

1. Edite o arquivo `config.json`:
   ```json
   {
     "subreddits": ["memes"],
     "posts_limit": 10,
     "image_duration": 3,
     "run_interval_minutes": 60,
     "fps": 30,
     "add_music": true,
     "feed_types": ["new"]
   }
   ```

2. Execute o gerador através da interface web, selecionando "new" como tipo de feed.

### Gerar Vídeos sem Música

Para gerar vídeos sem música de fundo:

1. Edite o arquivo `config.json`:
   ```json
   {
     "add_music": false
   }
   ```

2. Ou na interface web, desmarque a opção correspondente (se disponível).

## Configurações Avançadas

### Personalizar a Duração de Cada Imagem

Para criar um vídeo com durações de imagem diferentes:

1. Através da interface web:
   - Selecione o valor desejado no campo "Duração por Imagem"

2. Ou editando o `config.json`:
   ```json
   {
     "image_duration": 5
   }
   ```

### Usar Subreddits de Nicho

Para usar subreddits mais específicos:

1. Edite o arquivo `config.json`:
   ```json
   {
     "subreddits": ["wholesomememes", "rarepuppers", "EarthPorn", "oddlysatisfying"]
   }
   ```

2. Ou use a interface web para inserir múltiplos subreddits separados por vírgula:
   ```
   wholesomememes, rarepuppers, EarthPorn, oddlysatisfying
   ```

### Personalizar a Qualidade do Vídeo

Para ajustar a qualidade do vídeo gerado, modifique o código em `meme_generator.py`:

```python
# Para qualidade mais alta
clip.write_videofile(
    output_file,
    fps=fps,
    codec='libx264',
    preset='slow',
    bitrate='2000k'
)

# Para arquivo menor/qualidade mais baixa
clip.write_videofile(
    output_file,
    fps=fps,
    codec='libx264',
    preset='ultrafast',
    bitrate='500k'
)
```

### Combinar Diferentes Tipos de Feed

Para incluir posts de diferentes tipos de feed em uma única execução:

1. Edite o arquivo `config.json`:
   ```json
   {
     "feed_types": ["hot", "top", "rising"]
   }
   ```

2. Execute várias vezes manualmente, selecionando diferentes tipos de feed em cada execução.

## Exemplos de Integração

### Integrar com Sistema de Postagem Automática em Redes Sociais

Este exemplo mostra como você pode integrar o gerador com um script para postar automaticamente os vídeos em redes sociais:

```python
import os
import glob
import subprocess
import time
from datetime import datetime

# Primeiro, gera um novo vídeo
subprocess.run(["python", "run.py", "--once"], check=True)

# Encontra o vídeo mais recente
latest_folder = max(glob.glob("output_*"), key=os.path.getctime)
video_files = glob.glob(f"{latest_folder}/*.mp4")

if video_files:
    latest_video = max(video_files, key=os.path.getctime)
    
    # Aqui você usaria uma biblioteca como tweepy, facebook-sdk, etc.
    # para postar o vídeo na plataforma desejada
    print(f"Posting video {latest_video} to social media...")
    
    # Exemplo com tweepy (Twitter)
    """
    import tweepy
    
    # Autenticar
    auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")
    api = tweepy.API(auth)
    
    # Postar vídeo
    media = api.media_upload(latest_video)
    api.update_status(
        status=f"Memes do dia! #{datetime.now().strftime('%d%m%Y')} #memes #funny",
        media_ids=[media.media_id_string]
    )
    """
```

### Integrar com Dashboard de Análise

Este exemplo mostra como você poderia extrair dados para um dashboard de análise:

```python
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Conectar ao banco de dados (se estiver usando SQLite)
conn = sqlite3.connect("instance/meme_videos.db")

# Consultar dados
df = pd.read_sql_query("""
SELECT 
    subreddit, 
    COUNT(*) as video_count,
    AVG(size) as avg_size,
    MIN(created_at) as first_video,
    MAX(created_at) as last_video
FROM 
    video 
GROUP BY 
    subreddit
ORDER BY 
    video_count DESC
""", conn)

# Fechar conexão
conn.close()

# Criar visualização
plt.figure(figsize=(12, 6))
sns.barplot(x="subreddit", y="video_count", data=df)
plt.title("Vídeos por Subreddit")
plt.tight_layout()
plt.savefig("dashboard_videos_por_subreddit.png")

# Visualizar os dados
print(df)
```

## Exemplos de Personalização

### Adicionar Marca D'água ao Vídeo

Para adicionar uma marca d'água aos vídeos gerados:

```python
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_watermark(text, size=(200, 50), color=(255, 255, 255, 128)):
    """Cria uma imagem com marca d'água transparente"""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 24)
    w, h = draw.textsize(text, font=font)
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, font=font, fill=color)
    return np.array(img)

def create_video_with_watermark(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True, watermark_text="@SeuUsuario"):
    """Versão modificada da função create_video que adiciona marca d'água"""
    # ... código existente ...
    
    # Criar marca d'água
    watermark = create_watermark(watermark_text)
    watermark_clip = ImageClip(watermark).set_duration(clip.duration).set_position(("right", "bottom"))
    
    # Adicionar marca d'água ao vídeo
    final_clip = CompositeVideoClip([clip, watermark_clip])
    
    # Continuar com o código existente para salvar o vídeo...
    # final_clip.write_videofile(...)
```

### Adicionar Transições entre Imagens

Para adicionar transições suaves entre as imagens:

```python
def create_video_with_transitions(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True):
    """Versão modificada da função create_video que adiciona transições"""
    # ... código existente ...
    
    # Criar clips com transições
    clips = []
    for i, img in enumerate(image_files):
        clip = ImageClip(img).set_duration(duration_per_image)
        
        # Adicionar fade in/out
        if i > 0:  # Não adicionar fade in no primeiro
            clip = clip.fadein(0.5)
        
        if i < len(image_files) - 1:  # Não adicionar fade out no último
            clip = clip.fadeout(0.5)
            
        clips.append(clip)
    
    # Criar vídeo concatenado com transições
    concat_clip = concatenate_videoclips(clips, method="compose")
    
    # Continuar com o código existente...
```

### Personalizar Tamanho do Vídeo

Para gerar vídeos em diferentes resoluções:

```python
def create_video_with_custom_resolution(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True, resolution=(720, 1280)):
    """Versão modificada da função create_video que personaliza a resolução"""
    # ... código existente ...
    
    # Redimensionar imagens para a resolução desejada
    clips = []
    for img in image_files:
        clip = ImageClip(img).set_duration(duration_per_image)
        
        # Redimensionar preservando a proporção
        clip = clip.resize(height=resolution[0])
        
        # Centralizar na tela
        clip = clip.set_position("center")
        
        clips.append(clip)
    
    # Criar vídeo na resolução desejada
    concat_clip = concatenate_videoclips(clips)
    
    # Criar background preto com a resolução correta
    background = ColorClip(resolution, color=(0, 0, 0), duration=concat_clip.duration)
    
    # Compor o vídeo final
    final_clip = CompositeVideoClip([background, concat_clip.set_position("center")])
    
    # Continuar com o código existente...
```

### Adicionar Legendas aos Memes

Para adicionar título ou legendas aos memes no vídeo:

```python
def create_video_with_captions(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True, titles=None):
    """Versão modificada da função create_video que adiciona títulos/legendas"""
    # ... código existente ...
    
    # Se não houver títulos, use lista vazia
    if not titles:
        titles = [""] * len(image_files)
    
    # Criar clips com títulos
    clips = []
    for i, (img, title) in enumerate(zip(image_files, titles)):
        # Criar clip da imagem
        img_clip = ImageClip(img).set_duration(duration_per_image)
        
        # Criar texto
        if title:
            txt_clip = TextClip(title, fontsize=24, color='white', bg_color='black', font='Arial')
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration_per_image)
            
            # Combinar imagem e texto
            clip = CompositeVideoClip([img_clip, txt_clip])
        else:
            clip = img_clip
            
        clips.append(clip)
    
    # Continuar com o código existente...
```

Estes exemplos demonstram a flexibilidade do sistema e como ele pode ser adaptado para diferentes necessidades e casos de uso.
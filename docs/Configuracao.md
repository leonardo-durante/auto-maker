# Guia de Configuração Detalhado

Este documento descreve todas as configurações disponíveis no Gerador de Vídeos de Memes do Reddit e como personalizá-las para atender às suas necessidades.

## Índice

1. [Arquivo config.json](#arquivo-configjson)
2. [Variáveis de Ambiente](#variáveis-de-ambiente)
3. [Configuração da Interface Web](#configuração-da-interface-web)
4. [Configuração do Agendador](#configuração-do-agendador)
5. [Configuração de Música de Fundo](#configuração-de-música-de-fundo)
6. [Configuração Avançada](#configuração-avançada)

## Arquivo config.json

O arquivo `config.json` é o centro de configuração da aplicação. Ele controla as principais configurações do gerador de vídeos.

### Estrutura padrão

```json
{
    "subreddits": ["memes", "dankmemes", "wholesomememes"],
    "posts_limit": 10,
    "image_duration": 3,
    "run_interval_minutes": 60,
    "fps": 30,
    "add_music": true,
    "feed_types": ["hot", "new", "top", "rising"]
}
```

### Parâmetros Explicados

#### subreddits

Lista de subreddits para buscar memes. Cada subreddit é processado separadamente, e um vídeo separado é gerado para cada um.

```json
"subreddits": ["memes", "dankmemes", "wholesomememes", "ProgrammerHumor"]
```

Dicas:
- Para subreddits de humor, use: "memes", "dankmemes", "wholesomememes", "funny", "me_irl"
- Para subreddits de animais, use: "aww", "cats", "dogs", "rarepuppers"
- Para conteúdo específico de tecnologia: "ProgrammerHumor", "techsupportgore"

#### posts_limit

Número máximo de posts (imagens) a serem baixados de cada subreddit. Este número determina quantas imagens serão incluídas em cada vídeo.

```json
"posts_limit": 10
```

Considerações:
- Valores mais altos resultam em vídeos mais longos
- Recomendado: entre 5 e 20 posts
- O limite real pode ser menor se não houver posts suficientes que atendam aos critérios

#### image_duration

Duração (em segundos) que cada imagem aparecerá no vídeo.

```json
"image_duration": 3
```

Dicas:
- Valores mais baixos (1-2s) criam vídeos mais rápidos e dinâmicos
- Valores mais altos (3-5s) dão mais tempo para visualizar cada meme
- Duração total do vídeo = posts_limit × image_duration

#### run_interval_minutes

Intervalo de tempo (em minutos) entre execuções automáticas quando o agendador está ativo.

```json
"run_interval_minutes": 60
```

Considerações:
- Valor mínimo recomendado: 30 minutos (para evitar limites da API do Reddit)
- Para conteúdo sempre atualizado, use entre 60-120 minutos
- Para uso menos frequente, considere 360 (6 horas) ou 720 (12 horas)

#### fps

Frames por segundo do vídeo gerado. Afeta a suavidade das transições.

```json
"fps": 30
```

Dicas:
- 24 fps: aparência cinematográfica
- 30 fps: padrão para conteúdo na web
- 60 fps: transições mais suaves, mas arquivos maiores

#### add_music

Define se deve ser adicionada música de fundo ao vídeo.

```json
"add_music": true
```

Opções:
- `true`: adiciona música de fundo aleatória
- `false`: vídeo sem áudio

#### feed_types

Lista de tipos de feed do Reddit para buscar posts. Quando o gerador é executado, ele escolhe aleatoriamente um dos tipos de feed configurados.

```json
"feed_types": ["hot", "new", "top", "rising"]
```

Opções disponíveis:
- `"hot"`: posts populares no momento
- `"new"`: posts mais recentes
- `"top"`: posts mais votados (de todos os tempos)
- `"rising"`: posts que estão ganhando popularidade rapidamente

## Variáveis de Ambiente

As variáveis de ambiente são usadas para configurações sensíveis ou que variam entre ambientes.

### Configurações do Reddit API

Estas configurações são necessárias para autenticação com a API do Reddit.

```
ID=seu_reddit_client_id
SECRET=seu_reddit_client_secret
AGENT=seu_reddit_user_agent
```

### Configuração do Banco de Dados

```
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
```

Se esta variável não for definida, a aplicação usará SQLite como fallback.

### Configurações da Aplicação Web

```
PORT=5000
DEBUG=True
```

- `PORT`: porta em que o servidor web será executado
- `DEBUG`: modo de depuração (True ou False)

## Configuração da Interface Web

A interface web é configurada principalmente através do código em `web_app.py` e dos templates em `templates/`.

### Personalização do Template

Para personalizar a aparência da interface web, você pode editar os seguintes arquivos:

1. `templates/index.html`: página principal que lista os vídeos
2. `static/css/custom.css`: estilos personalizados (crie este arquivo se não existir)

#### Exemplo de CSS personalizado

Crie ou edite o arquivo `static/css/custom.css`:

```css
.video-container {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s;
}

.video-container:hover {
    transform: translateY(-5px);
}

.card-title {
    color: #336699;
}
```

E inclua-o no `templates/index.html`:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
```

## Configuração do Agendador

O agendador (`scheduler.py`) controla a execução automática da geração de vídeos.

### Configuração de Execução

Para iniciar o agendador:

```bash
python run.py --scheduler
```

O intervalo entre execuções é controlado pelo parâmetro `run_interval_minutes` no `config.json`.

### Executando como Serviço do Sistema

Para garantir que o agendador continue rodando após o fechamento do terminal, você pode configurá-lo como um serviço do sistema.

#### Linux (systemd)

Crie um arquivo `/etc/systemd/system/meme-generator.service`:

```
[Unit]
Description=Meme Video Generator Scheduler
After=network.target

[Service]
User=seu_usuario
WorkingDirectory=/caminho/para/meme-video-generator
ExecStart=/caminho/para/python /caminho/para/meme-video-generator/run.py --scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ative e inicie o serviço:

```bash
sudo systemctl enable meme-generator.service
sudo systemctl start meme-generator.service
```

## Configuração de Música de Fundo

A aplicação usa músicas de fundo livres de direitos autorais. Você pode personalizar as fontes de música.

### Adicionar Músicas Personalizadas

1. Crie uma pasta `music/` na raiz do projeto (se não existir)
2. Adicione arquivos de música em formato MP3 nesta pasta
3. A aplicação selecionará aleatoriamente uma música durante a geração de vídeos

### Configuração Avançada

Para personalizar a seleção de música, você pode editar a função `download_background_music()` em `meme_generator.py`.

## Configuração Avançada

### Personalização do Processamento de Vídeo

Para personalizar o processamento de vídeo, você pode editar a função `create_video()` em `meme_generator.py`.

Algumas modificações possíveis:

#### Adicionar Transições entre Imagens

```python
def create_video(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True):
    # ... código existente ...
    
    # Adiciona transições de fade entre as imagens
    clips = []
    for i, img in enumerate(image_files):
        clip = ImageClip(img).set_duration(duration_per_image)
        
        # Adiciona fade in e fade out
        if i > 0:  # Não adiciona fade in na primeira imagem
            clip = clip.fadein(0.5)
        
        if i < len(image_files) - 1:  # Não adiciona fade out na última imagem
            clip = clip.fadeout(0.5)
            
        clips.append(clip)
    
    # ... resto do código ...
```

#### Personalizar Resolução do Vídeo

```python
def create_video(duration_per_image=3, output_folder=None, name='video', fps=30, add_music=True, resolution=(1080, 1920)):
    # ... código existente ...
    
    # Redimensiona todas as imagens para a mesma resolução
    clips = []
    for img in image_files:
        clip = ImageClip(img).set_duration(duration_per_image)
        clip = clip.resize(height=resolution[0])  # Mantém a proporção
        clips.append(clip)
    
    # ... resto do código ...
```

### Configuração do Banco de Dados

Para configurações avançadas do banco de dados, você pode modificar o arquivo `app.py`.

#### Exemplo: Configurar Pool de Conexões

```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20
}
```

#### Exemplo: Configurar Timeout de Conexão

```python
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }
}
```

## Depuração e Solução de Problemas

### Ativar Logs Detalhados

Para obter logs mais detalhados, você pode modificar a configuração de logging no início dos arquivos principais:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
```

### Verificar Logs

Para verificar os logs em busca de erros:

```bash
tail -f debug.log
```

### Teste Manual

Para testar manualmente cada componente:

```bash
# Testar apenas a API do Reddit
python -c "from RedditBot import RedditBot; bot = RedditBot(); print(bot.get_images('memes', 1))"

# Testar apenas a geração de vídeo
python -c "import meme_generator; meme_generator.create_video(duration_per_image=1, name='test')"
```
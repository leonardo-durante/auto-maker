# Guia de Instalação Detalhado

Este guia fornece instruções passo a passo para instalar e configurar o Gerador de Vídeos de Memes do Reddit em diferentes sistemas operacionais.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação no Linux](#instalação-no-linux)
3. [Instalação no Windows](#instalação-no-windows)
4. [Instalação no macOS](#instalação-no-macos)
5. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
6. [Configuração da API do Reddit](#configuração-da-api-do-reddit)
7. [Teste da Instalação](#teste-da-instalação)

## Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Git
- PostgreSQL (opcional, mas recomendado)
- FFmpeg (para processamento de vídeo)

## Instalação no Linux

### 1. Instalar dependências do sistema

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git ffmpeg postgresql
```

#### Fedora/CentOS:

```bash
sudo dnf update
sudo dnf install -y python3 python3-pip python3-virtualenv git ffmpeg postgresql
```

### 2. Clone o repositório

```bash
git clone https://github.com/seu-usuario/meme-video-generator.git
cd meme-video-generator
```

### 3. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados PostgreSQL

```bash
sudo -u postgres psql
```

No prompt do PostgreSQL:

```sql
CREATE DATABASE meme_videos;
CREATE USER meme_user WITH ENCRYPTED PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE meme_videos TO meme_user;
\q
```

### 6. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
echo "ID=seu_reddit_client_id" > .env
echo "SECRET=seu_reddit_client_secret" >> .env
echo "AGENT=seu_reddit_user_agent" >> .env
echo "DATABASE_URL=postgresql://meme_user:sua_senha@localhost:5432/meme_videos" >> .env
```

## Instalação no Windows

### 1. Instale o Python

Baixe e instale Python do [site oficial](https://www.python.org/downloads/windows/), certificando-se de marcar a opção "Add Python to PATH" durante a instalação.

### 2. Instale o Git

Baixe e instale Git do [site oficial](https://git-scm.com/download/win).

### 3. Instale o FFmpeg

1. Baixe o pacote FFmpeg para Windows do [site oficial](https://ffmpeg.org/download.html) ou [aqui](https://github.com/BtbN/FFmpeg-Builds/releases)
2. Extraia os arquivos para C:\ffmpeg
3. Adicione C:\ffmpeg\bin ao PATH do sistema:
   - Abra Painel de Controle > Sistema > Configurações avançadas do sistema > Variáveis de Ambiente
   - Edite a variável PATH e adicione C:\ffmpeg\bin

### 4. Clone o repositório

Abra o Prompt de Comando ou PowerShell:

```bash
git clone https://github.com/seu-usuario/meme-video-generator.git
cd meme-video-generator
```

### 5. Crie e ative um ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 6. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 7. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
ID=seu_reddit_client_id
SECRET=seu_reddit_client_secret
AGENT=seu_reddit_user_agent
DATABASE_URL=postgresql://meme_user:sua_senha@localhost:5432/meme_videos
```

Se preferir usar SQLite em vez de PostgreSQL, omita a linha `DATABASE_URL`.

## Instalação no macOS

### 1. Instale as dependências do sistema

Usando Homebrew:

```bash
brew update
brew install python ffmpeg postgresql
pip3 install virtualenv
```

### 2. Inicie o PostgreSQL

```bash
brew services start postgresql
```

### 3. Clone o repositório

```bash
git clone https://github.com/seu-usuario/meme-video-generator.git
cd meme-video-generator
```

### 4. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 6. Configure o banco de dados PostgreSQL

```bash
psql postgres
```

No prompt do PostgreSQL:

```sql
CREATE DATABASE meme_videos;
CREATE USER meme_user WITH ENCRYPTED PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE meme_videos TO meme_user;
\q
```

### 7. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
echo "ID=seu_reddit_client_id" > .env
echo "SECRET=seu_reddit_client_secret" >> .env
echo "AGENT=seu_reddit_user_agent" >> .env
echo "DATABASE_URL=postgresql://meme_user:sua_senha@localhost:5432/meme_videos" >> .env
```

## Configuração do Banco de Dados

### PostgreSQL

Se você optar por usar o PostgreSQL, certifique-se de que o serviço esteja rodando e que o usuário e o banco de dados tenham sido criados conforme as instruções acima.

Para verificar a conexão com o banco de dados:

```bash
python -c "import psycopg2; conn = psycopg2.connect('postgresql://meme_user:sua_senha@localhost:5432/meme_videos'); print('Conectado ao PostgreSQL')"
```

### SQLite

Se você não configurar a variável `DATABASE_URL`, a aplicação usará SQLite como banco de dados de fallback. O arquivo do banco de dados será criado automaticamente na raiz do projeto.

## Configuração da API do Reddit

Para usar a API do Reddit, você precisa criar uma aplicação no Reddit:

1. Acesse https://www.reddit.com/prefs/apps
2. Faça login na sua conta do Reddit
3. Clique em "create app" ou "create another app" na parte inferior
4. Preencha as informações:
   - Nome: MemeVideoGenerator
   - Tipo: script
   - Descrição: Uma aplicação para gerar vídeos de memes
   - Sobre URL: (pode deixar em branco)
   - URL de redirecionamento: http://localhost:8080
5. Clique em "create app"
6. Anote o Client ID (o código abaixo do nome da aplicação) e o Client Secret

Adicione essas informações ao seu arquivo `.env`:

```
ID=seu_client_id
SECRET=seu_client_secret
AGENT=script:MemeVideoGenerator:v1.0 (by /u/seu_username)
```

## Teste da Instalação

### 1. Verifique se o arquivo `config.json` foi criado

Se o arquivo não existir, ele será criado automaticamente na primeira execução. Você pode criá-lo manualmente com o seguinte conteúdo:

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

### 2. Execute o gerador de vídeos uma vez para testar

```bash
python run.py --once
```

Verifique se a pasta `output_*` foi criada e se contém arquivos de vídeo.

### 3. Inicie o servidor web

```bash
python run_flask.py
```

Ou para produção:

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Acesse `http://localhost:5000` no seu navegador para verificar se a interface web está funcionando corretamente.

## Solução de Problemas Comuns na Instalação

### Erro: No module named 'psycopg2'

Instale o pacote:

```bash
pip install psycopg2-binary
```

### Erro: FFmpeg not found

Certifique-se de que o FFmpeg está instalado e disponível no PATH do sistema.

### Erro: Cannot connect to PostgreSQL

Verifique se o serviço PostgreSQL está rodando:

- Linux: `sudo systemctl status postgresql`
- macOS: `brew services list`
- Windows: Verifique nos Serviços do Windows

Verifique também se as credenciais no `DATABASE_URL` estão corretas.

### Erro: Não foi possível autenticar com o Reddit

Verifique se as credenciais da API do Reddit estão corretas no arquivo `.env`.

Se ainda tiver problemas, consulte a documentação completa no GitHub ou abra uma issue para obter suporte.
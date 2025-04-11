# Documentação do Gerador de Vídeos de Memes do Reddit

## Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Uso da Aplicação](#uso-da-aplicação)
6. [Arquitetura do Sistema](#arquitetura-do-sistema)
7. [API](#api)
8. [Banco de Dados](#banco-de-dados)
9. [Solução de Problemas](#solução-de-problemas)

## Visão Geral

O Gerador de Vídeos de Memes do Reddit é uma aplicação Python que automaticamente baixa imagens de memes de subreddits específicos do Reddit, compila essas imagens em um vídeo com música de fundo, e disponibiliza os vídeos gerados através de uma interface web.

Principais funcionalidades:
- Busca e download automático de memes dos subreddits configurados
- Conversão de imagens para um formato padronizado (JPG)
- Criação de vídeos com música de fundo
- Interface web para gerenciar os vídeos gerados
- Suporte para múltiplos tipos de feeds do Reddit (hot, new, top, rising)
- Agendamento automático da geração de vídeos
- Compartilhamento fácil em redes sociais
- Sistema de categorias para organizar os subreddits

## Requisitos do Sistema

- Python 3.8+
- PostgreSQL (ou SQLite como alternativa de fallback)
- Bibliotecas Python (instaladas automaticamente):
  - Flask
  - Flask-SQLAlchemy
  - PRAW (Python Reddit API Wrapper)
  - MoviePy
  - Gunicorn (para produção)
  - python-dotenv
  - Psycopg2 (para PostgreSQL)

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/meme-video-generator.git
cd meme-video-generator
```

### 2. Configure o ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as credenciais do Reddit

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
ID=seu_reddit_client_id
SECRET=seu_reddit_client_secret
AGENT=seu_reddit_user_agent
```

Para obter essas credenciais:
1. Acesse https://www.reddit.com/prefs/apps
2. Clique em "create another app..."
3. Preencha as informações (tipo: script)
4. Após criar, você verá o ID (abaixo do nome da aplicação) e o SECRET

### 5. Configure o banco de dados

A aplicação usará PostgreSQL por padrão se a variável `DATABASE_URL` estiver definida. Caso contrário, usará SQLite.

Para PostgreSQL, adicione ao arquivo `.env`:

```
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco
```

## Configuração

### Arquivo config.json

O arquivo `config.json` controla o comportamento do gerador de vídeos. Ele é criado automaticamente na primeira execução, mas você pode personalizá-lo:

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

### Parâmetros:

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| subreddits | Lista de subreddits para buscar memes | ["memes", "dankmemes", "wholesomememes"] |
| posts_limit | Número máximo de posts para baixar de cada subreddit | 10 |
| image_duration | Duração em segundos que cada imagem aparece no vídeo | 3 |
| run_interval_minutes | Intervalo em minutos para execução automática | 60 |
| fps | Frames por segundo do vídeo gerado | 30 |
| add_music | Se deve adicionar música de fundo aos vídeos | true |
| feed_types | Tipos de feed do Reddit para buscar posts | ["hot", "new", "top", "rising"] |

## Uso da Aplicação

### Iniciar o servidor web

```bash
python run_flask.py
# ou para produção
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Acesse a interface web em `http://localhost:5000`

### Executar geração de vídeos manualmente

```bash
# Executa uma vez
python run.py --once

# Inicia o agendador (executa periodicamente)
python run.py --scheduler
```

### Interface Web

A interface web permite:

1. **Visualizar Vídeos Gerados**:
   - Lista todos os vídeos gerados com detalhes (subreddit, data, tamanho)
   - Reprodução direta no navegador
   - Opções de compartilhamento em redes sociais
   - Download dos vídeos

2. **Gerar Novos Vídeos**:
   - Escolher subreddits (incluindo categorias pré-definidas)
   - Definir número de posts
   - Selecionar tipo de feed (hot, new, top, rising)
   - Ajustar duração por imagem

## Arquitetura do Sistema

### Componentes Principais

1. **RedditBot (RedditBot.py)**:
   - Gerencia a autenticação com a API do Reddit
   - Busca e baixa imagens dos subreddits especificados
   - Converte imagens para formato JPG

2. **Gerador de Vídeos (meme_generator.py)**:
   - Processa as imagens baixadas
   - Cria vídeos com música de fundo
   - Gerencia a criação das pastas de saída

3. **Aplicação Web (web_app.py)**:
   - Interface do usuário baseada em Flask
   - Lista os vídeos gerados
   - Permite configuração e geração de novos vídeos

4. **Agendador (scheduler.py)**:
   - Executa a geração de vídeos periodicamente
   - Gerencia intervalos de execução

5. **Banco de Dados (models.py)**:
   - Modelos para armazenar informações sobre vídeos e subreddits
   - Facilita busca e gerenciamento dos dados

## API

A aplicação oferece endpoints JSON para integração com outros sistemas:

### `/api/videos`

Retorna a lista de todos os vídeos gerados no formato JSON.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "path": "output_memes_20250410_123045/memes_memes.mp4",
    "name": "memes_memes.mp4",
    "subreddit": "memes",
    "date": "10/04/2025 12:30:45",
    "size": "1.2 MB",
    "feed_type": "hot",
    "post_count": 10
  }
]
```

### `/api/subreddits`

Retorna a lista de subreddits cadastrados no sistema.

**Exemplo de resposta:**
```json
[
  {
    "id": 1,
    "name": "memes",
    "description": "Memes gerais e populares",
    "category": "Humor",
    "subscribers": null
  }
]
```

## Banco de Dados

O sistema utiliza SQLAlchemy para gerenciar os modelos e acessar o banco de dados.

### Modelo `Video`

Armazena informações sobre os vídeos gerados:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| filename | String | Nome do arquivo de vídeo |
| path | String | Caminho completo para o arquivo |
| subreddit | String | Nome do subreddit de origem |
| created_at | DateTime | Data e hora de criação |
| feed_type | String | Tipo de feed usado (hot, new, etc.) |
| duration | Integer | Duração total em segundos |
| size | Integer | Tamanho em bytes |
| post_count | Integer | Número de posts incluídos |

### Modelo `Subreddit`

Armazena informações sobre subreddits populares:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| name | String | Nome do subreddit |
| description | Text | Descrição do conteúdo |
| category | String | Categoria (Humor, Animais, etc.) |
| subscribers | Integer | Número de inscritos |
| last_updated | DateTime | Última atualização |

## Solução de Problemas

### Erros comuns

1. **Erro de autenticação com o Reddit**
   - Verifique se as credenciais no arquivo `.env` estão corretas
   - Certifique-se de que o arquivo `.env` está na raiz do projeto

2. **Nenhuma imagem baixada**
   - Verifique se os subreddits especificados existem
   - Teste com outro tipo de feed (por exemplo, "new" em vez de "hot")
   - Alguns subreddits podem ter restrições de idade ou conteúdo

3. **Erro ao criar vídeo**
   - Verifique se o FFmpeg está instalado
   - Certifique-se de que há espaço suficiente no disco
   - Verifique se o formato das imagens é compatível

4. **Banco de dados não conecta**
   - Verifique a string de conexão DATABASE_URL
   - Certifique-se de que o PostgreSQL está rodando
   - A aplicação usará SQLite como fallback se o PostgreSQL não estiver disponível

### Logs

Os logs da aplicação são armazenados no console e podem ser redirecionados para um arquivo. Verifique os logs para diagnosticar problemas.

---

## Suporte

Para obter suporte, abra uma issue no repositório do GitHub ou entre em contato com os mantenedores do projeto.
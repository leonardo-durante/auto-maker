# Arquitetura do Sistema

Este documento descreve a arquitetura do Gerador de Vídeos de Memes do Reddit, explicando como os diferentes componentes interagem entre si e o fluxo de dados através do sistema.

## Índice

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Componentes Principais](#componentes-principais)
3. [Fluxo de Dados](#fluxo-de-dados)
4. [Modelo de Dados](#modelo-de-dados)
5. [Integração com API Externa](#integração-com-api-externa)
6. [Sistema de Arquivos](#sistema-de-arquivos)
7. [Processamento de Mídia](#processamento-de-mídia)
8. [Interface Web](#interface-web)
9. [Considerações de Design](#considerações-de-design)

## Visão Geral da Arquitetura

O sistema é baseado em uma arquitetura modular, onde cada componente é responsável por uma parte específica do processo. A aplicação segue um fluxo de dados linear que começa com a coleta de imagens do Reddit, passa pelo processamento das imagens e criação de vídeos, e termina com o armazenamento e apresentação dos vídeos gerados.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  RedditBot  │───▶│    Meme     │───▶│  Banco de   │───▶│  Interface  │
│  (Coleta)   │    │  Generator  │    │    Dados    │    │     Web     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                                      │
       │                  │                                      │
       ▼                  ▼                                      ▼
┌─────────────┐    ┌─────────────┐                       ┌─────────────┐
│  API Reddit │    │  Sistema de │                       │  Navegador  │
│             │    │  Arquivos   │                       │  do Usuário │
└─────────────┘    └─────────────┘                       └─────────────┘
```

O sistema também inclui um agendador que pode executar o processo periodicamente sem intervenção manual.

## Componentes Principais

### 1. RedditBot (RedditBot.py)

Este componente é responsável por interagir com a API do Reddit, autenticar-se e baixar imagens dos subreddits configurados.

**Responsabilidades:**
- Autenticação com a API do Reddit
- Busca de posts em subreddits específicos
- Filtragem de posts para obter apenas aqueles com imagens
- Download de imagens
- Conversão de formatos de imagem (PNG, JPEG) para JPG

**Dependências:**
- PRAW (Python Reddit API Wrapper)
- python-dotenv (para variáveis de ambiente)
- PIL/Pillow (para processamento de imagens)

### 2. Gerador de Memes (meme_generator.py)

Este componente é responsável por processar as imagens baixadas e criar vídeos com música de fundo.

**Responsabilidades:**
- Processamento de imagens
- Criação de sequências de slides
- Adição de música de fundo
- Renderização de vídeo final
- Organização de arquivos em pastas de saída

**Dependências:**
- MoviePy (para criação de vídeos)
- FFmpeg (usado internamente pelo MoviePy)
- Requests (para download de música)

### 3. Agendador (scheduler.py)

Este componente controla a execução periódica do gerador de vídeos.

**Responsabilidades:**
- Gerenciamento de intervalos de execução
- Execução do gerador de vídeos em intervalos configurados
- Logs de execução

**Dependências:**
- schedule (para agendamento)
- time (para controle de tempo)

### 4. Interface Web (web_app.py)

Este componente fornece uma interface de usuário baseada em web para visualizar, gerenciar e configurar a geração de vídeos.

**Responsabilidades:**
- Listar vídeos gerados
- Permitir reprodução de vídeos no navegador
- Facilitar compartilhamento em redes sociais
- Permitir configuração de novos vídeos
- Fornecer endpoints de API para integração

**Dependências:**
- Flask (framework web)
- Flask-SQLAlchemy (ORM para banco de dados)
- Jinja2 (sistema de templates)

### 5. Modelos de Dados (models.py)

Este componente define as estruturas de dados usadas pela aplicação e gerencia a interação com o banco de dados.

**Responsabilidades:**
- Definição de esquema de banco de dados
- Mapeamento objeto-relacional
- Consultas ao banco de dados

**Dependências:**
- SQLAlchemy (ORM)
- Flask-SQLAlchemy (integração com Flask)

### 6. Executor (run.py)

Este componente serve como ponto de entrada para execução manual da aplicação.

**Responsabilidades:**
- Processamento de argumentos de linha de comando
- Execução única do gerador
- Inicialização do agendador

**Dependências:**
- argparse (para processamento de argumentos)

## Fluxo de Dados

O fluxo de dados através do sistema segue estas etapas:

1. **Coleta de dados:**
   - O RedditBot se autentica na API do Reddit
   - Busca posts dos subreddits configurados
   - Filtra posts para obter apenas aqueles com imagens
   - Baixa as imagens para a pasta `images/`
   - Converte as imagens para formato JPG

2. **Processamento de mídia:**
   - O gerador de vídeos processa as imagens baixadas
   - Cria um clip para cada imagem com duração configurada
   - Concatena os clips em uma sequência
   - Baixa música de fundo (se configurado)
   - Adiciona a música ao vídeo
   - Renderiza o vídeo final

3. **Armazenamento:**
   - Cria uma pasta de saída com timestamp
   - Salva o vídeo gerado na pasta de saída
   - Registra os metadados do vídeo no banco de dados

4. **Apresentação:**
   - A interface web consulta o banco de dados para obter a lista de vídeos
   - Apresenta os vídeos com metadados e controles
   - Permite reprodução, download e compartilhamento

## Modelo de Dados

### Diagrama ER

```
┌───────────┐       ┌────────────┐
│   Video   │       │  Subreddit │
├───────────┤       ├────────────┤
│ id        │       │ id         │
│ filename  │       │ name       │
│ path      │       │ description│
│ subreddit │       │ category   │
│ created_at│       │ subscribers│
│ feed_type │       │ last_updated│
│ duration  │       └────────────┘
│ size      │
│ post_count│
└───────────┘
```

### Modelo Video

Armazena informações sobre os vídeos gerados:

- **id**: Identificador único (chave primária)
- **filename**: Nome do arquivo de vídeo
- **path**: Caminho completo para o arquivo
- **subreddit**: Nome do subreddit de origem
- **created_at**: Data e hora de criação
- **feed_type**: Tipo de feed usado (hot, new, etc.)
- **duration**: Duração total em segundos
- **size**: Tamanho em bytes
- **post_count**: Número de posts incluídos

### Modelo Subreddit

Armazena informações sobre subreddits populares:

- **id**: Identificador único (chave primária)
- **name**: Nome do subreddit
- **description**: Descrição do conteúdo
- **category**: Categoria (Humor, Animais, etc.)
- **subscribers**: Número de inscritos
- **last_updated**: Última atualização

## Integração com API Externa

A aplicação se integra com a API do Reddit através do PRAW (Python Reddit API Wrapper).

### Autenticação

A autenticação é realizada usando o método de script do Reddit, que requer:
- Client ID
- Client Secret
- User Agent

Estas informações são armazenadas em variáveis de ambiente para segurança.

### Endpoints Usados

- `/r/{subreddit}/{feed_type}` - Para buscar posts de subreddits específicos
- Parâmetros de consulta:
  - `limit`: Número máximo de posts para retornar
  - `after`: Marcador para paginação

### Limitações

- A API do Reddit tem limite de 60 solicitações por minuto
- Restrições de idade e conteúdo podem afetar os resultados
- Algumas imagens podem ser removidas ou indisponíveis

## Sistema de Arquivos

A aplicação organiza os arquivos da seguinte forma:

```
/
├── .env                  # Variáveis de ambiente (não versionado)
├── config.json           # Configurações da aplicação
├── images/               # Pasta temporária para imagens baixadas
├── music/                # Músicas de fundo
├── output_*_*/           # Pastas de saída para vídeos gerados
├── static/               # Arquivos estáticos para a web
├── templates/            # Templates HTML
├── RedditBot.py          # Código do bot
├── meme_generator.py     # Gerador de vídeos
├── scheduler.py          # Agendador
├── web_app.py            # Interface web
├── models.py             # Modelos de dados
├── app.py                # Aplicação Flask
├── run.py                # Script principal
└── wsgi.py               # Ponto de entrada para servidores WSGI
```

Cada execução cria uma nova pasta de saída no formato `output_{subreddit}_{timestamp}/` para armazenar os vídeos gerados.

## Processamento de Mídia

### Processamento de Imagens

1. As imagens são baixadas em seu formato original
2. Convertidas para JPG para garantir compatibilidade
3. Redimensionadas, se necessário, para manter consistência

### Processamento de Vídeo

1. Cada imagem é transformada em um clip com duração fixa
2. Os clips são concatenados em sequência
3. Música de fundo é adicionada (se configurada)
4. O vídeo final é renderizado com configurações definidas (fps, resolução)

### Processamento de Áudio

1. Música de fundo é baixada de fontes livres de direitos autorais
2. O áudio é cortado para corresponder à duração do vídeo
3. Volume é ajustado para um nível apropriado

## Interface Web

A interface web é construída com Flask e segue uma arquitetura MVC simples:

- **Modelos**: definidos em `models.py`
- **Visualizações**: implementadas em `web_app.py`
- **Templates**: armazenados na pasta `templates/`

### Rotas Principais

- `/`: Página inicial com lista de vídeos
- `/video/<path>`: Serve um arquivo de vídeo específico
- `/run`: Executa a geração de vídeos com parâmetros personalizados
- `/api/videos`: Endpoint JSON que retorna a lista de vídeos
- `/api/subreddits`: Endpoint JSON que retorna a lista de subreddits

### Design Responsivo

A interface web usa Bootstrap para garantir compatibilidade com dispositivos móveis e desktop.

## Considerações de Design

### Segurança

- Credenciais da API do Reddit são armazenadas em variáveis de ambiente
- Configurações sensíveis não são versionadas
- Validação de entrada em todas as rotas da web

### Escalabilidade

- Uso de um banco de dados para persistência
- Desacoplamento de componentes
- Suporte para múltiplos subreddits
- Agendamento para execução automática

### Manutenção

- Código modular e bem organizado
- Logs abrangentes para depuração
- Tratamento de erros consistente
- Documentação detalhada

### Extensibilidade

O sistema foi projetado para ser facilmente estendido com novas funcionalidades:

- **Novos formatos de saída**: adicionar novos formatos além de MP4
- **Fontes adicionais de conteúdo**: integrar com outras plataformas além do Reddit
- **Efeitos visuais personalizados**: implementar transições ou filtros adicionais
- **Análise de conteúdo**: integrar com serviços de AI para classificação ou moderação de conteúdo
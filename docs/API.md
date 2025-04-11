# Documentação da API

Este documento descreve os endpoints da API disponíveis no Gerador de Vídeos de Memes do Reddit, permitindo integração com outros sistemas ou desenvolvimento de aplicações cliente personalizadas.

## Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Endpoints](#endpoints)
   - [Listar Vídeos](#listar-vídeos)
   - [Detalhes do Vídeo](#detalhes-do-vídeo)
   - [Listar Subreddits](#listar-subreddits)
   - [Executar Geração de Vídeo](#executar-geração-de-vídeo)
4. [Objetos de Resposta](#objetos-de-resposta)
5. [Códigos de Status](#códigos-de-status)
6. [Exemplos de Uso](#exemplos-de-uso)
7. [Limitações](#limitações)

## Visão Geral

A API do Gerador de Vídeos de Memes do Reddit segue os princípios RESTful e usa JSON como formato de dados. Todos os endpoints estão disponíveis no mesmo servidor que a interface web, facilitando a integração.

**URL Base**: `http://seu-servidor:5000/api`

## Autenticação

Atualmente, a API não requer autenticação, mas isso pode mudar em versões futuras para proteger recursos sensíveis.

## Endpoints

### Listar Vídeos

Retorna uma lista de todos os vídeos gerados, ordenados por data de criação (mais recentes primeiro).

- **URL**: `/videos`
- **Método**: GET
- **Parâmetros de Consulta**:
  - `limit` (opcional): Número máximo de vídeos a retornar (padrão: 50)
  - `offset` (opcional): Número de vídeos a pular (para paginação, padrão: 0)
  - `subreddit` (opcional): Filtrar por subreddit específico

#### Exemplo de Resposta

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
  },
  {
    "id": 2,
    "path": "output_dankmemes_20250410_123050/dankmemes_memes.mp4",
    "name": "dankmemes_memes.mp4",
    "subreddit": "dankmemes",
    "date": "10/04/2025 12:30:50",
    "size": "1.5 MB",
    "feed_type": "new",
    "post_count": 10
  }
]
```

### Detalhes do Vídeo

Retorna informações detalhadas sobre um vídeo específico.

- **URL**: `/videos/:id`
- **Método**: GET
- **Parâmetros de URL**:
  - `id`: ID do vídeo

#### Exemplo de Resposta

```json
{
  "id": 1,
  "path": "output_memes_20250410_123045/memes_memes.mp4",
  "name": "memes_memes.mp4",
  "subreddit": "memes",
  "date": "10/04/2025 12:30:45",
  "created_at": "2025-04-10T12:30:45Z",
  "size": "1.2 MB",
  "size_bytes": 1258291,
  "feed_type": "hot",
  "post_count": 10,
  "duration": 30,
  "url": "http://seu-servidor:5000/video/output_memes_20250410_123045/memes_memes.mp4"
}
```

### Listar Subreddits

Retorna a lista de subreddits cadastrados no sistema.

- **URL**: `/subreddits`
- **Método**: GET
- **Parâmetros de Consulta**:
  - `category` (opcional): Filtrar por categoria

#### Exemplo de Resposta

```json
[
  {
    "id": 1,
    "name": "memes",
    "description": "Memes gerais e populares",
    "category": "Humor",
    "subscribers": null
  },
  {
    "id": 2,
    "name": "dankmemes",
    "description": "Memes irreverentes e populares",
    "category": "Humor",
    "subscribers": null
  },
  {
    "id": 3,
    "name": "cats",
    "description": "Fotos e vídeos de gatos",
    "category": "Animais",
    "subscribers": null
  }
]
```

### Executar Geração de Vídeo

Inicia a geração de um novo vídeo com as configurações especificadas.

- **URL**: `/generate`
- **Método**: POST
- **Tipo de Conteúdo**: `application/json`
- **Corpo da Requisição**:

```json
{
  "subreddit": "memes",
  "limit": 10,
  "feed_type": "hot",
  "duration": 3
}
```

#### Parâmetros

- `subreddit` (obrigatório): Nome do subreddit ou lista de subreddits separados por vírgula
- `limit` (opcional): Número máximo de posts para baixar (padrão: 10)
- `feed_type` (opcional): Tipo de feed do Reddit (padrão: "hot")
- `duration` (opcional): Duração de cada imagem em segundos (padrão: 3)

#### Exemplo de Resposta

```json
{
  "status": "success",
  "message": "Geração de vídeo iniciada",
  "job_id": "gen_20250410_123045",
  "estimated_completion_time": "1-2 minutes"
}
```

## Objetos de Resposta

### Objeto Video

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| path | String | Caminho relativo do arquivo |
| name | String | Nome do arquivo |
| subreddit | String | Nome do subreddit |
| date | String | Data formatada para exibição |
| created_at | String | Data ISO 8601 |
| size | String | Tamanho formatado para exibição |
| size_bytes | Integer | Tamanho em bytes |
| feed_type | String | Tipo de feed usado |
| post_count | Integer | Número de posts incluídos |
| duration | Integer | Duração em segundos |
| url | String | URL completa para acessar o vídeo |

### Objeto Subreddit

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Identificador único |
| name | String | Nome do subreddit |
| description | String | Descrição do conteúdo |
| category | String | Categoria do subreddit |
| subscribers | Integer | Número de inscritos (se disponível) |

## Códigos de Status

A API usa códigos de status HTTP padrão:

- **200 OK**: A requisição foi bem-sucedida
- **400 Bad Request**: A requisição contém parâmetros inválidos
- **404 Not Found**: O recurso solicitado não foi encontrado
- **500 Internal Server Error**: Ocorreu um erro no servidor

## Exemplos de Uso

### Curl

#### Listar Vídeos

```bash
curl -X GET "http://localhost:5000/api/videos"
```

#### Obter Detalhes de um Vídeo

```bash
curl -X GET "http://localhost:5000/api/videos/1"
```

#### Gerar um Novo Vídeo

```bash
curl -X POST "http://localhost:5000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"subreddit": "memes,dankmemes", "limit": 15, "feed_type": "hot", "duration": 3}'
```

### Python

```python
import requests
import json

# Listar vídeos
response = requests.get("http://localhost:5000/api/videos")
videos = response.json()
print(f"Encontrados {len(videos)} vídeos")

# Gerar novo vídeo
data = {
    "subreddit": "memes",
    "limit": 10,
    "feed_type": "hot",
    "duration": 3
}
response = requests.post("http://localhost:5000/api/generate", json=data)
result = response.json()
print(f"Status: {result['status']}, Mensagem: {result['message']}")
```

### JavaScript (Fetch API)

```javascript
// Listar vídeos
fetch('http://localhost:5000/api/videos')
  .then(response => response.json())
  .then(data => {
    console.log(`Encontrados ${data.length} vídeos`);
  });

// Gerar novo vídeo
const data = {
  subreddit: 'memes',
  limit: 10,
  feed_type: 'hot',
  duration: 3
};

fetch('http://localhost:5000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(result => {
    console.log(`Status: ${result.status}, Mensagem: ${result.message}`);
  });
```

## Limitações

- A API não suporta autenticação atualmente
- Não há limite de taxa de requisições implementado
- A operação de geração de vídeo é assíncrona, e o status não pode ser consultado após o início
- As consultas não suportam ordenação ou filtragem avançada
- O endpoint de geração não valida a existência dos subreddits

## Notas para Desenvolvedores

Para estender a API, você pode adicionar novos endpoints no arquivo `web_app.py`. A estrutura básica para um novo endpoint seria:

```python
@app.route('/api/novo_endpoint', methods=['GET'])
def novo_endpoint():
    # Lógica do endpoint
    return jsonify({"resultado": "dados"})
```

Lembre-se de adicionar tratamento de erros adequado e validação de entrada para qualquer novo endpoint.
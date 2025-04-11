# Guia de Solução de Problemas

Este documento contém informações para ajudar a diagnosticar e resolver problemas comuns que você pode encontrar ao usar o Gerador de Vídeos de Memes do Reddit.

## Índice

1. [Problemas de Instalação](#problemas-de-instalação)
2. [Problemas com a API do Reddit](#problemas-com-a-api-do-reddit)
3. [Problemas na Geração de Vídeos](#problemas-na-geração-de-vídeos)
4. [Problemas com o Banco de Dados](#problemas-com-o-banco-de-dados)
5. [Problemas na Interface Web](#problemas-na-interface-web)
6. [Problemas no Agendador](#problemas-no-agendador)
7. [Verificação de Logs](#verificação-de-logs)
8. [Perguntas Frequentes](#perguntas-frequentes)

## Problemas de Instalação

### Erro: Pacote não encontrado

**Sintoma**: Mensagem de erro do tipo `ModuleNotFoundError: No module named 'nome_do_pacote'`

**Solução**:
1. Verifique se você está no ambiente virtual correto (se estiver usando venv)
2. Reinstale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Instale o pacote específico que está faltando:
   ```bash
   pip install nome_do_pacote
   ```

### Erro: FFmpeg não encontrado

**Sintoma**: Erro do tipo `RuntimeError: MoviePy Error: failed to find ffmpeg`

**Solução**:
1. Instale o FFmpeg:
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) ou `sudo dnf install ffmpeg` (Fedora)
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Baixe de https://ffmpeg.org/download.html e adicione ao PATH
2. Verifique se o FFmpeg está no PATH do sistema:
   ```bash
   ffmpeg -version
   ```

### Erro: Python incorreto sendo usado

**Sintoma**: A versão do Python usada é muito antiga ou não é a que você esperava

**Solução**:
1. Verifique a versão do Python que está sendo usada:
   ```bash
   python --version
   ```
2. Especifique a versão correta ao criar o ambiente virtual:
   ```bash
   python3 -m venv venv
   ```
3. Em alguns sistemas, você pode precisar usar `python3` em vez de `python`.

## Problemas com a API do Reddit

### Erro: Falha na autenticação

**Sintoma**: Erro do tipo `prawcore.exceptions.ResponseException: received 401 HTTP response`

**Solução**:
1. Verifique se as credenciais no arquivo `.env` estão corretas
2. Certifique-se de que o arquivo `.env` está na raiz do projeto
3. Verifique se as credenciais ainda são válidas (elas podem expirar ou ser revogadas)
4. Recrie as credenciais no [Reddit App Preferences](https://www.reddit.com/prefs/apps)

### Erro: Muitas solicitações

**Sintoma**: Erro do tipo `prawcore.exceptions.TooManyRequests`

**Solução**:
1. Reduza a frequência de solicitações (aumente o intervalo no agendador)
2. Reduza o número de subreddits processados de uma vez
3. Adicione um atraso entre solicitações:
   ```python
   import time
   time.sleep(2)  # Espera 2 segundos entre solicitações
   ```

### Erro: Subreddit não encontrado

**Sintoma**: Erro do tipo `prawcore.exceptions.NotFound` ou nenhuma imagem é baixada

**Solução**:
1. Verifique se o nome do subreddit está correto
2. Confirme se o subreddit existe e é público
3. Alguns subreddits podem ter restrições de idade ou conteúdo

### Erro: Nenhuma imagem encontrada

**Sintoma**: O programa executa sem erros, mas nenhuma imagem é baixada

**Solução**:
1. Verifique se o subreddit realmente contém imagens
2. Experimente aumentar o limite de posts no `config.json`
3. Tente um tipo diferente de feed (por exemplo, "new" em vez de "hot")
4. Verifique se os posts no subreddit contêm imagens diretas e não apenas links externos

## Problemas na Geração de Vídeos

### Erro: Nenhuma imagem para processar

**Sintoma**: Mensagem de erro indicando que não há imagens para processar

**Solução**:
1. Verifique se as imagens foram baixadas corretamente na pasta `images/`
2. Confirme se o formato das imagens é compatível
3. Verifique se as permissões de arquivo permitem a leitura das imagens

### Erro: Falha ao criar vídeo

**Sintoma**: Erro durante a criação do vídeo, possivelmente relacionado ao MoviePy

**Solução**:
1. Verifique se o FFmpeg está instalado e disponível no PATH
2. Certifique-se de que há espaço suficiente em disco
3. Verifique se o formato das imagens é compatível
4. Tente com menos imagens ou imagens de menor resolução
5. Verifique se há algum problema com arquivos de música

### Erro: Vídeo criado sem áudio

**Sintoma**: O vídeo é gerado, mas não tem áudio

**Solução**:
1. Verifique se a opção `add_music` está definida como `true` no `config.json`
2. Confira se a pasta `music/` contém arquivos de música válidos
3. Tente baixar a música novamente:
   ```bash
   rm -rf music/
   python -c "from meme_generator import download_background_music; download_background_music()"
   ```

### Erro: Vídeo muito grande

**Sintoma**: O vídeo gerado tem um tamanho de arquivo excessivamente grande

**Solução**:
1. Reduza o FPS no `config.json`
2. Reduza a duração por imagem
3. Use menos imagens
4. Ajuste o nível de compressão no código:
   ```python
   # Em meme_generator.py, ajuste os parâmetros de codificação
   clip.write_videofile(output_file, fps=fps, codec='libx264', preset='medium', bitrate='1000k')
   ```

## Problemas com o Banco de Dados

### Erro: Falha na conexão com o PostgreSQL

**Sintoma**: Erro do tipo `sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server`

**Solução**:
1. Verifique se o PostgreSQL está em execução:
   ```bash
   sudo systemctl status postgresql  # Linux
   brew services list  # macOS
   ```
2. Confirme se a string de conexão no `DATABASE_URL` está correta
3. Verifique se o usuário e banco de dados existem
4. Se necessário, use SQLite como fallback removendo a variável `DATABASE_URL`

### Erro: Tabela não existe

**Sintoma**: Erro do tipo `sqlalchemy.exc.ProgrammingError: relation "video" does not exist`

**Solução**:
1. Certifique-se de que o esquema do banco de dados foi criado:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```
2. Se o esquema mudou, você pode precisar migrar o banco de dados ou recriá-lo:
   ```bash
   # Recriação em PostgreSQL
   sudo -u postgres psql
   DROP DATABASE meme_videos;
   CREATE DATABASE meme_videos;
   ```

### Erro: Violação de chave única

**Sintoma**: Erro ao adicionar registros duplicados no banco de dados

**Solução**:
1. Verifique se você está tentando adicionar um registro com uma chave que já existe
2. Use uma cláusula de atualização em vez de inserção para registros existentes:
   ```python
   # Exemplo de upsert em SQLAlchemy
   from sqlalchemy.dialects.postgresql import insert
   
   stmt = insert(Video).values(path=path, subreddit=subreddit)
   stmt = stmt.on_conflict_do_update(
       index_elements=['path'],
       set_=dict(subreddit=subreddit)
   )
   db.session.execute(stmt)
   ```

## Problemas na Interface Web

### Erro: Servidor não inicia

**Sintoma**: Erro ao iniciar o servidor Flask ou Gunicorn

**Solução**:
1. Verifique se a porta não está em uso:
   ```bash
   netstat -tuln | grep 5000
   # Ou
   lsof -i :5000
   ```
2. Se a porta estiver em uso, encerre o processo ou use uma porta diferente:
   ```bash
   python run_flask.py --port 5001
   # Ou
   gunicorn --bind 0.0.0.0:5001 wsgi:app
   ```

### Erro: Vídeos não aparecem na interface

**Sintoma**: A interface web carrega, mas nenhum vídeo é listado

**Solução**:
1. Verifique se há vídeos no banco de dados:
   ```bash
   python -c "from app import app; from models import Video; with app.app_context(): print(Video.query.all())"
   ```
2. Verifique se os arquivos de vídeo existem nos caminhos especificados
3. Regenere os vídeos ou atualize os registros do banco de dados
4. Verifique os logs do servidor web para erros específicos

### Erro: Não é possível reproduzir vídeos

**Sintoma**: Os vídeos estão listados, mas não reproduzem no navegador

**Solução**:
1. Verifique se o caminho do vídeo está correto
2. Confirme se o navegador suporta o formato de vídeo (MP4 com H.264)
3. Verifique se o servidor web tem permissão para ler os arquivos de vídeo
4. Tente fazer o download do vídeo e reproduzi-lo localmente

## Problemas no Agendador

### Erro: Agendador não executa

**Sintoma**: O agendador inicia, mas não executa a geração de vídeos no intervalo configurado

**Solução**:
1. Verifique se o valor de `run_interval_minutes` no `config.json` é maior que zero
2. Confirme se o agendador ainda está em execução (pode ter sido encerrado)
3. Verifique os logs para erros durante a execução

### Erro: Execuções múltiplas

**Sintoma**: O agendador inicia múltiplas execuções da geração de vídeos simultaneamente

**Solução**:
1. Implemente um mecanismo de bloqueio para evitar execuções simultâneas:
   ```python
   # Em scheduler.py
   import os
   import time
   
   def run_with_lock():
       lock_file = "generator.lock"
       if os.path.exists(lock_file):
           print("Outra instância já está em execução")
           return
           
       try:
           with open(lock_file, "w") as f:
               f.write(str(time.time()))
           # Executar gerador aqui
       finally:
           if os.path.exists(lock_file):
               os.remove(lock_file)
   ```

## Verificação de Logs

Os logs são essenciais para diagnosticar problemas. Aqui está como usá-los efetivamente:

### 1. Logs da Aplicação

Por padrão, os logs são enviados para o console. Para salvar os logs em um arquivo:

```bash
python run.py --once > generator.log 2>&1
# ou
python run_flask.py > web.log 2>&1
```

### 2. Ativar Logs Detalhados

Para obter logs mais detalhados, você pode modificar o nível de logging nos arquivos principais:

```python
# Adicione no início dos arquivos principais
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
```

### 3. Logs do PostgreSQL

Para ver logs detalhados do PostgreSQL:

```bash
# Linux
sudo tail -f /var/log/postgresql/postgresql-*.log

# macOS (com Homebrew)
tail -f /usr/local/var/log/postgres.log
```

### 4. Logs do Flask

Para logs detalhados do Flask, ative o modo de depuração:

```python
app.debug = True
```

Ou ao iniciar o servidor:

```bash
FLASK_DEBUG=1 python run_flask.py
```

### 5. Logs do FFmpeg

Para ver logs detalhados do FFmpeg durante a geração de vídeo:

```python
# Em meme_generator.py, modifique a chamada write_videofile
clip.write_videofile(
    output_file,
    fps=fps,
    codec='libx264',
    logger=None  # Altere para None para ver todos os logs do FFmpeg
)
```

## Perguntas Frequentes

### Posso usar subreddits com restrição de idade?

Sim, mas você precisará de uma conta do Reddit que tenha confirmado idade e configurar as credenciais apropriadamente. A API do Reddit respeitará as restrições de acesso da sua conta.

### Como aumentar a qualidade dos vídeos?

Modifique a função `create_video()` em `meme_generator.py` para usar configurações de maior qualidade:

```python
clip.write_videofile(
    output_file,
    fps=fps,
    codec='libx264',
    preset='slow',  # Usa mais CPU mas melhor compressão
    bitrate='2000k'  # Bitrate mais alto
)
```

### Por que meu agendador para após algum tempo?

O agendador pode ser interrompido por vários motivos:
1. O processo foi encerrado pelo sistema (falta de memória)
2. Exceção não tratada durante a execução
3. O terminal foi fechado (se não estiver executando como serviço)

Para solucionar:
1. Execute como um serviço do sistema (ver [Configuração do Agendador](Configuracao.md#configuração-do-agendador))
2. Adicione mais tratamento de exceções
3. Use um supervisor de processo como o systemd, supervisor ou PM2

### Como adicionar minha própria música de fundo?

Simplesmente adicione arquivos MP3 na pasta `music/`. O sistema escolherá aleatoriamente entre esses arquivos quando gerar vídeos.

### Posso personalizar o formato de saída?

Sim, modifique a função `create_video()` em `meme_generator.py` para usar um codec e formato diferentes:

```python
# Para GIF em vez de MP4
clip.write_gif(output_file.replace('.mp4', '.gif'), fps=fps)

# Para WebM
clip.write_videofile(output_file.replace('.mp4', '.webm'), fps=fps, codec='libvpx')
```

### O que fazer se o Reddit bloquear meu acesso?

A API do Reddit tem limites de taxa. Se você for bloqueado:
1. Reduza a frequência de solicitações
2. Use um User-Agent mais específico
3. Considere pedir permissão ao Reddit para maior acesso à API
4. Espere algumas horas antes de tentar novamente
import time
import json
import logging
import datetime
import subprocess
import os

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    """Carrega as configurações do arquivo config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erro ao carregar configurações: {str(e)}")
        # Configurações padrão
        return {
            "subreddits": ["memes"],
            "posts_limit": 10,
            "image_duration": 3,
            "run_interval_minutes": 60,
            "fps": 30,
            "add_music": True,
            "feed_types": ["hot", "new", "top", "rising"]
        }

def run_meme_generator():
    """Executa o gerador de memes como um processo separado"""
    logger.info("Iniciando gerador de memes...")
    try:
        subprocess.run(["python", "meme_generator.py"], check=True)
        logger.info("Gerador de memes executado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao executar gerador de memes: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return False

def main():
    """Função principal que executa o scheduler"""
    logger.info("Iniciando scheduler para geração de vídeos de memes")
    
    # Carregar configuração
    config = load_config()
    interval_minutes = config.get("run_interval_minutes", 60)
    
    # Converter para segundos
    interval_seconds = interval_minutes * 60
    
    # Criar pasta de log se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")
        logger.info("Pasta de logs criada")
    
    # Execução inicial
    run_meme_generator()
    last_run = datetime.datetime.now()
    
    # Loop do scheduler
    try:
        while True:
            # Calcular o tempo desde a última execução
            current_time = datetime.datetime.now()
            elapsed = (current_time - last_run).total_seconds()
            
            # Verificar se é hora de executar novamente
            if elapsed >= interval_seconds:
                logger.info(f"Intervalo de {interval_minutes} minutos atingido. Executando novamente...")
                run_meme_generator()
                last_run = current_time
            
            # Mostrar tempo restante a cada 5 minutos
            if int(elapsed) % 300 == 0:
                remaining = interval_seconds - elapsed
                logger.info(f"Próxima execução em {int(remaining / 60)} minutos e {int(remaining % 60)} segundos")
            
            # Aguardar um pouco para não sobrecarregar a CPU
            time.sleep(10)
    
    except KeyboardInterrupt:
        logger.info("Scheduler interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro no scheduler: {str(e)}")

if __name__ == "__main__":
    main()
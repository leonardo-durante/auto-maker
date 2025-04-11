#!/usr/bin/env python
import argparse
import logging
import sys
import os
import subprocess

# Configurar logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    # Verificar se precisamos carregar as variáveis de ambiente do arquivo .env
    from dotenv import load_dotenv
    load_dotenv()
    
    required_env_vars = ['ID', 'SECRET', 'AGENT']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variáveis de ambiente necessárias não encontradas: {', '.join(missing_vars)}")
        logger.error("Por favor, crie um arquivo .env com as credenciais do Reddit:")
        logger.error("ID=seu_reddit_client_id")
        logger.error("SECRET=seu_reddit_client_secret")
        logger.error("AGENT=seu_reddit_user_agent")
        return False
    
    # Verifica se o arquivo config.json existe
    if not os.path.exists('config.json'):
        logger.error("Arquivo config.json não encontrado")
        logger.error("Criando arquivo config.json com configurações padrão...")
        import json
        default_config = {
            "subreddits": ["memes", "dankmemes", "wholesomememes"],
            "posts_limit": 10,
            "image_duration": 3,
            "run_interval_minutes": 60,
            "fps": 30,
            "add_music": True,
            "feed_types": ["hot", "new", "top", "rising"]
        }
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
        logger.info("Arquivo config.json criado com sucesso")
    
    return True

def run_once():
    """Executa o gerador de memes uma vez"""
    logger.info("Executando gerador de memes uma vez...")
    try:
        subprocess.run(["python", "meme_generator.py"], check=True)
        return True
    except Exception as e:
        logger.error(f"Erro ao executar: {str(e)}")
        return False

def run_scheduler():
    """Inicia o programador que executará o gerador periodicamente"""
    logger.info("Iniciando programador...")
    try:
        subprocess.run(["python", "scheduler.py"], check=True)
        return True
    except Exception as e:
        logger.error(f"Erro ao executar programador: {str(e)}")
        return False

def parse_arguments():
    """Processa os argumentos da linha de comando"""
    parser = argparse.ArgumentParser(
        description='Gerador de vídeos de memes do Reddit',
        epilog='Exemplo: python run.py --once para executar uma vez ou python run.py --scheduler para executar periodicamente'
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--once', action='store_true', help='Executa o gerador uma vez')
    group.add_argument('--scheduler', action='store_true', help='Inicia o programador que executará o gerador periodicamente')
    
    return parser.parse_args()

def main():
    """Função principal"""
    # Verificar ambiente
    if not check_environment():
        sys.exit(1)
    
    # Processar argumentos
    args = parse_arguments()
    
    # Executar de acordo com o modo escolhido
    if args.once:
        success = run_once()
    elif args.scheduler:
        success = run_scheduler()
    
    # Retornar código de saída apropriado
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Programa interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        sys.exit(1)
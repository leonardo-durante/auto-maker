from web_app import app

if __name__ == "__main__":
    # Inicializar o servidor Flask
    print("Iniciando servidor Flask na porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
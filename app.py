from app import create_app

# Vercel cherchera cette variable globale "app" pour lancer le serveur
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

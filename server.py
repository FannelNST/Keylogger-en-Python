# Importer Flask depuis le module flask
from flask import Flask, request

# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir une route pour recevoir les logs via une requête POST
@app.route('/receive_logs', methods=['POST'])
def receive_logs():
    # Récupérer les logs envoyés dans la requête
    logs = request.form.get('logs')
    # Si des logs sont présents, les écrire dans un fichier
    if logs:
        with open('received_logs.txt', 'a', encoding='utf-8') as file:
            file.write(logs + '\n')
        return 'Logs received successfully!', 200
    else:
        return 'No logs received!', 400

# Démarrer l'application Flask en mode debug
if __name__ == '__main__':
    app.run(debug=True)

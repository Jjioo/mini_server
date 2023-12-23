from flask import Flask, render_template, request, jsonify
from colorama import Fore, Style, init
import logging
import threading

app = Flask(__name__)

# Set the log level to a higher value to suppress log messages
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Store messages in memory
chat_messages = []

# Initialize colorama
init(autoreset=True)

def print_colored_message(name, message, color=Fore.WHITE):
    # Print in the cmd with colors
    print(f"{color}{name} {Fore.WHITE}{message}")

def send_server_message(message):
    # Print in the cmd with colors
    print_colored_message("Server :", message, Fore.BLUE)

    # Add the message to the chat_messages list
    chat_messages.append({'name': '🍕Server: ', 'message': message})

def send_user_message(name, message, add_to_chat=True):
    # Check if the message is not empty and not a duplicate
    if message and (not chat_messages or message != chat_messages[-1]['message']):
        # Print in the cmd with colors
        print_colored_message(f'🌟 {name} says:', message, Fore.GREEN)

        # Add the message to the chat_messages list only if add_to_chat is True
        if add_to_chat:
            chat_messages.append({'name': f'🌟 {name} says: ', 'message': message})



# Thread function to listen for messages from the command line
def command_line_listener():
    while True:
        try:
            message = input("")
            if message.lower() == 'exit':
                # Optionally add a condition to gracefully exit the thread
                break
            send_server_message(message)
        except KeyboardInterrupt:
            # Handle KeyboardInterrupt (Ctrl+C) to exit the thread gracefully
            break

# Start the command line listener thread
cmd_listener_thread = threading.Thread(target=command_line_listener, daemon=True)
cmd_listener_thread.start()

@app.route('/')
def index():
    return render_template('index.html', messages=[{'name': '🍕Server: ', 'message': 'hey'}, {'name': '🍕Server: ', 'message': 'qsd'}] + chat_messages)

# Route to fetch updates
@app.route('/fetch_updates')
def fetch_updates():
    return jsonify(chat_messages)

# Route to send messages from users
@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    message = request.form.get('message')

    # Skip adding the message to the list if it's a debug message
    if name != "fgfg" and message != "fg":
        # Add the message to the chat_messages list
        send_user_message(name, message)

    # Return the updated messages
    return jsonify(chat_messages)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) to exit the application gracefully
        pass
    finally:
        # Ensure that the command line listener thread is stopped when the application exits
        cmd_listener_thread.join()

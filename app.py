from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from PasswordGenerator import Generate
import asyncio, time, os, datetime

# if os.path.exists('__pycache__'):
#     os.remove('__pycache__')

dt = datetime.datetime

delay = 0 # Задержка перед остоновкой
show_safe_code = False
enable_log_messages = False # Включить логирование сообщений
# http://95.31.8.49:5001/ - http://127.0.0.1:5001/


safe_code = Generate(100, 100, use_all_symbols=True) # Safe_code strong generator

if show_safe_code:
    print(f'Ваш код шифрования: {safe_code}')

HOST = ''
PORT = input('Введите порт (5001): ')
GLOBAL = input('Введите если хотите использовать глобальный режим (y or anything else): ').lower()

if GLOBAL == 'y':
    HOST = '0.0.0.0'
else:
    HOST = '127.0.0.1'

if PORT == '':
    PORT = 5001

PORT = int(PORT)

# Создаем экземпляр Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = f'{safe_code}'

# Создаем экземпляр SocketIO с использованием eventlet
socketio = SocketIO(app, async_mode='eventlet')

# Список для хранения сообщений
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('send_message')
def handle_message(data):
    if enable_log_messages:
        print(data)

    if str(data['message']).lower() == 'стоп':
        # {'author': 'Система', 'message': f'Чат быдет остановлен через {delay} секунд.'}
        # emit('receive_message', {'author': 'Система', 'message': f'Чат быдет остановлен через {delay} секунд.'}, broadcast=True)
        print(f'Stopping chat after {delay} secs!')
        exit_save()
    elif str(data['message']).lower() == 'очистить':
        print(f'Stopping chat after {delay} secs!')
        messages.clear()
        emit('receive_message', {'author': 'Система', 'message': f'Чат очищен.'}, broadcast=True)
        emit('reload', broadcast=True)
    elif str(data['message']).lower() == 'релоад':
        emit('reload', broadcast=True)
    else:
        msg = f'{dt.now().hour}:{dt.now().minute}| {data["message"]}'

        data = {'author': data['author'], 'message': msg}
        emit('receive_message', data, broadcast=True)
    
    # Сохраняем сообщение и автора
    messages.append(data)

def exit_save():
    time.sleep(delay)
    exit()

if __name__ == '__main__':
    if GLOBAL == 'y':
        print(f'Server running on http://your_global_ip:{PORT}')
    else:
        print(f'Server running on http://{HOST}:{PORT}')
    # Запускаем приложение с использованием eventlet
    socketio.run(app, host=HOST, port=PORT, debug=False)
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from PasswordGenerator import Generate
import datetime
from AvirtCrypto import AvirtCrypto

# if os.path.exists('__pycache__'):
#     os.remove('__pycache__')

dt = datetime.datetime
crypto = AvirtCrypto()

#delay = 0 # Задержка перед остоновкой
show_safe_code = False
enable_log_messages = False # Включить логирование сообщений (они будут всёравно зашифрованы)
# http://95.31.8.49:5001/ - http://127.0.0.1:5001/


safe_code = Generate(100, 100, use_all_symbols=True) # Safe_code strong generator

if show_safe_code:
    print(f'Ваш код шифрования flask: {safe_code}')

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
    return '''
<center style="margin-top: 50vh;"><a href="/chat" style="border: none; color: white; font-size: 50px; padding: 25px; text-decoration: none; background-color: rgb(0, 140, 255); transition: .3s; border-radius: 1.7vh; user-select: none;">Открыть чат</a></center>
'''

@app.route('/chat')
def chat():
    return render_template('chat.html', messages=messages)

@socketio.on('send_message')
def handle_message(data):
    append = True

    data['message'] = str(data['message'])
    
    data['message'] = crypto.decode(data['message'])

    js_script = str(data['message']).split('|')

    if enable_log_messages:
        print(data)

    if str(data['message']).lower() == 'стоп':
        # {'author': 'Система', 'message': f'Чат быдет остановлен через {delay} секунд.'}
        # emit('receive_message', {'author': 'Система', 'message': f'Чат быдет остановлен через {delay} секунд.'}, broadcast=True)
        print(f'Chat stopped')
        exit_save()
    elif str(data['message']).lower() == 'очистить':
        messages.clear()
        emit('receive_message', {'author': 'Система', 'message': f'Чат очищен.'}, broadcast=True)
        emit('reload', broadcast=True)
    elif str(data['message']).lower() == 'релоад':
        append = False
        emit('reload', broadcast=True)
    elif js_script[0].lower() == 'command':
        append = False
        emit('command', js_script[1], broadcast=True)
    else:
        #msg = f'{dt.now().hour}:{dt.now().minute}| {data["message"]}'

        #data = {'author': data['author'], 'message': crypto.decode(data['message'])}
        emit('receive_message', data, broadcast=True)
    
    if append:
        # Сохраняем сообщение и автора
        data['message'] = crypto.encode(data['message'])
        messages.append(data)

def exit_save():
    exit()

if __name__ == '__main__':
    if GLOBAL == 'y':
        print(f'Server running on http://your_global_ip:{PORT}')
    else:
        print(f'Server running on http://{HOST}:{PORT}')
    # Запускаем приложение с использованием eventlet
    socketio.run(app, host=HOST, port=PORT, debug=False)
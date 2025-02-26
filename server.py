import socket
from threading import Thread

# Настройки сервера
HOST = '127.0.0.1'  # Локальный хост
PORT = 65432        # Порт для соединения
clients = {}        # Словарь для хранения подключенных клиентов

def broadcast(message, sender):
    """Отправка сообщения всем подключенным клиентам."""
    for client_socket in clients:
        if client_socket != sender:  # Не отправлять сообщение самому себе
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

def handle_client(client_socket, address):
    """Обработка клиента."""
    try:
        # Получаем имя пользователя
        username = client_socket.recv(1024).decode('utf-8')
        print(f"{address} присоединился как {username}")
        clients[client_socket] = username

        # Уведомляем всех о новом участнике
        welcome_message = f"{username} присоединился к чату!"
        broadcast(welcome_message.encode('utf-8'), None)

        while True:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Получено сообщение от {username}: {message.decode('utf-8')}")
            broadcast(f"{username}: {message.decode('utf-8')}".encode('utf-8'), client_socket)
    except Exception as e:
        print(f"Ошибка с клиентом {username}: {e}")
    finally:
        # Удаляем клиента из списка и уведомляем других
        del clients[client_socket]
        client_socket.close()
        goodbye_message = f"{username} покинул чат."
        broadcast(goodbye_message.encode('utf-8'), None)
        print(f"{username} отключился.")

def start_server():
    """Запуск сервера."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        print(f"Подключение от {address}")
        Thread(target=handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    start_server()
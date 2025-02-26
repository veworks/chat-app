import socket

# Настройки клиента
HOST = '69cb8057-1e44-40f4-97b5-4d34ffa0504f-00-2sw5wvcs5ggw3.pike.replit.dev'  # Замените на ваш URL
PORT = 65432

# Создаем сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        # Подключаемся к серверу
        client_socket.connect((HOST, PORT))
        print(f"Подключено к {HOST}:{PORT}")

        # Отправляем имя пользователя
        username = input("Введите ваше имя: ")
        client_socket.sendall(username.encode('utf-8'))

        # Обмен сообщениями
        while True:
            message = input("Введите сообщение: ")
            if message.lower() == "exit":
                break
            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024).decode('utf-8')
            print(f"От сервера: {data}")
    except Exception as e:
        print(f"Ошибка: {e}")
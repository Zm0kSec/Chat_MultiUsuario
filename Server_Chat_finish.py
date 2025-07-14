from socket import *
from threading import *
import ssl
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

clients = set()
connected_users = {}
diccionario = {}

# Email Credentials (IMPORTANT: Use environment variables or a secure config in production)
EMAIL_SERVER = "email de servidor a usar"
EMAIL_PASS = "clave de aplicacion"

def client_thread(ssl_socket, client_address):
    username = None
    try:
        # 1. Receive Username and Check for Duplicates
        username = ssl_socket.recv(1024).decode("utf-8")
        if username in connected_users:
            ssl_socket.send("ERROR_USERNAME_TAKEN".encode("utf-8"))
            print(f"Duplicate username connection attempt: {username} from {client_address}")
            ssl_socket.close()
            return
        
        ssl_socket.send("USERNAME_ACCEPTED".encode("utf-8"))
        connected_users[username] = ssl_socket
        clients.add(ssl_socket)

        # 2. Receive Email for Notifications
        email = ssl_socket.recv(1024).decode("utf-8")
        test_email_regex = r"\b[A-Za-z-0-9._+-]+@[A-Za-z0-9]+\.[A-Za-z]{2,}\b"
        if email and re.findall(test_email_regex, email):
            diccionario[username] = email

        # 3. Notify Clients About Connection
        ssl_socket.send((f"Usuarios conectados: {len(connected_users)}\n").encode("utf-8"))
        for user_name_in_chat, client_sock_in_chat in connected_users.items():
            if client_sock_in_chat is not ssl_socket:
                try:
                    client_sock_in_chat.send(f"--- {username} se ha conectado al chat. ---".encode("utf-8"))
                except Exception as e:
                    print(f"Error notifying {user_name_in_chat}: {e}")

        print(f"User {username} connected from {client_address[0]}:{client_address[1]}")
        print(f"Active users: {list(connected_users.keys())}")

        # Main Message Handling Loop
        while True:
            msg = ssl_socket.recv(2048).decode("utf-8")
            if not msg: # Client disconnected
                print(f"User {username} disconnected.")
                break

            # Message Processing Logic
            if msg.startswith("Says:"):
                full_message = f"{username} {msg}"
                print(f"Chat: {full_message}")
                for user_name_in_chat, client_sock_in_chat in connected_users.items():
                    if client_sock_in_chat is not ssl_socket: # Do not send back to sender
                        try:
                            client_sock_in_chat.send(full_message.encode("utf-8"))
                        except Exception as e:
                            print(f"Error relaying message to {user_name_in_chat}: {e}")

            elif msg.startswith("NOTIFY:"):
                target_cmd = msg[len("NOTIFY:"):].strip()

                if target_cmd == "GENERAL":
                    print(f"GENERAL notification initiated by {username}")
                    for user_email_key, from_user_email in diccionario.items():
                        try:
                            msg_smtp = MIMEMultipart()
                            msg_smtp['From'] = EMAIL_SERVER
                            msg_smtp['To'] = from_user_email
                            msg_smtp['Subject'] = 'AnonChat Notification (General)'
                            body = f"¡Una notificación general de AnonChat! {username} ha enviado una alerta a todos. Conéctate."
                            msg_smtp.attach(MIMEText(body, 'plain'))
                            server_smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server_smtp.login(EMAIL_SERVER, EMAIL_PASS)
                            server_smtp.sendmail(EMAIL_SERVER, msg_smtp['To'], msg_smtp.as_string())
                            server_smtp.quit()
                            print(f"General notification email sent to {user_email_key} ({from_user_email}).")
                        except Exception as e:
                            print(f"Error sending general email to {user_email_key}: {e}")
                            ssl_socket.send(f"ERROR: No se pudo enviar notificación a {user_email_key} ({e})".encode("utf-8"))

                elif target_cmd in diccionario:
                    target_email = diccionario[target_cmd]
                    print(f"Notification to {target_cmd} initiated by {username}")
                    try:
                        msg_smtp = MIMEMultipart()
                        msg_smtp['From'] = EMAIL_SERVER
                        msg_smtp['To'] = target_email
                        msg_smtp['Subject'] = 'AnonChat Notification'
                        body = f"¡{username} te ha enviado una notificacion desde AnonChat! Conéctate."
                        msg_smtp.attach(MIMEText(body, 'plain'))
                        server_smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        server_smtp.login(EMAIL_SERVER, EMAIL_PASS)
                        server_smtp.sendmail(EMAIL_SERVER, msg_smtp['To'], msg_smtp.as_string())
                        server_smtp.quit()
                        print(f"Notification email sent to {target_cmd} ({target_email}).")
                        ssl_socket.send(f"Notificación enviada a {target_cmd}.".encode("utf-8"))
                    except Exception as e:
                        print(f"Error sending email to {target_cmd}: {e}")
                        ssl_socket.send(f"ERROR: No se pudo enviar notificación a {target_cmd} ({e})".encode("utf-8"))
                else:
                    error_msg = f"Notification command '{target_cmd}' or user not valid for notification."
                    print(error_msg)
                    ssl_socket.send(error_msg.encode("utf-8"))
            
            else:
                error_user = "Mensaje no reconocido. Use 'Says: <tu_mensaje>' para chatear o 'NOTIFY:<usuario>'/'NOTIFY:GENERAL' para notificar."
                ssl_socket.send(error_user.encode("utf-8"))

    except Exception as e:
        print(f"Error in client thread {username if username else 'unknown'}: {e}")
    
    finally:
        # Cleanup on thread exit
        if ssl_socket in clients:
            clients.remove(ssl_socket)
        if username and username in connected_users:
            del connected_users[username]

        print(f"User {username if username else 'unknown'} disconnected.")
        print(f"Remaining active users: {list(connected_users.keys())}")

        # Notify other clients of disconnection
        for user_name_in_chat, client_sock_in_chat in connected_users.items():
            try:
                client_sock_in_chat.send(f"--- {username if username else 'Un usuario'} se ha desconectado del chat. ---".encode("utf-8"))
            except Exception as e:
                print(f"Error notifying disconnection to {user_name_in_chat}: {e}")
        
        ssl_socket.close()

# Server SSL Configuration
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="./server-cert.pem", keyfile="./server-key.key")

host_socket = socket(AF_INET, SOCK_STREAM)
host_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

host = "127.0.0.1"
port = 4488

host_socket.bind((host, port))
host_socket.listen()

print("Waiting for connection")

while True:
    client_socket, client_address = host_socket.accept()
    ssl_socket = context.wrap_socket(client_socket, server_side=True)
    
    print(f"Connection attempt from {client_address[0]}:{client_address[1]}")
    thread = Thread(target=client_thread, args=(ssl_socket, client_address,))
    thread.start()
import socket
from Crypto.Cipher import AES


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))
K3 = b"1234567890123456"
IV_initial = "0123456789012345"

try:
    data = client_socket.recv(1024).decode("utf-8")
    if data == "CFB":
        print("Received from server:", data)
        client_socket.send(bytes("B: Am primit CFB.", "utf-8"))

        enc_K2 = client_socket.recv(1024)
        enc_IV2 = client_socket.recv(1024)

        aes = AES.new(K3, AES.MODE_CBC, IV_initial.encode("utf-8"))
        K2 = aes.decrypt(enc_K2)
        aes = AES.new(K3, AES.MODE_CBC, IV_initial.encode("utf-8"))
        IV2 = aes.decrypt(enc_IV2)
        print(K2)
        print(IV2)

        confirm = "B: Putem incepe."
        aes = AES.new(K2, AES.MODE_CBC, IV2)
        confirm = aes.encrypt(bytes(confirm, "utf-8"))
        client_socket.send(confirm)

    # message = input("Send a character to the server:")
    # client_socket.send(bytes(message, "utf-8"))
except KeyboardInterrupt:
    print("Exited by user.")
client_socket.close()

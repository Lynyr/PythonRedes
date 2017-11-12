import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 5151

def gerenciador_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)

    print "Servidor iniciou na porta " + str(PORT)

    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Cliente (%s, %s) conectou" % addr

                broadcast(server_socket, sockfd, "[%s:%s] entrou no chat\n" % addr)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        broadcast(server_socket, sock, "Cliente (%s, %s) esta offline\n" % addr)
                except:
                    broadcast(server_socket, sock, "Cliente (%s, %s) esta offline\n" % addr)
                    continue

    server_socket.close()

# Envia mensagens de um fclient para todos os demais conectados
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # Desligar socket
                socket.close()
                # Remover socket desligado
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":

    sys.exit(gerenciador_server())

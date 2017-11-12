import sys
import socket
import select

def main():
    print('1 - Conectar ao servidor')
    print('2 - Conectar ao cliente')
    opt = input()
    if opt==1:
        serv()
    elif opt==2:
        cliente()
    else:
        main()

def serv():

    host = raw_input("Escolha o IP do servidor: ")
    port = input("Escolha a porta do servidor: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
    except :
        print 'Nao e possivel se conectar'
        sys.exit()

    print 'Conectado'
    sys.stdout.write('[Eu] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDesconectado do servidor'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('[Eu] '); sys.stdout.flush()

            else :
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Eu] '); sys.stdout.flush()

    if __name__ == "__main__":

        sys.exit(serv())


def cliente():

    host = raw_input("Escolha o IP do servidor: ")
    port = input("Escolha a porta do servidor: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try :
        s.connect((host, port))
    except :
        print 'Nao e possivel se conectar'
        sys.exit()

    print 'Conectado'
    sys.stdout.write('[Eu] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDesconectado do servidor'
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('[Eu] '); sys.stdout.flush()

            else :
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Eu] '); sys.stdout.flush()

    if __name__ == "__main__":

        sys.exit(cliente())

main()

import threading
import socket

#Função 'main()' que será chamada no arquivo servidor.py, ela contém toda a conexão do socket(da parte do cliente) com o servidor
def main():

    #Cria um socket TCP/IP para o cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Input da porta que o cliente deseja conectar
    porta = int(input('Digite uma porta para conexão: '))

    try:
        #Conexão com o servidor utilizando a porta que foi digitada
        endereco_servidor = ('localhost', porta)
        cliente.connect(endereco_servidor)
        print('Conectando-se à rede \nNome: {} \nPorta: {} '.format(*endereco_servidor))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    #Nome do usuário
    nomeUser = input('Usuário: ')
    print('\nConectado')

    #Thread1 para mensagens recebidas(Juntando a mensagem recebida com o nome do usuário)
    thread1 = threading.Thread(target=recebiMensagens, args=[cliente])

    #Thread2 para mensagens enviadas(envia a mensagem junto com o nome do usuário)
    thread2 = threading.Thread(target=envioMensagens, args=[cliente, nomeUser])

    #Inicio das threads
    thread1.start()
    thread2.start()


#Função para recebimento de mensagens
def recebiMensagens(cliente):
    #While para recebimento e print de mensagem, enquanto o cliente não retornar um erro
    while True:
        try:
            #recv recebe dados de um socket conectado
            #decode serve para descodificar uma string(já codificada), no caso para 'utf-8'
            mensagem = cliente.recv(2048).decode('utf-8')
            print(mensagem+'\n')


        #Tratamento de erro(Se a variavel cliente retornar um erro)
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            cliente.close()
            break
            
#Função para envio de mensagens
def envioMensagens(cliente, nomeUser):
    #While para envio e print de mensagens, em caso de erro não retorna nada
    while True:
        try:
            mensagem = input('\n')
            #encode serve para codificar uma string, no caso para 'utf-8'
            cliente.send(f'<{nomeUser}> {mensagem}'.encode('utf-8'))

        except:
            return


main()

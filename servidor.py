#Threads são utilizadas para que seja possível realizar múltiplas tarefas simultaneamente, no caso dessa aplicação ela é utilizada para que mais de dois usuários possam se comunicar simultanemente
import threading
import socket

#Vetor que armazenara os clientes conectados no servidor
clientes = []

def main():

    #Cria o socket TCP/IP para o servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Input de uma porta para criação do servidor
    porta = int(input('Digite uma porta para o servidor(Recomendado 10000): '))

    try:

        #Define a variavel 'endereco_servidor' com o endereço do servidor para conexão
        endereco_servidor = ('localhost', porta)

        #O comando bind associa um endereço a um socket, no caso está associando a variavel 'endereco_servidor'
        server.bind(endereco_servidor)

        #Escuta de conexão do servidor, para sockets que tentarem se conectar
        server.listen()
    except:

        #Retorno de erro sobre a conexão do servidor
        return print('Não foi possível iniciar o servidor!')


    print('Servidor Iniciado! \nAguardando Conexões...')

    #While para aceitar a conexão dos sockets, mostrar qual usuário conectou e adiciona-lo a uma thread
    while True:

        #.accept() aceita as conexões dos sockets que tentarem conectar
        cliente, cliente_address = server.accept()

        print('Usuário conectado:',cliente_address)

        #Adiciona o cliente à lista
        clientes.append(cliente)

        #Thread juntando a função
        thread = threading.Thread(target=tratamentoMsg, args=[cliente])
        thread.start()

#Função para tratamento de mensagem
def tratamentoMsg(cliente):
    while True:
        try:
            #recv recebe dados de um socket conectado, no caso recebendo até 2048 bytes
            msg = cliente.recv(2048)
            #Depois de receber os dados ele manda para a função 'veriTransmissão' que verfica os clientes conectados
            veriTransmissão(msg, cliente)
        #Se houver algum erro com o 'cliente' ele será excluido
        except:
            deleteCliente(cliente)
            break


#Verificação dos clientes presentes no vetor 'clients', se o cliente estiver presente nesse vetor sua mensagem será enviada senão o cliente será deletado
def veriTransmissão(msg, cliente):
    for clienteItem in clientes:
        if clienteItem != cliente:
            try:
                clienteItem.send(msg)

            except:
                deleteCliente(clienteItem)

#Função para deletar um cliente(Está sendo utilizada para a função 'broadcast')
def deleteCliente(cliente):
    clientes.remove(cliente)

#Chama a função 'def main()' presente no arquivo cliente.py
main()
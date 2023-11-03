import grpc
import numbersApi_pb2_grpc as pb2_grpc
import numbersApi_pb2 as pb2


def make_message(number):
    '''
        Converte o inteiro de entrada no tipo específico
    '''
    return pb2.InputNumber(
        a=int(number)
    )

def generate_messages():
    '''
        Gera uma combinação de mensagens para serem enviadas ao servidor.
    '''
    messages = [
        make_message(1),
        make_message(2),
        make_message(3),
        make_message(0),
        make_message(4),
        make_message(5),
    ]

    for msg in messages:
        print(f">>>> Sending number: {msg.a}")
        yield msg


def send_message(stub):
    '''
        Envia as mensagens para o servidor e processa o retorno.
    '''
    responses = stub.CalculateUntilZero(generate_messages())
    for response in responses:
        print(f">>>> Receiving result: {response.result}")


def run():
    '''
        Inicializa o cliente bidirecional.
    '''
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.NumbersApiStub(channel)
        send_message(stub)


if __name__ == '__main__':
    run()
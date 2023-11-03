import grpc
from concurrent import futures
import time
import numbersApi_pb2_grpc as pb2_grpc
import numbersApi_pb2 as pb2


class NumbersApiService(pb2_grpc.NumbersApiServicer):
    '''
        Classe de implementação da inteface da API.
    '''

    def __init__(self, *args, **kwargs):
        pass
    
    def SumNumbers(self, request, context):
        '''
            Realiza a soma de dois números.
        '''
        sum = request.a + request.b
        return pb2.Number(result=sum)


    def ListNumbers(self, request, context):
        '''
            Retorna uma lista contida no intervalo dado: [a, b]
        '''
        for i in range(request.a, request.b + 1):
            yield pb2.Number(result=i)


    def CalculateUntilZero(self, request_iterator, context):
        '''
            Calcula o quadrado de um número até que ele seja igual a zero.
        '''
        for request in request_iterator:
            if request.a == 0:
                break

            yield pb2.Number(result=request.a ** 2)
            

def serve():
    '''
        Método responsável pela inicialização do servidor
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_NumbersApiServicer_to_server(NumbersApiService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started, listening on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
import boto3
import json

class Fila:
    def __init__(self):
        self.sqs = boto3.client('sqs') # Crie o cliente SQS.
        
    def criar(self, queue_name):
        # Crie uma fila SQS
        response = self.sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                'DelaySeconds': '60',
                'MessageRetentionPeriod': '86400'
            }
        )
        
        return response
        
    def listar_filas(self):
        # Lista sqs filas.
        response = self.sqs.list_queues()
        
        return response['QueueUrls']
    
    def url(self, queue_name):
        response = self.sqs.get_queue_url(QueueName=queue_name)

        return response['QueueUrl']
   
    def deletar(self, queue_name):
        # Excluir sqs fila
        response=self.sqs.delete_queue(QueueUrl=queue_name)
        
        return response
        
    def enviar_msg(self, queue_url, msg):
        # Enviando mensagem para a fila SQS
        response = self.sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=5,
            MessageBody=msg
        )
        
        return response['MessageId']
        
    def ler_msg(self, queue_url, MaxNumberOfMessages=1):
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=MaxNumberOfMessages,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        
        return response['Messages']
        
if __name__ == '__main__':
    fila = Fila()
    nome = 'teste_exercicio1'
    
    print(json.dumps(fila.criar(nome), indent=4))
    url = fila.url(nome)
    
    for num in range(1, 10):
        fila.enviar_msg(url, (f'msg: {num} Olá, Mundo'))
       
    
    messages = fila.ler_msg(url, 10)
    print(json.dumps(messages, indent=4))
    for msg in messages:
        print(msg['Body'])
    
    
    #fila.deletar(nome)
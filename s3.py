import json

from fila import Fila

fila = Fila()
nome = 'teste_exercicio1'
url = fila.url(nome)


def handler(event, context):
    msg = {
        "bucket": event['Records'][0]['s3']['bucket']['name'],
        "chave": event['Records'][0]['s3']['object']['key']
    }
    
    print(fila.enviar_msg(url, json.dumps(msg)))
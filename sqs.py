import json

from s3_utils import delete_file
from fila import Fila

fila = Fila()
nome = 'teste_exercicio1'
url = fila.url(nome)

def handler(event, context):
    msg = json.loads(event['Records'][0]['body'])
    
    print(json.dumps(msg, indent=4))
    
    delete_file(msg['bucket'], msg['chave'])
    
    
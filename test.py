import boto3
import json
import re

from dynamo import BaseDAO
from decimal import Decimal

#class DecimalEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            return int(o)
#        return super(DecimalEncoder, self).default(o)
        

client = boto3.client('s3')
dy = BaseDAO('votos')

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = re.sub('\D{0,100}\/', '', event['Records'][0]['s3']['object']['key'])
    file_content = client.get_object(Bucket=bucket, Key=object_key)["Body"].read()

    votos = json.loads(file_content)
    items_dy = dy.scan_table_allpages()
    
    if items_dy:
        print(json.dumps(items_dy, default=str))
    else:
        totaldevotos = 0
        items = []
        
        for candidato in votos['votos']:
            totaldevotos += votos['votos'][candidato]
            items.append({
                'candidato': candidato,
                'total': votos['votos'][candidato]
            })
        
        items.append({
            'candidato': 'totaldevotos',
            'total': totaldevotos
        })
        
        create_items(items)
    
    
def create_items(items):
    for item in items:
        dy.put_item(item)


if __name__ == '__main__':
    votos = {
        "votos":{
            "candidato1": 3,
            "candidato2": 4
        }
    }
        
    totaldevotos = 0
    items = []
    
    for candidato in votos['votos']:
        totaldevotos += votos['votos'][candidato]
        items.append({
            'candidato': candidato,
            'total': votos['votos'][candidato]
        })
    
    items.append({
        'candidato': 'totaldevotos',
        'total': totaldevotos
    })
    
    #print(json.dumps(items, indent=4))
    
    
    items_dy = [{'total': Decimal('7'), 'candidato': 'totaldevotos'}, {'total': Decimal('3'), 'candidato': 'candidato1'}, {'total': Decimal('4'), 'candidato': 'candidato2'}]
    
    
    for c in items_dy:
        for k, v in c.items():
            print(k, v)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
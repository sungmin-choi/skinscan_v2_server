import json
import boto3

# DynamoDB 서비스 리소스를 초기화합니다.
dynamodb = boto3.resource('dynamodb')

# 사용할 DynamoDB 테이블 이름을 정의합니다.
table_name = 'skinscan_products_dynamoDB'

# DynamoDB 테이블 객체를 가져옵니다.
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = json.loads(event['body'])
    print(body['product_id'])   # 기본값으로 빈 JSON 객체를 문자열로 설정

    item = {
        'product_id': body['product_id'],
        'title': body['title'],
        'product_analytics': body['product_analytics'],
        'product_info': body['product_info']
        
    }
    table.put_item(Item=item)
    
    
    # 응답 객체를 반환합니다.
    
    return {
        "status": 201
    }
    
    
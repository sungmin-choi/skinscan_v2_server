import json
import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import boto3


url = 'https://incidecoder.com/products/'

# DynamoDB 서비스 리소스를 초기화합니다.
dynamodb = boto3.resource('dynamodb')
table_name = 'skinscan_products_dynamoDB'

table = dynamodb.Table(table_name)

def getProductInfo(link):
    page = requests.get(url+link)

    soup = bs(page.text, "html.parser")

    result = OrderedDict()
    title = soup.select('#product-title')[0].text
    img_url = soup.select('#product-main-image > picture > img')[0].get('src')
    brand_name = soup.select('#product-brand-title > a')[0].text
    prouduct_description=soup.select('#product-details')[0].text.replace('\n', '')
    update_info=soup.select('#content > div.detailpage > div.std-side-padding.paddingtl > div.prodinfobox.prodnexttoimage.fleft > div > div.fs12')[0].text

    ingredients=soup.select('#showmore-section-ingredlist-short > div > span')

    result['title']=title
    result['img_url']=img_url
    result['brand_name']=brand_name
    result['prouduct_description']=prouduct_description
    result['update_info'] = update_info
    ingredients_text=''

    for ingredient in ingredients:
        ingredients_text+=ingredient.text

    result['ingredients'] = ingredients_text.replace(' ','').replace("\n", "").replace('[more]','')
    return result




def lambda_handler(event, context):
    try:
        res=''
        exist=False
        query=''
        queryStringParameters = event.get("queryStringParameters", {})
        keyword=queryStringParameters.get("query")
        
        if keyword is not None:
            query=query+keyword
            
        
        response = table.get_item(
            Key={
                'product_id':query
            }
        )
        # item = response.get('Item', None)
        item = response['Item']

        if item is None:
            res = getProductInfo(query)
        else:
            exist=True
            res=item
        
        
        return {
                'statusCode': 200,
                'body': json.dumps({'data':res, 'exist': exist})
                }
    except Exception as e:
            return {
            'statuscode': 500,
            'body': str(e)
            }
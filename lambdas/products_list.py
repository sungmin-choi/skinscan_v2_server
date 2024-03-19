import json
import requests
from bs4 import BeautifulSoup as bs
from collections import OrderedDict

search_url = 'https://incidecoder.com/search?query='


def getProductsList(keyword):
        result = OrderedDict()
        page = requests.get(search_url+keyword)


        soup = bs(page.text, "html.parser")

        elements = soup.select('#products > div.paddingbl > a.simpletextlistitem')

        elements2 = soup.select('#products > div.paddingbl.center.fs16 > a')

        products = []

        route_pages = []

        

        for index, element in enumerate(elements, 1):
                product = {
                        'id':element.get('href').replace("/products/", ""),
                        'title': element.text,
                        'url': element.get('href')
                }

                products.append(product)

        result['products'] = products

        for index, element in enumerate(elements2):
                route_page = {
                        'id':index,
                        'title': element.text,
                        'url': element.get('href').replace("/search?query=","")
                }

                route_pages.append(route_page)

        result['route_pages'] = route_pages
        

        return result


def lambda_handler(event, context):
        try:
                query=''
                queryStringParameters = event.get("queryStringParameters", {})
                
                
                keyword=queryStringParameters.get("query")
                page = queryStringParameters.get("ppage")
                activetab= queryStringParameters.get("activetab")
                
            
                if keyword is not None:
                        query=query+keyword
                if activetab is not None:
                        query=query+'&activetab='+event["queryStringParameters"]["activetab"]
                if page is not None:
                        query=query+'&ppage='+event["queryStringParameters"]["ppage"]

                
                res = getProductsList(query)
                return {
                'statusCode': 200,
                'body': json.dumps({'data':res})
                }

        except Exception as e:
                return {
                'statuscode': 500,
                'body': str(e)
                }
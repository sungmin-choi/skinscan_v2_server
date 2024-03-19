import json
import requests
from bs4 import BeautifulSoup as bs
import json
from collections import OrderedDict

url='https://folliculitisscout.com/xjsf?action=check_ingredients&ing_value='

# ingredients = 'Water, Polygonum Fagopyrum (Buckwheat) Seed Extract, Aloe Barbadensis Leaf Water, Butylene Glycol, Glycerin, Dipropylene Glycol, Glycereth-26, Pentylene Glycol, Propanediol, Hydroxyethyl Acrylate/​Sodium Acryloyldimethyl Taurate Copolymer, PEG-60 Hydrogenated Castor Oil, Octyldodeceth-16, Caprylyl Glycol, Phenoxyethanol, Arginine, Acrylates/​C10-30 Alkyl Acrylate Crosspolymer, Fragrance(Parfum), Polyquaternium-51, Disodium EDTA, Sodium Hyaluronate, Raffinose, Madecassoside, Saccharide Isomerate, Actinidia Chinensis (Kiwi) Fruit Extract, Solanum Lycopersicum (Tomato) Fruit/​Leaf/​Stem Extract, Sucrose, Sodium Palmitoyl Proline, Serine, Pca, Nymphaea Alba Flower Extract, Alanine, Threonine, Hydrolyzed Extensin, Mourera Fluviatilis Extract, Sodium Citrate, Citric Acid, Magnesium Gluconate, Calcium Gluconate, Zinc Gluconate'

def getIngredirentsInfo(ingredients):
    answers = OrderedDict()

    page = requests.get(url+ingredients)

    soup = bs(page.text, "html.parser")


    json_object = json.loads(soup.text)

    answers['danger'] =  json_object['danger']
    answers["danger_count"] = json_object['danger_count']
    answers['ingredients_info']=[]
    rows =  json_object['ing_result'].split('</tr>')

    for index,row in enumerate(rows):
        if index==len(rows)-1:
            continue
        not_safe_description = ''
        not_safe_rating=''
        isCuation = False
        ingredient_name=''
        caution_description =''
        ewg=''
        cir=''
        cosmetic_roles=''
        td_list = row.split('</td>')
        td1 = td_list[0].split('</span></div>')
        if len(td_list)>1:
            td2= row.split('</td>')[1].split('</span>')
            ewg=td2[0]
            cir=td2[1]
            if len(td2)>2:
                cosmetic_roles=td2[2].replace('</div>','')
        
        if 'Caution' in td1[0]:
            isCuation = True
            ingredient_name=td1[0].replace('Caution</span>', '').replace('\xa0(Amino Acid)</span>', '')
        else:
            ingredient_name= td1[0]
        
        if len(td1)>1 and len(td1[1]) >0:
            not_safe_item = td1[1].split('</li>')
            if isCuation:
                caution_description = not_safe_item[0]
                
            else:
                not_safe_description = not_safe_item[0]
            if len(not_safe_item)>2:
                not_safe_rating  = not_safe_item[1]

        ingredient_info ={
            'not_safe_description':not_safe_description,
            'not_safe_rating':not_safe_rating,
            'isCuation':isCuation,
            'ingredient_name':ingredient_name,
            'caution_description':caution_description,
            'ewg':ewg,
            'cir':cir,
            'cosmetic_roles':cosmetic_roles
        }

        answers['ingredients_info'].append(ingredient_info)

    return answers

def lambda_handler(event, context):
    try:
        query=''
        queryStringParameters = event.get("queryStringParameters", {})
        keyword=queryStringParameters.get("query")
        
        if keyword is not None:
            query=query+keyword
        
        res = getIngredirentsInfo(query)
        
        return {
                'statusCode': 200,
                'body': json.dumps({'data':res})
                }
    except Exception as e:
            return {
            'statuscode': 500,
            'body': str(e)
            }

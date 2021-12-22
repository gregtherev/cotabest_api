import flask
from flask import request, jsonify
import json
import uuid

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open('data.json') as json_file:
    print(json_file)
    data = json.load(json_file)

shopping_cart = []
aux = False

# Todos os produtos
#Exemplo do endpoint localhost:5000/v1/api/all
@app.route('/v1/api/all', methods=['GET'])
def api_all():
    return jsonify(data)

# Produtos por nome
#Exemplo do endpoint localhost:5000/v1/api/products?name=coelho
@app.route('/v1/api/products', methods=['GET'])
def api_products():
    if 'name' in request.args:
        name = request.args['name']
    else:
        return ('Erro. Digite o nome do produto que deseja buscar!')
    
    results = []

    for products in data:
        if name.lower() in products['name'].lower():
            results.append(products)
    return jsonify(results)


#Adicionar itens ao carrinho e alterar quantidade. Para remoção basta passar o qtd como negativo no endpoint
#Exemplo do endpoint localhost:5000/v1/api/shoppingcart/add?id=1&qtd=2
@app.route('/v1/api/shoppingcart/add', methods=['GET'])
def api_cart_add():
    aux = []
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return('Informe o ID do produto que deseja adicionar ao carrinho.')
    
    if 'qtd' in request.args: 
        qtd = int(request.args['qtd'])
    else:
        return('Infore a quantidade que deseja adicionar ao carrinho.')

    for products in data:
        if id == int(products['id']):
            dictionary = {"id": products['id'], "name": products['name'],
                            "price": products['price'], "minimun": products['minimun'],
                            "amount-per-package": products['amount-per-package'], "quantity": qtd}
            
            #Checando se o item já existe no carrinho. Caso sim a quantidade será incrementada               
            if shopping_cart:
                for buys in shopping_cart:
                    if buys['id'] == dictionary['id']:  
                        dictionary['quantity'] = buys['quantity'] + qtd
                        aux = True
                        break      

            #Verificando se a quantidade é a mínima
            if dictionary['quantity'] < dictionary['minimun']: 
                return(f'A quantidade minima do item {dictionary["name"]} é {dictionary["minimun"]}. Revise seus itens!')
            
            #Verificando se a quantidade desejada bate com a quantidade por pacote 
            if dictionary['quantity'] % dictionary['amount-per-package'] != 0:
                return(f'A quantidade do item {dictionary["name"]} não está de acordo com a quantidade por pacote!')
           
            #Verificando se a quantidade adicionada está disponível em estoque
            if dictionary['quantity'] > products['max-availability']:
                return(f'A quantidade do item {dictionary["name"]} é maior que o estoque de {products["max-availability"]} disponível!')

            if aux:
                buys['quantity'] += qtd
                aux = False
            else:
                shopping_cart.append(dictionary)
            return(jsonify(shopping_cart))
    return(f'Não há produtos com o id {id} cadastrados na base de dados.')
        
#Deletar itens do carrinho
#Exemplo do endpoint localhost:5000/v1/api/shoppingcart/remove?id=1
@app.route('/v1/api/shoppingcart/remove', methods=['GET'])        
def api_cart_remove():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return('Informe o ID do produto que deseja retirar da lista.')

    for i in range(len(shopping_cart)):
        if shopping_cart[i]['id'] == id:
            del shopping_cart[i]
            return jsonify(shopping_cart)   
    return(f'Não há produtos com o id {id} no carrinho.')

@app.route('/v1/api/shoppingcart/', methods=['GET'])
def api_cart_show():
    total_price = 0
    for products in shopping_cart:
        total_price += products['quantity'] * products['price']
    return json.dumps({"price": total_price, "items": shopping_cart})

# Finalizando a compra
@app.route('/v1/api/checkout', methods=['GET'])
def api_checkout():
    total_price = 0
    id = str(uuid.uuid4())

    for products in shopping_cart:
        total_price += products['quantity'] * products['price']

    checkout = json.dumps({"id": id, "total-price": total_price, "items": shopping_cart})
    shopping_cart.clear()

    return (checkout)                     


app.run()
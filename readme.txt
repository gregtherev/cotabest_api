Foi um desafio fazer esse mini sistemas pois não havia tido contato prévio e prático com API's.
Optei por utilizar o flask pela simplicidade e o gerenciador de arquivos para gravar os dados em
váriaveis globais.
Para gerar o id da compra utilizei a uuid.
Para o retorno dos valores foi utilizado o jsonify do próprio flask.
Não fiz a parte de testes, as checagens foram todas manuais nos if's do código sem uma biblioteca, pois o tempo foi meio corrido. Numa bateria com uma base de dados maior provavelmente o código vai quebrar em algumas partes.

Segue abaixo as instruções do código.

Checar todos os itens da base: /v1/api/all

Procurar produtos que contenham parte de uma string: /v1/api/products?name=texto

Adicionar itens ao carrinho: /v1/api/shoppingcart/add?id=1&qtd=120

Para editar a quantidade de itens, basta passar o id e quantidade no mesmo endpoint (valores negativos para retirada de itens)
Não criei um endpoint para mostrar o carrinho com todos os produtos poi

Remover itens ao carrinho: /v1/api/shoppingcart/remove?id=1

Ver itens do carrinho: /v1/api/shoppingcart

Finalizar as compras: /v1/api/checkout
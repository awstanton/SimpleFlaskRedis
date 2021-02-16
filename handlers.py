from flask import Flask, render_template, flash, redirect, request
import redis
from product import *
app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/products/", methods=['POST'])
def addProduct():
    # print(request.form.to_dict())
    client.hset(request.form.to_dict()["name"], "quantity", request.form.to_dict()["quantity"])
    client.hset(request.form.to_dict()["name"], "price", request.form.to_dict()["price"])
    return render_template('home.html')

@app.route("/products/", methods=['GET'])
def getProducts():
    productName = request.args.get('name')
    if (productName):
        # print(productName)
        product = client.hgetall(productName)
        # print(product)
        product['name'] = productName
        product['quantity'] = product[bytes('quantity','utf-8')].decode('utf-8')
        product['price'] = product[bytes('price','utf-8')].decode('utf-8')
        product.pop(b'quantity', None)
        product.pop(b'price', None)
        return render_template('home.html', product=product)
    else:
        products = []
        productNames = client.scan_iter('*')
        for productName in productNames:
            product = client.hgetall(productName)
            product['name'] = productName.decode('utf-8')
            product['quantity'] = product[b'quantity'].decode('utf-8')
            product['price'] = product[b'price'].decode('utf-8')
            product.pop(b'quantity', None)
            product.pop(b'price', None)
            products.append(product)
        # print(products)
        return render_template('home.html', products=products)

########

if __name__ == "__main__":
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    # print(client.ping())
    # print(client.keys())
    app.run(debug = True)


# Documentation on Tools
# https://flask.palletsprojects.com/en/1.1.x/
# https://redis-py.readthedocs.io/en/stable/
# https://jinja2docs.readthedocs.io/en/stable/
# https://werkzeug.palletsprojects.com/en/1.0.x/


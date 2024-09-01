from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from serializers import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/TedsBarAndCafeWebiste-DB'

#Intitialize the database
db.init_app(app)
migrate=Migrate(app, db)

#Initialize Cart
# cart = Cart()
cart = Cart()

# @app.route("/")
# def home():
#     return render_template("index.html")

@app.route("/")
def home():
    return render_template("index.html",cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/contact")
def contact():
    return render_template("contact.html", cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/newOrder", methods=['POST'])
def new_order():
    if request.method == "POST":
        f_name = request.form['fName']
        l_name = request.form['lName']
        phone = request.form['phone']
        email = request.form['email']
        pickup_time = request.form['pickup']

        print(f_name, l_name, pickup_time)

        customer = Customer_Details(f_name, l_name, phone, email, pickup_time, cart.get_contents_as_ids())

        try:
            db.session.add(customer)
            db.session.commit()
            return redirect('/order')
        except:
            return "There was an error adding the customer"
            
    return "Error"

@app.route("/check_out", methods=['GET'])
def check_out():
    if (cart.get_contents() == []):
        return redirect('/order')
    #need to fix empty cart logic on client side
    return render_template("check_out.html", cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/order/complete", methods=['GET'])
def order_complete():
    Burgers = Burger.query.all()
    Snacks = Snack.query.all()
    return render_template("index.html", burgers=Burgers, snacks=Snacks, cartItems=cart.get_contents(), cartTotal=cart.total_price())


@app.route("/order", methods=['POST', 'GET'])
def order():
    Burgers = Burger.query.all()
    Snacks = Snack.query.all()
    Beers = Beer.query.all()
    return render_template("order.html", burgers=Burgers, snacks=Snacks, cartItems=cart.get_contents(), cartTotal=cart.total_price())

#Cart APIS
@app.route("/cart", methods=['GET'])
def cart_content():
    render_template("cart.html", cartItems=Burger.query.all(), cartTotal=cart.total_price())   


@app.route("/add/<int:id>", methods=['GET'])
def add_to_cart(id):
    cart.add_item(id)    
    return {"status": "200"}

@app.route("/remove/<int:id>", methods=['GET'])
def remove_from_cart(id):
    cart.remove_item(id)
    return {"status": "200"}

@app.route("/empty", methods=['GET'])
def empty_cart():

    # formatted_cart = [{'id': item.product_id, 
    #                    'name': item.name,
    #                    'description': item.description,
    #                    'price': item.price,
    #                    'img_path': item.img_path,
    #                    } for item in cart]


    cart.empty_cart()
    return {"status": "200"}


@app.route("/addItem", methods=['POST','GET'])
def addItem():

    if request.method == "POST":
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        new_item = Burger(name=item_name, description=item_description, price=item_price)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/addItem')
        except:
            return "There was an error adding the item"
    else:
        menu_items = MenuItem.query.all()
        return render_template("addItem.html", stuff=menu_items, cartItems=cart.get_contents(), cartTotal=cart.total_price())



#main
if __name__ == "__main__":
    app.run(debug=True)
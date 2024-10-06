from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
from serializers import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@teds-bar-db-instance.cx4u2uqs8cs8.ap-southeast-2.rds.amazonaws.com:5432/TedsBarDBAws'

#Intitialize the database
db.init_app(app)
migrate=Migrate(app, db)

#Initialize Cart
# cart = Cart()
cart = Cart()
customer = Customer_Details()
completedOrder = False

# @app.route("/")
# def home():
#     return render_template("index.html")

def newCustomer(c):
    customer = c
    return 

@app.route("/")
def home():
    return render_template("index.html",cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/completed")
def completed():
    Burgers = Burger.query.all()
    Snacks = Snack.query.all()
    Beers = Beer.query.all()
    details = customer
    print(details.email)
    return render_template("completed.html", burgers=Burgers, snacks=Snacks, cartItems=cart.get_contents(), cartTotal=cart.total_price(), order_details=details)


@app.route("/about_us")
def about():
    return render_template("about.html", cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/contact")
def contact():
    return render_template("contact.html", cartItems=cart.get_contents(), cartTotal=cart.total_price())

@app.route("/newOrder", methods=['POST', 'GET'])
def new_order():
    details = []
    
    if request.method == "POST":
        f_name = request.form['fName']
        l_name = request.form['lName']
        phone = request.form['phone']
        email = request.form['email']
        pickup_time = request.form['pickup']

        print(f_name, l_name, pickup_time)

        details.append(Customer_Details(f_name, l_name, phone, email, pickup_time, cart.get_contents_as_ids()))

        try:
            db.session.add(details[0])
            db.session.commit()
            cart.empty_cart()
        except:
            return "There was an error adding the customer"
    
    if details==[]:
        return redirect("/order")
        
    Burgers = Burger.query.all()
    Snacks = Snack.query.all()
    Beers = Beer.query.all()
    print(details[0].email, "working")
    
    return render_template("order.html", burgers=Burgers, snacks=Snacks, cartItems=cart.get_contents(), cartTotal=cart.total_price(), showFeedback = True, order_details=details[0])
            

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
    print(customer.first_name)
    return render_template("order.html", burgers=Burgers, snacks=Snacks, cartItems=cart.get_contents(), cartTotal=cart.total_price(), showFeedback = False, order_details=customer)

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
    cart.empty_cart()
    return {"status": "200"}


@app.route("/addItem", methods=['POST','GET'])
def addItem():

    if request.method == "POST":
        item_name = request.form['name']
        item_description = request.form['description']
        item_price = request.form['price']
        new_item = Snack(name=item_name, description=item_description, price=item_price)

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
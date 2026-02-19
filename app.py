from flask import Flask, render_template, request, redirect, url_for, session

from werkzeug.security import generate_password_hash, check_password_hash



import smtplib

from email.mime.text import MIMEText

#Hardcoded users (username: hashed_password)
users = {
    "Nomcebo Mncwabe": generate_password_hash("Password123"),
    "Reyhana Meadows" : generate_password_hash("Password456"),
}

app = Flask(__name__)
app.secret_key = "coffee_secret_key"

# MENU DATA (acts like a database for now)
menu_items = [
    {
        "id": 2,
        "name": "Latte",
        "price": 35,
        "image": "latte.jpg",
        "description": "Smooth espresso with steamed milk and light foam."
    },
    {
        "id": 3,
        "name": "Cappuccino",
        "price": 32,
        "image": "cappuccino.jpg",
        "description": "Rich espresso with thick milk foam."
    },
    {
        "id": 6,
        "name": "Chocolate Cake",
        "price": 45,
        "image": "cake.jpg",
        "description": "Moist chocolate sponge with creamy frosting."
    },
    {
        "id": 1,
        "name": "Espresso",
        "price": 25,
        "image": "espresso.jpg",
        "description": "Strong, bold espresso shot with rich crema."
    },

    {
        "id": 4,
        "name": "Iced Latte",
        "price": 38,
        "image": "iced_latte.jpg",
        "description": "Chilled espresso with cold milk and ice."
    },
    {
        "id": 5,
        "name": "Mocha",
        "price": 40,
        "image": "mocha.jpg",
        "description": "Espresso mixed with chocolate and steamed milk."
    },

    {
        "id": 7,
        "name": "Vanilla Cake",
        "price": 40,
        "image": "vanilla_cake.jpg",
        "description": "Light vanilla sponge with smooth buttercream."
    },
    {
        "id": 8,
        "name": "Red Velvet Cake",
        "price": 50,
        "image": "red_velvet.jpg",
        "description": "Classic red velvet with cream cheese icing."
    },

    {
        "id": 10,
        "name": "Cheesecake",
        "price": 48,
        "image": "cheesecake.jpg",
        "description": "Creamy cheesecake on a buttery biscuit base."
    },

    {
        "id": 9,
        "name": "Cupcake",
        "price": 20,
        "image": "cupcake.jpg",
        "description": "Mini cake with sweet topping"
    }
]

#Home/ About Page
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")


#Menu Page
@app.route("/menu")
def menu():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("menu.html", menu=menu_items)

@app.route("/add-to-cart/<int:item_id>")
def add_to_cart(item_id):
    if "user" not in session:
        return redirect(url_for("login"))

    if "cart" not in session:
        session["cart"] = []

    for item in menu_items:
        if item["id"] == item_id:
            session["cart"].append(item)
            break

    session.modified = True
    return redirect(url_for("menu"))

#Cart Page
@app.route("/cart")
def cart():
    if "user" not in session:
        return redirect(url_for("login"))

    cart_items = session.get("cart", [])
    total = sum(item["price"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

#Checkout Page
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "GET":

        selected_ids = request.args.getlist("selected_items")

        if not selected_ids:
            return redirect(url_for("cart"))

        cart_list = []

        for item_id in selected_ids:
            item_id = int(item_id)

            # find item in menu
            item = next((m for m in menu_items if m["id"] == item_id), None)
            if not item:
                continue

            quantity = int(request.args.get(f"quantity_{item_id}", 1))
            subtotal = item["price"] * quantity

            cart_list.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "quantity": quantity, # <-- use actual quantity
                "subtotal": item["price"] * quantity, # <-- recalc subtotal
            })

        if not cart_list:
            return redirect(url_for("cart"))

        delivery_option = request.args.get("delivery_option", "collection")
        delivery_fee = 20 if delivery_option == "delivery" else 0

        session["order"] = {
                "cart": cart_list,
                "delivery_option": delivery_option,
                "delivery_fee": delivery_fee,
                "address": None,
                "total_price": sum(i["subtotal"] for i in cart_list) + delivery_fee
            }

        session.modified = True
        return render_template("checkout.html", order=session["order"])


    # POST: user submits delivery option and address
    delivery_option = request.form.get("delivery_option")
    address = request.form.get("address") if delivery_option == "delivery" else None

    # Update delivery info in session["order"]
    session["order"]["delivery_option"] = delivery_option
    session["order"]["address"] = address
    session["order"]["delivery_fee"] = 20 if delivery_option == "delivery" else 0

    # Recalculate total
    total = sum(item['subtotal'] for item in session["order"]["cart"])
    total += session["order"]["delivery_fee"]
    session["order"]["total_price"] = total
    session.modified = True

    # Redirect to payment page
    return redirect(url_for("payment"))



#Contact Page
@app.route('/contact')
def contact():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template('contact.html')


#Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # TEMP login logic (no database yet)
        if not username or not password:
            return render_template("login.html", errors="Please fill in all fields.")

        #Check if username exists
        if username not in users:
            return render_template("login.html", errors="Username not found.")

        #Check if password matches
        if not check_password_hash(users[username], password):
            return render_template("login.html", errors="Incorrect password.")

        #login successful
        session["user"] = username
        return redirect(url_for("home"))

    return render_template("login.html")

#Registration Page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", errors="All fields are required.")

        if len(password) < 6:
            return render_template("register.html", errors="Password must be at least 6 characters.")

        if username in users:
            return render_template("register.html", errors="Username already taken.")

        users[username] = generate_password_hash(password)
        return redirect(url_for("login"))

    return render_template("register.html")


#Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

#Payment Route
# --- Payment ---
@app.route("/payment", methods=["GET", "POST"])
def payment():
    if "user" not in session:
        return redirect(url_for("login"))

    order = session.get("order")
    if not order:
        return redirect(url_for("cart"))

    if request.method == "POST":
        customer_email = request.form.get("email")

        if not customer_email:
            return render_template(
                "payment.html",
                order=order,
                error="Please enter your email"
            )

        # Mark payment as completed
        session["payment_done"] = True
        session["invoice_email"] = customer_email

        return redirect(url_for("invoice"))

    return render_template("payment.html", order=order)


# --- Invoice ---
@app.route("/invoice")
def invoice():
    if not session.get("payment_done"):
        return redirect(url_for("cart"))

    order = session.get("order")
    email = session.get("invoice_email")

    # Send invoice ONCE
    if not session.get("invoice_sent"):
        send_invoice(email, order)
        session["invoice_sent"] = True

    return render_template("invoice.html", order=order)


def send_invoice(to_email, order):
    print("Invoice would be sent to:", to_email)
    print(order)

#After Finishing Order when going back to cart , nothing is selected
@app.route("/finish_order")
def finish_order():
    # Clear everything AFTER invoice is shown
    session.pop("order", None)
    session.pop("payment_done", None)
    session.pop("invoice_sent", None)
    session.pop("invoice_email", None)

    return redirect(url_for("menu"))




if __name__ == "__main__":
    app.run(debug=True)

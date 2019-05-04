from flask import *
import sqlite3
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def valid(email, pw):
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute("SELECT EmailID, Password FROM Customer")
        userInfo = cur.fetchall()
        for info in userInfo:
            if info[0] == email and info[1] == pw:
                return True
        return False


def valid_file(file):
    return '.' in file and \
        file.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def parse(data):
    output = []
    for i in range(len(data)):
        new = []
        for j in range(7):
            if i >= len(data):
                break
            new.append(data[i])
        output.append(new)
    return output


def getAccountDetails():
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor();
        if 'EmailID' not in session:
            loggedIn = False
            first_name = ''
            itemNo = 0
        else:
            loggedIn = True
            cur.execute("SELECT CustomerID, FirstName FROM Customer WHERE EmailID = ?", (session['EmailID'], ))
            customerID, first_name = cur.fetchone()
            cur.execute("SELECT count(ArticleID) FROM ShoppingCart WHERE CustomerID = ?", (customerID, ))
            itemNo = cur.fetchone()[0]
    edb.close()
    return(loggedIn, first_name, itemNo)

def getItemDetails():
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        if 'ArticleID' not in session:
            itemName = ''
            Price = 0
            SellerID = 0
        else:
            cur.execute("SELECT ArticleID, SellerID, Name, Price FROM Item WHERE ArticleID = ? ", session['ArticleID'], )
            itemID, SellerID, itemName, Price = cur.fetchone()
    edb.close()
    return (itemID, SellerID, itemName, Price)


@app.route("/")
def home():
    loggedIn, first_name, itemNo = getAccountDetails()
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute('SELECT Name, ArticleID, ItemType, Price, SellerID FROM Item ')
        itemInfo = cur.fetchall()
    itemInfo = parse(itemInfo)
    return render_template('home.html', itemInfo=itemInfo, loggedIn=loggedIn, itemNo=itemNo)


@app.route("/add")
def employee():
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute("SELECT ItemId, ItemName, Quantity, Price, SellerID, FROM Inventory")
        inventory = cur.fetchall()
    edb.close()
    return render_template('add.html', inventory=inventory)


@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        Name = request.form['Name']
        ArticleID = int(request.form['ArticleID'])
        ItemType = request.form['ItemType']
        Price = float(request.form['Price'])

        image = request.files['image']
        if image and valid_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('ecommerce.db') as edb:
            try:
                cur = edb.cursor()
                cur.execute('''INSERT INTO Item (Name, ArticleID, ItemType, Price, image) VALUES (?, ?, ?, ?, ?)''',
                            (Name, ArticleID, ItemType, Price, imagename))
                edb.commit()
                msg = "Added item successfully"
            except:
                msg="error occured adding item"
                edb.rollback()
        edb.close()
        print(msg)
        return redirect(url_for('home'))


@app.route("/delete")
def delete():
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute('SELECT Name, ArticleID, ItemType, Price, SellerID, Image FROM Item')
        itemData = cur.fetchall()
    edb.close()
    return render_template('remove.html', data=itemData)


@app.route("/deleteItem")
def deleteItem():
    ArticleID = request.args.get('ArticleID')
    with sqlite3.connect('ecommerce.db') as edb:
        try:
            cur = edb.cursor()
            cur.execute('DELETE FROM Item WHERE ArticleID = ?', (ArticleID, ))
            edb.commit()
            msg = "Deleted Item"
        except:
            edb.rollback()
            msg = "Error when deleting"
    edb.close()
    print(msg)
    return redirect(url_for('home'))


@app.route("/account/profile")
def viewProfile():
    if 'EmailID' not in session:
        return redirect(url_for('home'))
    loggedIn, first_name, itemNo = getAccountDetails()
    return render_template("profile.html", loggedIn=loggedIn, first_name=first_name, itemNo=itemNo)


@app.route("/account/profile/edit")
def editAccount():
    if 'EmailID' not in session:
        return redirect(url_for('home'))
    loggedIn, first_name, itemNo = getAccountDetails()
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute("SELECT CustomerID, PhoneNumber, FirstName, LastName, EmailID, Address FROM Customer WHERE EmailID = ?", (session['EmailID'], ))
        accountInfo = cur.fetchone()
    edb.close()
    return render_template("editAccount.html", accountInfo=accountInfo, loggedIn=loggedIn,first_name=first_name, itemNo=itemNo)


@app.route("/account/profile/updatePassword", methods=["GET", "POST"])
def changePassword():
    if 'EmailID' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        prevPass = request.form('prevPass')
        newPass = request.form('newPass')
        with sqlite3.connect('ecommerce.db') as edb:
            cur = edb.cursor()
            cur.execute("SELECT CustomerID, Password FROM Customer WHERE email = ?", (session['EmailID'], ))
            CustomerID, Password = cur.fetchone()
            if Password == prevPass:
                try:
                    cur.execute("UPDATE Customer SET Password = ? WHERE CustomerID = ?", (newPass, CustomerID))
                    edb.commit()
                    info = "Password Updated!"
                except:
                    edb.rollback()
                    info = "Password did not update"
                edb.close() # JUST IN CASE
                return render_template("updatePassword.html", info=info)
            else:
                info = "Incorrect password"
        edb.close()
        return render_template("updatePassword.html", info=info)
    else:
        return render_template("updatePassword")


@app.route("/updateAccount", methods=["GET", "POST"])
def updateAccount():
    if request.method == "POST":
        EmailID = request.form['EmailID']
        FirsttName = request.form['FirstName']
        LastName = request.form['LastName']
        number = request.form['PhoneNumber']
        Address = request.form['Address']
        with sqlite3.connect('ecommerce.db') as edb:
            try:
                cur = edb.cursor()
                cur.execute('UPDATE Customer SET FirstName = ?, LastName = ?, PhoneNumber = ?, Address = ? WHERE EmailID = ?', (FirsttName, LastName, number, Address, EmailID))
                edb.commit()
                output = "Updated Account info!"
            except:
                edb.rollback()
                output = "Error when updating account, please try again later"
        print(output)
        edb.close()
        return redirect(url_for('editAccount'))


@app.route("/verifylogin")
def verifyLogin():
    if 'EmailID' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        EmailID = request.form['EmailID']
        password = request.form['Password']
        if valid(EmailID, password):
            session['EmailID'] = EmailID
            return redirect(url_for('home'))
        else:
            error = 'Invalid Email/Password'
            print(error)
            return render_template('login.html', error=error)


@app.route("/itemInfo")
def itemInfo():
    loggedIn, firstName, itenmNo = getAccountDetails()
    ItemID = request.args.get('ArticleID')
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute('SELECT ArticleID, Name, Price, ItemType, SellerID FROM Item WHERE ArticleID = ?', (ItemID, ))
        itemInfo = cur.fetchone()
        cur.execute('SELECT DetailedReview, Ratings, CustomerID FROM Reviews WHERE ArticleID = ?', (ItemID))
        reviewData = cur.fetchone()
    edb.close()
    return render_template("itemInfo.html", itemInfo=itemInfo, reviews=reviewData, loggedIn=loggedIn, firstName=firstName, itemNo=itenmNo)


@app.route("/createReview", methods=['GET', 'POST'])
def review():
    if 'EmailID' not in session:
        return redirect(url_for('verifyLogin'))
    loggedIn, FirstName, ItemNo = getAccountDetails()
    if 'ArticleID' not in session:
        return render_template('404.html')
    itemID, SellerID, itemName, Price = getItemDetails()
    if request.method == "POST":
        review = request.form['DetailedReview']
        rating = request.form['Ratings']
        with sqlite3.connect('ecommerce.db') as edb:
            try:
                cur = edb.cursor()
                cur.execute("SELECT CustomerID FROM Customer WHERE EmailID = ?", (session['EmailID'], ))
                customer = cur.fetchone()[0]
                cur.execute('INSERT INTO Reviews (ArticleID, SellerID, CustomerID, Ratings, DetailedReview) VALUES (?, ?, ?, ?, ?)',
                    (itemID, SellerID, customer, rating, review))
                edb.commit()
                output = "Added Review!"
            except:
                edb.rollback()
                output = "Error when adding review"
        print(output)
        edb.close()
        return redirect(url_for('itemInfo'))


@app.route("/ShoppingCart")
def ShoppingCart():
    if 'EmailID' not in session:
        return redirect(url_for('verifyLogin'))
    loggedIn, FirstName, ItemNo = getAccountDetails()
    EmailID = session['EmailID']
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute("SELECT CustomerID FROM Customer WHERE EmailID = ?", (EmailID, ))
        customer = cur.fetchone()[0]
        cur.execute("SELECT Item.ArticleID, Item.Name, Item.Price, Item.SellerID, Item.Image FROM Item, ShoppingCart WHERE Item.ArticleID = ShoppingCart.ArticleID AND ShoppingCart.CustomerID = ?", (customer, ))
        items = cur.fetchall()
    totalPrice = 0
    for item in items:
        totalPrice += item[2]
    return render_template("ShoppingCart.html", items=items, totalPrice=totalPrice, loggedIn=loggedIn, firstName=FirstName, itemNo=ItemNo)


@app.route("/addToCart")
def addToCart():
    if 'EmailID' not in session:
        return redirect(url_for('verifyLogin'))
    else:
        ArticleID = int(request.args.get('ArticleID'))
        with sqlite3.connect('ecommerce.db') as edb:
            cur = edb.cursor()
            cur.execute("SELECT CustomerID FROM Customer WHERE EmailID = ?", (session['EmailID'], ))
            customer = cur.fetchone()
            try:
                cur.execute("INSERT INTO _adds_item_to_cart(ArticleID, CustomerID) VALUES (?, ?)", (ArticleID, customer))
                edb.commit()
                output = "Added Succesfully"
            except:
                edb.rollback()
                output = "Did not add to cart"
        edb.close()
        print(output)
        return redirect(url_for('home'))


@app.route("/removeFromCart")
def removeFromCart():
    if 'EmailID' not in session:
        return redirect(url_for('verifyLogin'))
    EmailID = session['EmailID']
    ArticleID = int(request.args.get('ArticleID'))
    with sqlite3.connect('ecommerce.db') as edb:
        cur = edb.cursor()
        cur.execute("SELECT CustomerID FROM Customer WHERE EmailID = ?", (EmailID, ))
        customerID = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM ShoppingCart WHERE CustomerID = ? AND ArticleID = ?", (customerID, ArticleID))
            edb.commit()
            output = "Removed from cart"
        except:
            edb.rollback()
            output = "Could not remove item from cart"
    edb.close()
    print(output)
    return redirect(url_for('home'))


@app.route("/logout")
def logout():
    session.pop('EmailID', None)
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = random.randint(1,1000001)
        pw = request.form['Password']
        email = request.form['EmailID']
        first = request.form['FirstName']
        last = request.form['LastName']
        number = request.form['PhoneNumber']
        address = request.form['Address']
        with sqlite3.connect('ecommerce.db') as edb:
            try:
                cur = edb.cursor()
                cur.execute("INSERT INTO Customer(CustomerID,PhoneNumber, FirstName, LastName, EmailID, Password, Address) VALUES (?, ?, ?, ?, ?, ?, ?)", (id, number, first, last, email, pw, address))
                edb.commit()
                output = "Enjoy you experience!"
            except:
                edb.rollback()
                output = "Sorry could not register at this time, try again later."
        edb.close()
        print(output)
        return render_template("login.html", error=output)


@app.route("/registration")
def registration():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)

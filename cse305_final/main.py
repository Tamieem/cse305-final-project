from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def getAccountDetails():
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor();
        if 'EmailID' not in session:
            loggedIn = False
            first_name = ''
            itemNo = 0
        else:
            loggedIn = True
            cur.execute("SELECT customerID, FirstName FROM Customer where EmailID = ?", (session['EmailID'], ))
            customerID, FirstName = cur.fetchone()
    conn.close()
    return(loggedIn, first_name, itemNo)

@app.route("/")
def root():
    loggedIn, first_name, itemNo = getAccountDetails()
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT ArticleID, ItemType, Price, SellerID FROM Item ')
        itemInfo = cur.fetchall()
    itemInfo = parse(itemInfo)
    return  render_template('home.html', itemInfo=itemInfo, loggedIn=loggedIn, itemNo=itemNo)

@app.route("/add")
def employee():
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT ItemId, ItemName, Quantity, Price, SellerID, FROM Inventory")
        inventory = cur.fetchall()
    conn.close()
    return render_template('add.html', inventory=inventory)

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        Name = request.form['Name']
        ArticleID = int(request.form['ArticleID'])
        ItemType = request.form['ItemType']
        Price = float(request.form['Price'])

        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        imagename = filename
        with sqlite3.connect('ecommerce.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('''INSERT INTO Item (Name, ArticleID, ItemType, Price, image) VALUES (?, ?, ?, ?, ?)''',
                            (Name, ArticleID, ItemType, Price, imagename))
                conn.commit()
                msg = "Added item successfully"
            except:
                msg="error occured adding item"
                conn.rollback()
        conn.close()
        print(msg)
        return redirect(url_for('root'))

@app.route("/delete")
def delete():
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT Name, ArticleID, ItemType, Price, SellerID, Image FROM Item')
        itemData = cur.fetchall()
    conn.close()
    return render_template('remove.html', data=itemData)

@app.route("/deleteItem")
def deleteItem():
    ArticleID = request.args.get('ArticleID')
    with sqlite3.connect('ecommerce.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM Item WHERE ArticleID = ?', (ArticleID, ))
            conn.commit()
            msg = "Deleted Item"
        except:
            conn.rollback()
            msg = "Error when deleting"
    conn.close()
    print(msg)
    return redirect(url_for('root'))

@app.route("/account/profile")
def viewProfile():
    if 'EmailID' not in session:
        return redirect(url_for('root'))
    loggedIn, first_name, itemNo = getAccountDetails()
    return render_template("profile.html", loggedIn=loggedIn, first_name=first_name, itemNo=itemNo)

@app.route("/account/profile/edit")
def editAccount():
    if 'EmailID' not in session:
        return redirect(url_for('root'))
    loggedIn, first_name, itemNo = getAccountDetails()
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT CustomerID, PhoneNumber, FirstName, LastName, EmailID, Address FROM Customer WHERE EmailID = ?", (session['EmailID'], ))
        accountInfo = cur.fetchone()
    conn.close()
    return render_template("editAccount.html", accountInfo=accountInfo, loggedIn=loggedIn,first_name=first_name, itemNo=itemNo)


@app.route("/account/profile/updatePassword", methods=["GET", "POST"])
def changePassword():
    if 'EamilID' not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        prevPass = request.form('prevPass')
        newPass = request.form('newPass')
        with sqlite3.connect('ecommerce.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT CustomerID, Password FROM Customer WHERE email = ?", (session['EmailID'], ))
            CustomerID, Password = cur.fetchone()
            if Password == prevPass:
                try:
                    cur.execute("UPDATE Customer SET Password = ? WHERE CustomerID = ?", (newPass, CustomerID))
                    conn.commit()
                    info = "Password Updated!"
                except:
                    conn.rollback()
                    info = "Password did not update"
                conn.close() # JUST IN CASE
                return render_template("updatePassword.html", info=info)
            else:
                info = "Incorrect password"
        conn.close()
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
        with sqlite3.connect('ecommerce.db') as conn:
            try:
                cur = conn.cursor()
                cur.execute('UPDATE Customer SET FirstName = ?, LastName = ?, PhoneNumber = ?, Address = ? WHERE EmailID = ?', (FirsttName, LastName, number, Address, EmailID))
                conn.commit()
                info = "Updated Account info!"
            except:
                conn.rollback()
                info = "Error when updating account, please try again later"
        conn.close()
        return redirect(url_for('editAccount'))

@app.route("/verifylogin")
def verifyLogin():
    if 'EmailID' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        EmailID = request.form['EmailID']
        password = request.form['Password']
        if valid(EmailID, password):
            session['email'] = EmailID
            return  render_template(url_for('root'))
        else:
            error = 'Invalid Email/Password'
            return render_template('login.html', error=error)

@app.route("/itemInfo")
def itemInfo():
    loggedIn, firstName, itenmNo = getAccountDetails()
    ItemID = request.args.get('ArticleID')
    with sqlite3.connect('ecommerce') as conn:
        cur = conn.cursor()
        cur.execute('SELECT ArticleID, Name, Price, ItemType, SellerID FROM Item WHERE ArticleID = ?', (ItemID, ))
        itemInfo = cur.fetchone()
    conn.close()
    return render_template("itemInfo.html", data=itemInfo, loggedIn=loggedIn, firstName=firstName, itemNo=itenmNo)

@app.route("/addToCart")
def addToCart():
    if 'EmailID' not in session:
        return redirect(url_for('verifyLogin'))
    loggedIn, FirstName, ItemNo = getAccountDetails()
    EmailID = session['EmailID']
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT CustomerID FROM Customer WHERE EmailID = ?", (EmailID, ))
        customer = cur.fetchone()[0]
        cur.execute("SELECT Item.ArticleID, Item.Name, Item.Price, Item.SellerID, Item.Image FROM Item, ShoppingCart WHERE Item.ArticleID = ShoppingCart.ArticleID AND ShoppingCart.CustomerID = ?", (customer, ))
        items = cur.fetchall()
    totalPrice = 0

    for item in items:
        totalPrice += item[2]
    return render_template("cart.html", items=items, totalPrice=totalPrice, loggedIn=loggedIn, firstName=FirstName, itemNo=ItemNo)

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

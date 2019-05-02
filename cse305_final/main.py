from flask import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'random string'


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
    return(loggedIn, first_name)

@app.rout("/")
def root():
    loggedIn, first_name = getAccountDetails()
    with sqlite3.connect('ecommerce.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT ArticleID, ItemType, Price, SellerID FROM Item ')
        i
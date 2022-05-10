from flask import *
import hashlib
import os
from connect_db import conn_create as cc

conn, cur = cc()

app = Flask(__name__)
app.secret_key = 'random_string_Value'

def get_Login_Details():
    conn, cur = cc()
    cur = conn.cursor()
    print(session)
    if 'email' not in session:
        x,fname,count_items = False,'',0
    else:
        x = True
        cur.execute(
            "SELECT userId, firstName FROM users WHERE email = %s", (session['email'], ))
        Uid, fname = cur.fetchone()
        cur.execute(
            "SELECT count(productId) FROM cart WHERE userId = %s", (Uid, ))
        count_items = cur.fetchone()[0]
    return (x, fname, count_items)


@app.route("/")
def _root_():
    x, fname, count_items = get_Login_Details()
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute(
        'SELECT productId, name, price, description, image, stock FROM products LIMIT 20')
    i_data = cur.fetchall()
    cur.execute('SELECT categoryId, name FROM categories LIMIT 10')
    cat_data = cur.fetchall()
    i_data = parse(i_data)
    return render_template('home.html', itemData=i_data, loggedIn=x, firstName=fname, count_items=count_items, categoryData=cat_data)


@app.route("/add")
def admin():
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute("SELECT categoryId, name FROM categories")
    cat = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=cat)

meth = ["GET", "POST"]

@app.route("/displayCategory")
def displayCategory():
    x, fname, count_items = get_Login_Details()
    cat_id = request.args.get("categoryId")
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = %s", (cat_id, ))
    fetch_data = cur.fetchall()
    conn.close()
    cat_name = fetch_data[0][4]
    fetch_data = parse(fetch_data)
    return render_template('displayCategory.html', data=fetch_data, loggedIn=x, firstName=fname, count_items=count_items, categoryName=cat_name)


@app.route("/displayMoreCategory")
def display_More_Category():
    x, fname, count_items = get_Login_Details()
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute('SELECT categoryId, name FROM categories')
    catData = cur.fetchall()
    return render_template('displayMoreCategory.html', loggedIn=x, firstName=fname, count_items=count_items, categoryData=catData)


@app.route("/displayProducts")
def display_Products():
    x, fname, count_items = get_Login_Details()
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute(
        'SELECT productId, name, price, description, image, stock FROM products')
    idata = cur.fetchall()
    idata = parse(idata)
    return render_template('displayProducts.html', itemData=idata, loggedIn=x, firstName=fname, count_items=count_items)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('_root_'))
    x, fname, count_items = get_Login_Details()
    return render_template("profileHome.html", loggedIn=x, firstName=fname, count_items=count_items)


@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('_root_'))
    x, fname, count_items = get_Login_Details()
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute(
        "SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = %s", (session['email'], ))
    pro_data = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=pro_data, loggedIn=x, firstName=fname, count_items=count_items)


@app.route("/account/profile/changePassword", methods=meth)
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        o_pass = request.form['oldpassword']
        o_pass = hashlib.md5(o_pass.encode()).hexdigest()
        n_pass = request.form['newpassword']
        newPassword = hashlib.md5(n_pass.encode()).hexdigest()
        conn, cur = cc()
        cur = conn.cursor()
        cur.execute(
            "SELECT userId, password FROM users WHERE email = %s", (session['email'], ))
        userId, password = cur.fetchone()
        if (password == o_pass):
            try:
                cur.execute(
                    "UPDATE users SET password = %s WHERE userId = %s", (n_pass, userId))
                conn.commit()
                msg = "Changed successfully"
            except:
                conn.rollback()
                msg = "Failed"
            return render_template("changePassword.html", msg=msg)
        else:
            msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")


@app.route("/updateProfile", methods=meth)
def updateProfile():
    if request.method == 'POST':
        email, fname,lname,add1,add2 = request.form['email'],request.form['firstName'],request.form['lastName'],request.form['address1'],request.form['address2']
        state,city,zip,country,phone = request.form['state'],request.form['city'],request.form['zipcode'],request.form['country'],request.form['phone']
        conn, cur = cc()
        try:
            cur = conn.cursor()
            cur.execute('UPDATE users SET firstName = %s, lastName = %s, address1 = %s, address2 = %s, zipcode = %s, city = %s, state = %s, country = %s, phone = %s WHERE email = %s',
                        (fname, lname, add1, add2, zip, city, state, country, phone, email))
            conn.commit()
        except:
            conn.rollback()
        conn.close()
        return redirect(url_for('editProfile'))


@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('_root_'))
    else:
        return render_template('login.html', error='')


def validity_checking(email, password):
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for i,j in data:
        if i == email and j == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/login", methods = meth)
def login():
    if request.method == 'POST':
        e_mail,password = request.form['email'],request.form['password']
        if validity_checking(e_mail, password):
            session['email'] = e_mail
            return redirect(url_for('_root_'))
    return render_template('login.html', error='OOPS!! Incorrect Details')


@app.route("/productDescription")
def productDescription():
    x, fname, count_items = get_Login_Details()
    prd_id = request.args.get('productId')
    conn, cur = cc()
    cur.execute(
        'SELECT productId, name, price, description, image, stock FROM products WHERE productId = %s', (prd_id, ))
    prd_data = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=prd_data, loggedIn=x, firstName=fname, count_items=count_items)


@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute("SELECT userId FROM users WHERE email = %s",(session['email'], ))
    try:
        cur.execute(
            "INSERT INTO cart (userId, productId) VALUES (%s, %s)",
            (cur.fetchone()[0], int(request.args.get('productId'))))
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return redirect(url_for('_root_'))

@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    x, fname, count_items = get_Login_Details()
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute("SELECT userid FROM users WHERE email = %s", (session['email'], ))
    cur.execute("SELECT products.productid, products.name, products.price, products.image FROM products, cart WHERE products.productid = cart.productid AND cart.userid = %s", (cur.fetchone()[0], ))
    prod = cur.fetchall()
    totalPrice = 0
    for row in prod:
        totalPrice += float(row[2])
    return render_template("cart.html", products=prod, totalPrice=totalPrice, loggedIn=x, firstName=fname, count_items=count_items)

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    conn, cur = cc()
    cur = conn.cursor()
    cur.execute("SELECT userId FROM users WHERE email = %s", (session['email'], ))
    try:
        cur.execute(
            "DELETE FROM cart WHERE userId = %s AND productId = %s",
            (cur.fetchone()[0], int(request.args.get('productId'))))
        conn.commit()
    except:
        conn.rollback()
    conn.close()
    return redirect(url_for('cart'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('_root_'))

@app.route("/register", methods = meth)
def register():
    if request.method == 'POST':
        e_mail,password = request.form['email'],request.form['password']
        fname,lname = request.form['firstName'],request.form['lastName']
        add1,add2 = request.form['address1'],request.form['address2']
        zip,city,state = request.form['zipcode'],request.form['city'],request.form['state']
        country,phone = request.form['country'],request.form['phone']
    print(request)
    conn, cur = cc()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (hashlib.md5(
            password.encode()).hexdigest(), e_mail, fname, lname, add1, add2, zip, city, state, country, phone))
        conn.commit()
        msg = "Registered Successfully"
    except Exception as e:
        conn.rollback()
        print(e)
        msg = "Error occured"
    conn.close()
    return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)
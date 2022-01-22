from flask import Flask, redirect, url_for, render_template, request, session, flash, json
import flask
from webforms import LoginForm, ProductAddForm, ProductDeleteForm, ProductSearchForm, StoreAddForm, StoreDeleteForm, SupplierAddForm, SupplierDeleteForm, AdminAddForm, AdminDeleteForm, StoreSearchForm, SupplierSearchForm, AdminSearchForm, ProductUpdateForm, StoreUpdateForm, SupplierUpdateForm
from datetime import datetime
import DBConnection
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

#connect to mysql database
ksql = DBConnection.dbcon().mydb

def dtnow():
    dt = datetime.now()
    str_now = str(dt)
    str_now = str_now[:-6]
    return str_now

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        username = session['username']
    else:
        form = LoginForm()
        if form.validate_on_submit():
            # request username and password
            username = request.form['username']
            password = request.form['password']
            # check if username and password exists in database Admin & Supervisor
            conn = ksql.cursor()
            conn.execute("SELECT * FROM Admin WHERE Username = %s AND AdminPW = %s", (username, password,))
            record = conn.fetchone()
            if record:
                session['loggedin'] = True
                session['username'] = record[2]
                flash("Logged in successfully!")
                return redirect(url_for('adminhome'))
            elif not username or not password:
                flash("Incorrect Username/Password! Please Try Again.")
                return render_template("login.html", form=form)
            else:
                conn.execute("SELECT * FROM Supervisor WHERE Username = %s AND SupervisorPW = %s", (username, password,))
                rec = conn.fetchone()
                if rec:
                    session['loggedin'] = True
                    session['username'] = rec[2]
                    flash("Logged in successfully!")
                    return redirect(url_for('supervisorhome'))
                else:
                    flash("Incorrect Username/Password! Please Try Again.")
                    return render_template("login.html", form=form)
        return render_template('login.html', form=form)

# Logout
@app.route('/logout')
def logout():
    if "username" in session:
        username = session["username"]
        session.pop("loggedin", None)
        session.pop("username",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

# ===========================
# Admin Home
@app.route("/adminhome")
def adminhome():
    if "username" in session:
        username = session["username"]
        return render_template("adminhome.html")
    else:
        return redirect(url_for("login"))

# Supervisor Home
@app.route("/supervisorhome")
def supervisorhome():
    if "username" in session:
        username = session["username"]
        return render_template("supervisorhome.html")
    else:
        return redirect(url_for("login"))

# Supplier Menu
@app.route("/suppliermenu")
def suppliermenu():
    if "username" in session:
        username = session["username"]
        return render_template("suppliermenu.html")
    else:
        return redirect(url_for("login"))

# Store Menu
@app.route("/storemenu")
def storemenu():
    if "username" in session:
        username = session["username"]
        return render_template("storemenu.html")
    else:
        return redirect(url_for("login"))

# Product Menu
@app.route("/productmenu")
def productmenu():
    if "username" in session:
        username = session["username"]

        return render_template("productmenu.html")
    else:
        return redirect(url_for("login"))

# Admin Menu
@app.route("/adminmenu")
def adminmenu():
    if "username" in session:
        username = session["username"]
        return render_template("adminmenu.html")
    else:
        return redirect(url_for("login"))

# ===========================
# Product Add
@app.route("/productadd", methods=['GET', 'POST'] )
def productadd():
    if "username" in session:
        username = session["username"]
        form = ProductAddForm()
        if form.validate_on_submit():
            sku = request.form['sku']
            name = request.form['name']
            description = request.form['description']
            producttype = request.form['producttype']
            conn = ksql.cursor()
            conn.execute("SELECT SKU FROM Products WHERE SKU = %s", (sku,))
            record = conn.fetchall()
            li = []
            if (record == li):
                conn.execute("INSERT INTO Products (SKU, ProductsName, Description, ProductType) VALUES (%s, %s, %s, %s)",(sku, name, description, producttype))
                ksql.commit()
                flash("Product Added!")
                return redirect(url_for("productmenu"))
            else:
                flash("Duplicate data! Please enter another product SKU.")
                return redirect(url_for("productadd"))

        return render_template("productadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Product Delete
@app.route("/productdelete", methods=['GET', 'POST'])
def productdelete():
    if "username" in session:
        username = session["username"]
        form = ProductDeleteForm()
        if form.validate_on_submit():
            sku = request.form['sku']
            conn = ksql.cursor()
            conn.execute("SELECT SKU FROM Products WHERE SKU = %s", (sku,))
            record = conn.fetchall()
            li = []
            # sku product exists in the data
            if (record != li):
                conn.execute("DELETE FROM Products WHERE SKU = %s", (sku,))
                ksql.commit()
                flash("Product Deleted")
                return redirect(url_for('productmenu'))
            else:
                flash("Data does not exist! Please enter another product SKU.")
                return redirect(url_for('productdelete'))
        return render_template('productdelete.html', form=form)
    else:
        return redirect(url_for('login'))

# Product Search
@app.route('/productsearch', methods=['GET', 'POST'])
def productsearch():
    if "username" in session:
        username = session['username']
        form = ProductSearchForm()
        if form.validate_on_submit():
            return redirect(url_for('productsearch'))
        return render_template("productsearch.html", form=form)
    else:
        return redirect(url_for('login'))

# Product View
@app.route('/productview', methods=['GET', 'POST'])
def productview():
    if "username" in session:
        username = session['username']
        #form = ProductViewForm()
        if request.method == 'POST':
            sku = request.form['sku']
            conn = ksql.cursor()
            conn.execute("SELECT SKU FROM Products WHERE SKU = %s", (sku,))
            rec = conn.fetchall()
            li = []
            if (rec != li):
                conn.execute("SELECT SKU, ProductsName, Description, ProductType FROM Products WHERE SKU = %s", (sku,))
                record = conn.fetchone()
                ksql.commit()
                return render_template('productview.html', record=record)
            else:
                flash("SKU does not exist! Please enter another product SKU.")
                return redirect(url_for("productsearch"))
        return render_template('productview.html')
    else:
        return redirect(url_for('login'))

# Product Update (use product search)
@app.route("/productupdate",  methods=['GET', 'POST'])
def productupdate():
    if "username" in session:
        username = session["username"]
        form = ProductUpdateForm()
        if form.validate_on_submit():
            sku = request.form['sku']
            name = request.form['name']
            description = request.form['description']
            producttype = request.form['producttype']
            conn = ksql.cursor()
            conn.execute("SELECT SKU FROM Products WHERE SKU = %s", (sku,))
            record = conn.fetchall()
            conn.execute("UPDATE Products SET ProductsName = %s, Description = %s, ProductType = %s  WHERE SKU = %s",(name, description, producttype,sku))
            ksql.commit()
            flash("Product Updated!")
            return redirect(url_for('productmenu'))
        return render_template('productupdate.html', form=form)
    else:
        return redirect(url_for('login'))



# ===========================
# Store Add
@app.route("/storeadd", methods=['GET', 'POST'])
def storeadd():
    if "username" in session:
        username = session["username"]
        form = StoreAddForm()
        if form.validate_on_submit():
            code = request.form['code']
            location = request.form['location']
            address = request.form['address']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Stores WHERE Code = %s",(code,))
            record = conn.fetchall()
            li = []
            if (record == li):
                conn.execute("INSERT INTO Stores (Code, Location, Address) VALUES (%s, %s, %s)",(code, location, address))
                ksql.commit()
                flash("Store Added!")
                return redirect(url_for("storemenu"))
            else:
                flash("Duplicate data! Please enter another store code.")
                return redirect(url_for("storeadd"))
        return render_template("storeadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Store Delete
@app.route("/storedelete", methods=['GET', 'POST'])
def storedelete():
    if "username" in session:
        username = session["username"]
        form = StoreDeleteForm()
        if form.validate_on_submit():
            code = request.form['code']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Stores WHERE Code = %s",(code,))
            record = conn.fetchall()
            li = []
            # code product exists in the data
            if (record != li):
                conn.execute("DELETE FROM Stores WHERE Code = %s", (code,))
                ksql.commit()
                flash("Store Deleted")
                return redirect(url_for('storemenu'))
            else:
                flash("Data does not exist! Please enter another store code.")
                return redirect(url_for('storedelete'))
        return render_template('storedelete.html', form=form)
    else:
        return redirect(url_for('login'))

# Store Search
@app.route('/storesearch', methods=['GET', 'POST'])
def storesearch():
    if "username" in session:
        username = session['username']
        form = StoreSearchForm()
        if form.validate_on_submit():
            return redirect(url_for('storesearch'))
        return render_template("storesearch.html", form=form)
    else:
        return redirect(url_for('login'))

# Store View
@app.route('/storeview', methods=['GET', 'POST'])
def storeview():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            code = request.form['code']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Stores WHERE Code = %s", (code,))
            rec = conn.fetchall()
            li = []
            if (rec != li):
                conn.execute("SELECT Code, Location, Address FROM Stores WHERE Code = %s", (code,))
                record = conn.fetchone()
                ksql.commit()
                return render_template('storeview.html', record=record)
            else:
                flash("Code does not exist! Please enter another store code.")
                return redirect(url_for("storesearch"))
        return render_template('storeview.html')
    else:
        return redirect(url_for('login'))

# Store Update
@app.route("/storeupdate",  methods=["GET", "POST"])
def storeupdate():
    if "username" in session:
        username = session["username"]
        form = StoreUpdateForm()
        if form.validate_on_submit():
            code = request.form['code']
            location = request.form['location']
            address = request.form['address']
            cur = ksql.cursor()
            cur.execute("UPDATE Stores SET Location = %s, Address = %s WHERE Code = %s", (location, address, code))
            ksql.commit()
            flash("Store Updated!")
            return redirect(url_for('storemenu'))
        return render_template('storeupdate.html', form = form)
    else:
        return redirect(url_for('login'))

# ===========================
# Supplier Add
@app.route("/supplieradd", methods=['GET', 'POST'])
def supplieradd():
    if "username" in session:
        username = session["username"]
        form = SupplierAddForm()
        if form.validate_on_submit():
            code = request.form['code']
            name = request.form['name']
            phone = request.form['phone']
            address = request.form['address']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Suppliers WHERE Code = %s", (code,))
            record = conn.fetchall()
            li = []
            if (record == li):
                conn.execute("INSERT INTO Suppliers (Code, SupplierName, SupplierPhone, SupplierAddress) VALUES (%s, %s, %s, %s)", (code,name, phone, address))
                ksql.commit()
                flash("Supplier Added!")
                return redirect(url_for("suppliermenu"))
            else:
                flash("Duplicate data! Please enter another supplier code.")
                return redirect(url_for("supplieradd"))

        return render_template("supplieradd.html", form = form)
    else:
        return redirect(url_for("login"))

# Supplier Delete
@app.route("/supplierdelete", methods=['GET', 'POST'])
def supplierdelete():
    if "username" in session:
        username = session["username"]
        form = SupplierDeleteForm()
        if form.validate_on_submit():
            code = request.form['code']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Suppliers WHERE Code = %s", (code,))
            record = conn.fetchall()
            li = []
            # sku product exists in the data
            if (record != li):
                conn.execute("DELETE FROM Suppliers WHERE Code = %s", (code,))
                ksql.commit()
                flash("Supplier Deleted")
                return redirect(url_for('suppliermenu'))
            else:
                flash("Data does not exist! Please enter another product SKU.")
                return redirect(url_for('supplierdelete'))
        return render_template('supplierdelete.html', form=form)
    else:
        return redirect(url_for('login'))

# Supplier Search
@app.route('/suppliersearch', methods=['GET', 'POST'])
def suppliersearch():
    if "username" in session:
        username = session['username']
        form = SupplierSearchForm()
        if form.validate_on_submit():
            return redirect(url_for('suppliersearch'))
        return render_template("suppliersearch.html", form=form)
    else:
        return redirect(url_for('login'))

# Supplier View
@app.route('/supplierview', methods=['GET', 'POST'])
def supplierview():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            code = request.form['code']
            conn = ksql.cursor()
            conn.execute("SELECT Code FROM Suppliers WHERE Code = %s", (code,))
            rec = conn.fetchall()
            li = []
            if (rec != li):
                conn.execute("SELECT Code, SupplierName, SupplierPhone, SupplierAddress FROM Suppliers WHERE Code = %s", (code,))
                record = conn.fetchone()
                ksql.commit()
                return render_template('supplierview.html', record=record)
            else:
                flash("Code does not exist! Please enter another supplier code.")
                return redirect(url_for("suppliersearch"))
        return render_template('supplierview.html')
    else:
        return redirect(url_for('login'))

# Supplier Update
@app.route("/supplierupdate",  methods=["GET", "POST"])
def supplierupdate():
    if "username" in session:
        username = session["username"]
        form = SupplierUpdateForm()
        if form.validate_on_submit():
            code = request.form['code']
            name = request.form['name']
            phone = request.form['phone']
            address = request.form['address']
            cur = ksql.cursor()
            cur.execute("UPDATE Suppliers SET SupplierName = %s, SupplierPhone = %s, SupplierAddress = %s WHERE Code = %s", (name, phone, address, code))
            ksql.commit()
            flash("Supplier Updated!")
            return redirect(url_for("suppliermenu"))
        return render_template('supplierupdate.html', form=form)
    else:
        return redirect(url_for('login'))

# ===========================
# Admin Add
@app.route("/adminadd", methods=['GET', 'POST'])
def adminadd():
    if "username" in session:
        username = session["username"]
        name=None
        form = AdminAddForm()
        if form.validate_on_submit():
            req = request.form
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            record = cur.fetchall()
            li = []
            if (record == li):
                cur.execute("INSERT INTO Admin (FullName, Username, AdminPW, AdminPhone, AdminAddress, AdminEmail) VALUES (%s, %s, %s, %s, %s, %s)", (name, username, password, phone, address, email))
                ksql.commit()
                flash("Admin account created")
                return redirect(url_for("adminmenu"))
            else:
                flash("Username exists! Please enter another username.")
                return redirect(url_for("adminadd"))
        return render_template("adminadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Admin Delete
@app.route("/admindelete", methods=['GET', 'POST'])
def admindelete():
    if "username" in session:
        username = session["username"]
        form = AdminDeleteForm()
        if form.validate_on_submit():
            username = request.form['username']
            conn = ksql.cursor()
            conn.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            record = conn.fetchall()
            li = []
            # username exists in the data
            if (record != li):
                conn.execute("DELETE FROM Admin WHERE Username = %s", (username,))
                ksql.commit()
                flash("Admin Deleted")
                return redirect(url_for('adminmenu'))
            else:
                flash("Data does not exist! Please enter another product SKU.")
                return redirect(url_for('admindelete'))
        return render_template('admindelete.html', form=form)
    else:
        return redirect(url_for('login'))

# Admin Search
@app.route('/adminsearch', methods=['GET', 'POST'])
def adminsearch():
    if "username" in session:
        username = session['username']
        form = AdminSearchForm()
        if form.validate_on_submit():
            return redirect(url_for('adminsearch'))
        return render_template("adminsearch.html", form=form)
    else:
        return redirect(url_for('login'))

# Admin View
@app.route('/adminview', methods=['GET', 'POST'])
def adminview():
    if "username" in session:
        username = session['username']
        if request.method == 'POST':
            username = request.form['username']
            conn = ksql.cursor()
            conn.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            rec = conn.fetchall()
            li = []
            if (rec != li):
                conn.execute("SELECT FullName, Username, AdminPW, AdminPhone, AdminAddress, AdminEmail FROM Admin WHERE Username = %s", (username,))
                record = conn.fetchone()
                ksql.commit()
                return render_template('adminview.html', record=record)
            else:
                flash("Username does not exist! Please enter another username.")
                return redirect(url_for("adminsearch"))
        return render_template('adminview.html')
    else:
        return redirect(url_for('login'))

# Admin Update



if __name__ =="__main__":
    app.run(debug = True)
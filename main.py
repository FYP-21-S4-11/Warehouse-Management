from flask import Flask, redirect, url_for, render_template, request, session, flash, json

from webforms import LoginForm, ProductAddForm, ProductDeleteForm, ProductSearchForm, StoreAddForm, StoreDeleteForm, SupplierAddForm, SupplierDeleteForm, AdminAddForm, AdminDeleteForm, StoreSearchForm, SupplierSearchForm, AdminSearchForm, ProductUpdateForm, StoreUpdateForm, SupplierUpdateForm, AdminUpdateForm
from datetime import date, datetime
import DBConnection
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"

#connect to mysql database
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'kafka123@'
#app.config['MYSQL_DATABASE_DB'] = 'WManage'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['AUTH_PLUGIN'] = "mysql_native_password"
#app.config['PORT'] = "3306"
#mydb = MySQL(app)

#connect to mysql database
ksql = DBConnection.dbcon().mydb


def dtnow():
    dt = datetime.now()
    str_now = str(dt)
    str_now = str_now[:-6]
    return str_now

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        username = session["username"]
    else:
        form = LoginForm()
        if form.validate_on_submit():
            # request username and password
            username = request.form["username"]
            password = request.form["password"]
            # check if username and password exists in database Admin & Supervisor
            cur = ksql.cursor()
            cur.execute("SELECT * FROM Admin WHERE Username = %s AND AdminPW = %s", (username, password,))
            record = cur.fetchone()
            if record:
                session["loggedin"] = True
                session["username"] = record[2]
                flash("Logged in successfully!")
                return redirect(url_for("adminhome"))
            elif not username or not password:
                flash("Incorrect Username/Password! Please Try Again.")
                return render_template("login.html", form=form)
            else:
                cur.execute("SELECT * FROM Supervisor WHERE Username = %s AND SupervisorPW = %s", (username, password,))
                rec = cur.fetchone()
                if rec:
                    session["loggedin"] = True
                    session["username"] = rec[2]
                    flash("Logged in successfully!")
                    return redirect(url_for("supervisorhome"))
                else:
                    flash("Incorrect Username/Password! Please Try Again.")
                    return render_template("login.html", form=form)
        return render_template("login.html", form=form)

# Logout
@app.route("/logout")
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
@app.route("/productadd", methods=["GET", "POST"] )
def productadd():
    if "username" in session:
        username = session["username"]
        form = ProductAddForm()
        if form.validate_on_submit():
            sku = request.form["sku"]
            name = request.form["name"]
            description = request.form["description"]
            producttype = request.form["producttype"]
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Product (ProductSKU, ProductName, Description, ProductType) VALUES (%s, %s, %s, %s)",(sku, name, description, producttype))
                ksql.commit()
                flash("Product added!")
                return redirect(url_for("productmenu"))
            else:
                flash("Duplicate data! Please enter another product SKU.")
                return redirect(url_for("productadd"))
        return render_template("productadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Product Delete
@app.route("/productdelete", methods=["GET", "POST"])
def productdelete():
    if "username" in session:
        username = session["username"]
        form = ProductDeleteForm()
        if form.validate_on_submit():
            sku = request.form["sku"]
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            exist = cur.fetchall()
            if not exist:
                flash("Data does not exist! Please enter another product SKU.")
                return redirect(url_for("productdelete"))
            else:
                cur.execute("DELETE FROM Product WHERE ProductSKU = %s", (sku,))
                ksql.commit()
                flash("Product deleted!")
                return redirect(url_for("productmenu"))
        return render_template("productdelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Product Search
@app.route("/productsearch", methods=["GET", "POST"])
def productsearch():
    if "username" in session:
        username = session["username"]
        form = ProductSearchForm()
        if form.validate_on_submit():
            return redirect(url_for("productsearch"))
        return render_template("productsearch.html", form=form)
    else:
        return redirect(url_for("login"))

# Product View
@app.route("/productview", methods=["GET", "POST"])
def productview():
    if "username" in session:
        username = session["username"]
        #form = ProductViewForm()
        if request.method == "POST":
            sku = request.form["sku"]
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            rec = cur.fetchall()
            li = []
            if (rec != li):
                cur.execute("SELECT ProductSKU, ProductName, Description, ProductType FROM Product WHERE ProductSKU = %s", (sku,))
                record = cur.fetchone()
                ksql.commit()
                return render_template("productview.html", record=record)
            else:
                flash("SKU does not exist! Please enter another product SKU.")
                return redirect(url_for("productsearch"))
        return render_template("productview.html")
    else:
        return redirect(url_for("login"))

# Product Update
@app.route("/productupdate",  methods=["GET", "POST"])
def productupdate():
    if "username" in session:
        username = session["username"]
        form = ProductUpdateForm()
        if form.validate_on_submit():
            sku = request.form["sku"]
            name = request.form["name"]
            description = request.form["description"]
            producttype = request.form["producttype"]
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            exist = cur.fetchall()
            if not exist:
                flash("SKU does not exist! Please enter another product SKU.")
                render_template("productupdate.html", form=form)
            else:
                cur.execute("UPDATE Product SET ProductName = %s, Description = %s, ProductType = %s  WHERE ProductSKU = %s",(name, description, producttype,sku))
                ksql.commit()
                flash("Product updated!")
                return redirect(url_for("productmenu"))
        return render_template("productupdate.html", form=form)
    else:
        return redirect(url_for("login"))

# Inventory In (add products from store)
@app.route("/inventoryin", methods=["GET", "POST"])
def inventoryin():
    if "username" in session:
        username = session["username"]
        return render_template("inventoryin.html")
    else:
        return redirect(url_for("login"))


# Inventory Out (send products to stores)
@app.route("/inventoryout", methods=["GET", "POST"])
def inventoryout():
    if "username" in session:
        username = session["username"]
        # fetch all store code
        cur = ksql.cursor()
        cur.execute("SELECT StoreCode FROM Store")
        storeexist = cur.fetchall()
        cur.close()
        if request.method == "POST" or request.method == "GET":
            id = request.form.get('id')
            code = request.form.get('code')
            sku = request.form.get('sku')
            name = request.form.get('name')
            type = request.form.get('type')
            quantity = request.form.get('quantity')
            today = date.today()
            curdate = today.strftime("%Y-%m-%d")

            # check for product SKU
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            skuexist = cur.fetchall()
            cur.close()

            if request.method == "POST":
                cur = ksql.cursor()
                cur.execute(
                    "INSERT INTO Inventory (InventoryID, StoreCode, ProductSKU, ProductName, ProductType, Quantity, Date) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (id, code, sku, name, type, quantity, curdate))
                ksql.commit()
                cur.close()
                flash("Successfully sent products!")
                return redirect(url_for("productmenu"))
            elif not skuexist:
                flash("SKU does not exist. Please enter another product SKU.")
                return render_template("inventoryout.html", skuexist=skuexist, storeexist=storeexist, id=id, code=code, sku=sku, name=name, type=type, quantity=quantity)
            elif not storeexist:
                flash("Please select a store code!")
                return render_template("inventoryout.html", skuexist=skuexist, storeexist=storeexist, id=id, code=code, sku=sku, name=name, type=type, quantity=quantity)
            elif not code:
                flash("Please select a store code!")
                return render_template("inventoryout.html", skuexist=skuexist, storeexist=storeexist, id=id, code=code, sku=sku, name=name, type=type, quantity=quantity)
            else:
                flash("Error occured!")
                return render_template("inventoryout.html", skuexist=skuexist, storeexist=storeexist, id=id, code=code, sku=sku, name=name, type=type, quantity=quantity)
        return render_template("inventoryout.html")
    else:
        return redirect(url_for("login"))

# ===========================
# Store Add
@app.route("/storeadd", methods=["GET", "POST"])
def storeadd():
    if "username" in session:
        username = session["username"]
        form = StoreAddForm()
        if form.validate_on_submit():
            code = request.form["code"]
            location = request.form["location"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT StoreCode FROM Store WHERE StoreCode = %s",(code,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Store (StoreCode, Location, Address) VALUES (%s, %s, %s)",(code, location, address))
                ksql.commit()
                flash("Store added!")
                return redirect(url_for("storemenu"))
            else:
                flash("Duplicate data! Please enter another store code.")
                return redirect(url_for("storeadd"))
        return render_template("storeadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Store Delete
@app.route("/storedelete", methods=["GET", "POST"])
def storedelete():
    if "username" in session:
        username = session["username"]
        form = StoreDeleteForm()
        if form.validate_on_submit():
            code = request.form["code"]
            cur = ksql.cursor()
            cur.execute("SELECT StoreCode FROM Store WHERE StoreCode = %s",(code,))
            exist = cur.fetchall()
            if not exist:
                flash("Code does not exist! Please enter another store code.")
                return redirect(url_for("storedelete"))
            else:
                cur.execute("DELETE FROM Store WHERE StoreCode = %s", (code,))
                ksql.commit()
                flash("Store deleted!")
                return redirect(url_for("storemenu"))
        return render_template("storedelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Store Search
@app.route("/storesearch", methods=["GET", "POST"])
def storesearch():
    if "username" in session:
        username = session["username"]
        form = StoreSearchForm()
        if form.validate_on_submit():
            return redirect(url_for("storesearch"))
        return render_template("storesearch.html", form=form)
    else:
        return redirect(url_for("login"))

# Store View
@app.route("/storeview", methods=["GET", "POST"])
def storeview():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            code = request.form["code"]
            cur = ksql.cursor()
            cur.execute("SELECT StoreCode FROM Store WHERE StoreCode = %s", (code,))
            rec = cur.fetchall()
            li = []
            if (rec != li):
                cur.execute("SELECT StoreCode, Location, Address FROM Store WHERE StoreCode = %s", (code,))
                record = cur.fetchone()
                ksql.commit()
                return render_template("storeview.html", record=record)
            else:
                flash("Code does not exist! Please enter another store code.")
                return redirect(url_for("storesearch"))
        return render_template("storeview.html")
    else:
        return redirect(url_for("login"))

# Store Update
@app.route("/storeupdate",  methods=["GET", "POST"])
def storeupdate():
    if "username" in session:
        username = session["username"]
        form = StoreUpdateForm()
        if form.validate_on_submit():
            code = request.form["code"]
            location = request.form["location"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT StoreCode FROM Store WHERE StoreCode = %s", (code,))
            exist = cur.fetchall()
            if not exist:
                flash("Code does not exist! Please enter another store code.")
                return render_template("storeupdate.html", form=form)
            else:
                cur.execute("UPDATE Store SET Location = %s, Address = %s WHERE StoreCode = %s", (location, address, code))
                ksql.commit()
                flash("Store updated!")
                return redirect(url_for("storemenu"))
        return render_template("storeupdate.html", form=form)
    else:
        return redirect(url_for("login"))

# ===========================
# Supplier Add
@app.route("/supplieradd", methods=["GET", "POST"])
def supplieradd():
    if "username" in session:
        username = session["username"]
        form = SupplierAddForm()
        if form.validate_on_submit():
            code = request.form["code"]
            name = request.form["name"]
            phone = request.form["phone"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT SupplierCode FROM Supplier WHERE SupplierCode = %s", (code,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Supplier (SupplierCode, SupplierName, SupplierPhone, SupplierAddress) VALUES (%s, %s, %s, %s)", (code,name, phone, address))
                ksql.commit()
                flash("Supplier added!")
                return redirect(url_for("suppliermenu"))
            else:
                flash("Duplicate data! Please enter another supplier code.")
                return redirect(url_for("supplieradd"))

        return render_template("supplieradd.html", form = form)
    else:
        return redirect(url_for("login"))

# Supplier Delete
@app.route("/supplierdelete", methods=["GET", "POST"])
def supplierdelete():
    if "username" in session:
        username = session["username"]
        form = SupplierDeleteForm()
        if form.validate_on_submit():
            code = request.form["code"]
            cur = ksql.cursor()
            cur.execute("SELECT SupplierCode FROM Supplier WHERE SupplierCode = %s", (code,))
            exist = cur.fetchall()
            if not exist:
                flash("Code does not exist! Please enter another supplier code.")
                return redirect(url_for("supplierdelete"))
            else:
                cur.execute("DELETE FROM Supplier WHERE SupplierCode = %s", (code,))
                ksql.commit()
                flash("Supplier deleted!")
                return redirect(url_for("suppliermenu"))
        return render_template("supplierdelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Supplier Search
@app.route("/suppliersearch", methods=["GET", "POST"])
def suppliersearch():
    if "username" in session:
        username = session["username"]
        form = SupplierSearchForm()
        if form.validate_on_submit():
            return redirect(url_for("suppliersearch"))
        return render_template("suppliersearch.html", form=form)
    else:
        return redirect(url_for("login"))

# Supplier View
@app.route("/supplierview", methods=["GET", "POST"])
def supplierview():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            code = request.form["code"]
            cur = ksql.cursor()
            cur.execute("SELECT SupplierCode FROM Supplier WHERE SupplierCode = %s", (code,))
            rec = cur.fetchall()
            li = []
            if (rec != li):
                cur.execute("SELECT SupplierCode, SupplierName, SupplierPhone, SupplierAddress FROM Supplier WHERE SupplierCode = %s", (code,))
                record = cur.fetchone()
                ksql.commit()
                return render_template("supplierview.html", record=record)
            else:
                flash("Code does not exist! Please enter another supplier code.")
                return redirect(url_for("suppliersearch"))
        return render_template("supplierview.html")
    else:
        return redirect(url_for("login"))

# Supplier Update
@app.route("/supplierupdate",  methods=["GET", "POST"])
def supplierupdate():
    if "username" in session:
        username = session["username"]
        form = SupplierUpdateForm()
        if form.validate_on_submit():
            code = request.form["code"]
            name = request.form["name"]
            phone = request.form["phone"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT SupplierCode FROM Supplier WHERE SupplierCode = %s", (code,))
            exist = cur.fetchall()
            if not exist:
                flash("Code does not exist! Please enter another supplier code.")
                return render_template("supplierupdate.html", form=form)
            else:
                cur.execute("UPDATE Supplier SET SupplierName = %s, SupplierPhone = %s, SupplierAddress = %s WHERE SupplierCode = %s", (name, phone, address, code))
                ksql.commit()
                flash("Supplier updated!")
                return redirect(url_for("suppliermenu"))
        return render_template("supplierupdate.html", form=form)
    else:
        return redirect(url_for("login"))

# ===========================
# Admin Add
@app.route("/adminadd", methods=["GET", "POST"])
def adminadd():
    if "username" in session:
        username = session["username"]
        name=None
        form = AdminAddForm()
        if form.validate_on_submit():
            req = request.form
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Admin (FullName, Username, AdminPW, AdminPhone, AdminAddress, AdminEmail) VALUES (%s, %s, %s, %s, %s, %s)", (name, username, password, phone, address, email))
                ksql.commit()
                flash("Admin account created!")
                return redirect(url_for("adminmenu"))
            else:
                flash("Username exists! Please enter another username.")
                return redirect(url_for("adminadd"))
        return render_template("adminadd.html", form=form)
    else:
        return redirect(url_for("login"))

# Admin Delete
@app.route("/admindelete", methods=["GET", "POST"])
def admindelete():
    if "username" in session:
        username = session["username"]
        form = AdminDeleteForm()
        if form.validate_on_submit():
            username = request.form["username"]
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            exist = cur.fetchall()
            if not exist:
                flash("Admin account does not exist! Please enter another username.")
                return redirect(url_for("admindelete"))
            else:
                cur.execute("DELETE FROM Admin WHERE Username = %s", (username,))
                ksql.commit()
                flash("Admin deleted!")
                return redirect(url_for("adminmenu"))
        return render_template("admindelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Admin Search
@app.route("/adminsearch", methods=["GET", "POST"])
def adminsearch():
    if "username" in session:
        username = session["username"]
        form = AdminSearchForm()
        if form.validate_on_submit():
            return redirect(url_for("adminsearch"))
        return render_template("adminsearch.html", form=form)
    else:
        return redirect(url_for("login"))

# Admin View
@app.route("/adminview", methods=["GET", "POST"])
def adminview():
    if "username" in session:
        username = session["username"]
        if request.method == "POST":
            username = request.form["username"]
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            rec = cur.fetchall()
            li = []
            if (rec != li):
                cur.execute("SELECT FullName, Username, AdminPW, AdminPhone, AdminAddress, AdminEmail FROM Admin WHERE Username = %s", (username,))
                record = cur.fetchone()
                ksql.commit()
                return render_template("adminview.html", record=record)
            else:
                flash("Username does not exist! Please enter another username.")
                return redirect(url_for("adminsearch"))
        return render_template("adminview.html")
    else:
        return redirect(url_for("login"))

# Admin Update
@app.route("/adminupdate",  methods=["GET", "POST"])
def adminupdate():
    if "username" in session:
        username = session["username"]
        form = AdminUpdateForm()
        if form.validate_on_submit():
            name = request.form["name"]
            username = request.form["username"]
            password = request.form["password"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username,))
            exist = cur.fetchall()
            if not exist:
                flash("Username does not exist! Please enter another username.")
                return render_template("adminupdate.html", form=form)
            else:
                cur.execute("UPDATE Admin SET FullName = %s, AdminPW = %s, AdminPhone = %s, AdminAddress = %s, AdminEmail = %s WHERE Username = %s", (name, password, phone, address, email, username))
                ksql.commit()
                flash("Admin account updated!")
                return redirect(url_for("adminmenu"))
        return render_template("adminupdate.html", form=form)
    else:
        return redirect(url_for("login"))

# ===========================
# View Stock
@app.route("/viewstock", methods=["GET", "POST"])
def viewstock():
    if "username" in session:
        username = session["username"]
        headings = ("StockSKU", "StockName", "Reason", "Date")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Stock LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No stocks in the warehouse!")
            return redirect(url_for("adminhome"))
        else:
            cur.execute("SELECT * FROM Stock")
            data = cur.fetchall()
            return render_template("viewstock.html", headings=headings, data=data)
        # return render_template("adminhome.html")
    else:
        return redirect(url_for("login"))

# ===========================
# View Admin Profile
@app.route("/adminprofile", methods=["GET", "POST"])
def adminprofile():
    if "username" in session:
        username = session["username"]
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT Username, FullName, AdminPW, AdminPhone, AdminAddress, AdminEmail FROM Admin WHERE Username = %s", (username,))
        userfound = cur.fetchone()
        ksql.commit()
        return render_template("adminprofile.html", userfound=userfound)
    else:
        return redirect(url_for("login"))


@app.route("/supervisorprofile", methods=["GET", "POST"])
def supervisorprofile():
    if "username" in session:
        username = session["username"]
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Supervisor WHERE Username = %s", (username,))
        userfound = cur.fetchall()
        return render_template("supervisorprofile.html", userfound=userfound)
    else:
        return redirect(url_for("login"))


if __name__ =="__main__":
    app.run(debug = True)
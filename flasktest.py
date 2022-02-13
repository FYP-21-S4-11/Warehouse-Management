from flask import Flask, redirect, url_for, render_template, request, session, flash, json
from webforms import LoginForm, ProductAddForm, ProductDeleteForm, \
     StoreAddForm, StoreDeleteForm, SupplierAddForm, \
    SupplierDeleteForm, AdminAddForm, AdminDeleteForm, ProductUpdateForm, StoreUpdateForm, \
    SupplierUpdateForm, AdminUpdateForm,TopicForm
from datetime import date, datetime
import dbconnection
import kafka
from kafka import KafkaProducer
from kafka import KafkaConsumer
import time
import mysql.connector
#from flaskext.mysql import MySQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234"

#connect to mysql database
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'Warehouse'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['AUTH_PLUGIN'] = "mysql_native_password"
#app.config['PORT'] = "3306"
#mydb = MySQL(app)

#connect to mysql database
#ksql = DBConnection.dbcon().mydb
ksql = dbconnection.dbcon().mydb

def json_serializer(data):
    return json.dumps(data).encode("utf-8")
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=json_serializer)
jsonproducer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

#date time for json
def dtnow():
    dt = datetime.now()
    str_now = str(dt)
    str_now = str_now[:-6]
    return str_now

# Login
@app.route("/")
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
            _datetime = dtnow()
            _username = str(username)
            # check if username and password exists in database Admin & Supervisor
            cur = ksql.cursor()
            cur.execute("SELECT * FROM Admin WHERE Username = %s AND AdminPW = %s", (username, password,))
            record = cur.fetchone()
            if record:
                session["loggedin"] = True
                session["username"] = record[2]
                flash("Logged in successfully!")
                logindict = {"User": _username, "Activity": "Logged in", "time": _datetime
                             }
                #jsonproducer.send("testtopic1", _username + " logged in on :" + _datetime)
                jsonproducer.send("logininfo", logindict)
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
                    #jsonproducer.send("testtopic1", _username + " logged in on :" + _datetime)
                    logindict = {"User": _username, "Activity": "Logged in", "time": _datetime}
                    jsonproducer.send("logininfo", logindict)
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
        _datetime = dtnow()
        _username = str(username)
        session.pop("loggedin", None)
        session.pop("username",None)
        #jsonproducer.send("testtopic1", _username + " logged out on :" + _datetime)
        logoutdict = {"User": _username, "Activity": "Logged out", "time": _datetime}
        jsonproducer.send("logininfo", logoutdict)
        print(logoutdict)
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
            _datetime = dtnow()
            _username = str(username)
            _sku= str(sku)
            addprod = "added product sku "+_sku
            description = request.form["description"]
            producttype = request.form["producttype"]
            cur = ksql.cursor()
            cur.execute("SELECT ProductSKU FROM Product WHERE ProductSKU = %s", (sku,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Product (ProductSKU, ProductName, Description, ProductType) VALUES (%s, %s, %s, %s)",(sku, name, description, producttype))
                ksql.commit()
                flash("Product added!")
                addproddict = {"User": _username, "Activity":addprod, "time": _datetime}
                jsonproducer.send("productinfo", addproddict)
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
            _datetime = dtnow()
            _username = str(username)
            _sku = str(sku)
            delprod = " deleted product sku " + _sku
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
                delproddict = {"User": _username, "Activity": delprod, "time": _datetime}
                jsonproducer.send("productinfo", delproddict)
                return redirect(url_for("productmenu"))
        return render_template("productdelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Product Search
#@app.route("/productsearch", methods=["GET", "POST"])
#def productsearch():
#    if "username" in session:
#        username = session["username"]
#        form = ProductSearchForm()
#        if form.validate_on_submit():
#            return redirect(url_for("productsearch"))
#        return render_template("productsearch.html", form=form)
#    else:
#        return redirect(url_for("login"))

# Product View
@app.route("/productview", methods=["GET", "POST"])
def productview():
    if "username" in session:
        username = session["username"]
        headings = ("ProductSKU", "Product Name", "Product Description", "Product Type")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Product LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No products in the warehouse!")
            return redirect(url_for("producthome"))
        else:
            cur.execute("SELECT ProductSKU, ProductName, Description, ProductType FROM Product")
            data = cur.fetchall()
            return render_template("productview.html", headings=headings, data=data)
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
            _datetime = dtnow()
            _username = str(username)
            _sku = str(sku)
            upprod = " updated product sku " + _sku
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
                upproddict = {"User": _username, "Activity": upprod, "time": _datetime}
                jsonproducer.send("productinfo", upproddict)
                return redirect(url_for("productmenu"))
        return render_template("productupdate.html", form=form)
    else:
        return redirect(url_for("login"))

# Inventory Incoming (receive products from stores)
@app.route("/inventoryin", methods=["GET", "POST"])
def inventoryin():
    if "username" in session:
        username = session["username"]
        # fetch all store code
        cur = ksql.cursor()
        cur.execute("SELECT StoreCode FROM Store")
        storeexist = cur.fetchall()
        cur.close()

        # fetch all product sku
        cur = ksql.cursor()
        cur.execute("SELECT ProductSKU FROM Product")
        skuexist = cur.fetchall()
        cur.close()

        id = request.form.get('id')
        code = request.form.get('code')
        sku = request.form.get('sku')
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        today = date.today()
        curdate = today.strftime("%Y-%m-%d")
        now = datetime.now()
        curtime = now.strftime("%H:%M:%S")
        reason = request.form.get("reason")

        _datetime = dtnow()
        _username = str(username)
        _sku = str(sku)
        _quantity = int(quantity)
        _remark = str(reason)
        _code = str(code)
        activity = "inventory in from" + _code

        if request.method == "POST":
            # check for inventory ID
            cur = ksql.cursor()
            cur.execute("SELECT InventoryID FROM Inventory WHERE InventoryID = %s", (id,))
            exist = cur.fetchall()
            cur.close()
            # check if inventory id exist
            if not exist:
                empty = 0
                # insert new inventory id
                cur = ksql.cursor()
                cur.execute("INSERT INTO Inventory (InventoryID, StoreCode, ProductSKU, ProductName, QuantityCurrent, DateIn, TimeIn, QuantityOutgoing, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, code, sku, name, quantity, curdate, curtime, empty, reason))
                ksql.commit()
                cur.close()
                flash("Successfully received incoming inventory!")
                return redirect(url_for("productmenu"))
            elif not quantity or not quantity.isnumeric() or int(quantity) <= 0:
                flash("Please enter a valid quantity.")
                return render_template("inventoryin.html", storeexist=storeexist, skuexist=skuexist)
            elif not skuexist:
                flash("SKU does not exist! Please select another product SKU.")
                return render_template("inventoryin.html", storeexist=storeexist, skuexist=skuexist)
            elif not storeexist:
                flash("Code does not exist! Please select another store code.")
                return render_template("inventoryin.html", storeexist=storeexist, skuexist=skuexist)
            else:
                # check for inventory ID
                cur = ksql.cursor()
                cur.execute("SELECT InventoryID FROM Inventory WHERE InventoryID = %s", (id,))
                cur.fetchone()
                cur.close()
                if request.method == "POST":
                    cur = ksql.cursor()
                    cur.execute("SELECT QuantityCurrent FROM Inventory WHERE InventoryID = %s", (id,))
                    dataout = cur.fetchone()
                    result = int(quantity) + int(dataout[0])
                    cur.close()

                    cur = ksql.cursor()
                    cur.execute("Update Inventory SET QuantityCurrent = %s, DateIn = %s, TimeIn = %s, Reason = %s WHERE InventoryID = %s", (result, curdate, curtime, reason, id))
                    ksql.commit()
                    cur.close()
                    flash("Successfully updated incoming inventory!")
                    inventoryindict = {"User": _username, "Activity": activity, "time": _datetime, "Quantity": _quantity, "Product": _sku, "Remark":_remark}
                    jsonproducer.send("inventoryinfo", inventoryindict)
                    return redirect(url_for("productmenu"))
                else:
                    flash("Error")
                    return render_template("inventoryin.html", storeexist=storeexist, skuexist=skuexist)
        else:
            return render_template("inventoryin.html", storeexist=storeexist, skuexist=skuexist)
    else:
        return redirect(url_for("login"))


# Inventory Outgoing (receive products from stores)
@app.route("/inventoryout", methods=["GET", "POST"])
def inventoryout():
    if "username" in session:
        username = session["username"]
        # fetch all store code
        cur = ksql.cursor()
        cur.execute("SELECT StoreCode FROM Store")
        storeexist = cur.fetchall()
        cur.close()

        # fetch all product sku
        cur = ksql.cursor()
        cur.execute("SELECT ProductSKU FROM Product")
        skuexist = cur.fetchall()
        cur.close()

        id = request.form.get('id')
        code = request.form.get('code')
        sku = request.form.get('sku')
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        today = date.today()
        curdate = today.strftime("%Y-%m-%d")
        now = datetime.now()
        curtime = now.strftime("%H:%M:%S")

        _datetime = dtnow()
        _username = str(username)
        _sku = str(sku)
        _quantity = int(quantity)
        _remark = str(code)
        _code = str(code)
        activity = "inventory out to" + _code

        if request.method == "POST":
            # check for inventory ID
            cur = ksql.cursor()
            cur.execute("SELECT InventoryID FROM Inventory WHERE InventoryID = %s", (id,))
            exist = cur.fetchall()
            cur.close()
            # check if inventory id exist
            if not exist:
                empty = 0
                # enter a valid inventory out id
                cur = ksql.cursor()
                cur.execute(
                    "INSERT INTO Inventory (InventoryID, StoreCode, ProductSKU, ProductName, QuantityCurrent, QuantityOutgoing, DateOut, TimeOut) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, code, sku, name, empty, quantity, curdate, curtime))
                ksql.commit()
                cur.close()
                flash("Successfully sent outgoing inventory!")
                return redirect(url_for("productmenu"))
            elif not quantity or not quantity.isnumeric() or int(quantity) <= 0:
                flash("Please enter a valid quantity.")
                return render_template("inventoryout.html", storeexist=storeexist, skuexist=skuexist)
            elif not skuexist:
                flash("SKU does not exist! Please select another product SKU.")
                return render_template("inventoryout.html", storeexist=storeexist, skuexist=skuexist)
            elif not storeexist:
                flash("Code does not exist! Please select another store code.")
                return render_template("inventoryout.html", storeexist=storeexist, skuexist=skuexist)
            else:
                # check for inventory ID
                cur = ksql.cursor()
                cur.execute("SELECT InventoryID FROM Inventory WHERE InventoryID = %s", (id,))
                cur.fetchone()
                cur.close()
                if request.method == "POST":
                    # delete current quantity
                    #cur = ksql.cursor()
                    #cur.execute("SELECT QuantityCurrent FROM Inventory WHERE InventoryID = %s", (id,))
                    #datain = cur.fetchone()
                    #resultin = int(datain[0]) - int(quantity)
                    #cur.close()

                    # record outgoing quantity
                    cur = ksql.cursor()
                    cur.execute("SELECT QuantityOutgoing FROM Inventory WHERE InventoryID = %s", (id,))
                    dataout = cur.fetchone()
                    resultout = int(quantity) + int(dataout[0])
                    cur.close()

                    cur = ksql.cursor()
                    cur.execute("Update Inventory SET QuantityOutgoing = %s, DateOut = %s, TimeOut = %s WHERE InventoryID = %s", (resultout, curdate, curtime, id))
                    ksql.commit()
                    cur.close()
                    flash("Successfully updated outgoing inventory!")
                    inventoryoutdict = {"User": _username, "Activity": activity, "time": _datetime, "Quantity": _quantity, "Product": _sku, "Remark": _remark}
                    jsonproducer.send("inventoryinfo", inventoryoutdict)
                    return redirect(url_for("productmenu"))
                else:
                    flash("Error")
                    return render_template("inventoryout.html", storeexist=storeexist, skuexist=skuexist)
        else:
            return render_template("inventoryout.html", storeexist=storeexist, skuexist=skuexist)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            addstore = " added store code " + _code
            cur = ksql.cursor()
            cur.execute("SELECT StoreCode FROM Store WHERE StoreCode = %s",(code,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Store (StoreCode, Location, Address) VALUES (%s, %s, %s)",(code, location, address))
                ksql.commit()
                flash("Store added!")
                addstoredict = {"User": _username, "Activity": addstore, "time": _datetime}
                jsonproducer.send("storeinfo", addstoredict)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            delstore = " deleted store code " + _code
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
                delstoredict = {"User": _username, "Activity": delstore, "time": _datetime}
                jsonproducer.send("storeinfo", delstoredict)
                return redirect(url_for("storemenu"))
        return render_template("storedelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Store Search
#@app.route("/storesearch", methods=["GET", "POST"])
#def storesearch():
#    if "username" in session:
#        username = session["username"]
#        form = StoreSearchForm()
#        if form.validate_on_submit():
#            return redirect(url_for("storesearch"))
#        return render_template("storesearch.html", form=form)
#    else:
#        return redirect(url_for("login"))

# Store View
@app.route("/storeview", methods=["GET", "POST"])
def storeview():
    if "username" in session:
        username = session["username"]
        headings = ("StoreCode", "Store Location", "Store Address")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Store LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No stores saved!")
            return redirect(url_for("storemenu"))
        else:
            cur.execute("SELECT StoreCode, Location, Address FROM Store")
            data = cur.fetchall()
            return render_template("storeview.html", headings=headings, data=data)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            upstore = " updated store code " + _code
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
                upstoredict = {"User": _username, "Activity": upstore, "time": _datetime}
                jsonproducer.send("storeinfo", upstoredict)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            addsup = " added supplier code " + _code
            cur = ksql.cursor()
            cur.execute("SELECT SupplierCode FROM Supplier WHERE SupplierCode = %s", (code,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Supplier (SupplierCode, SupplierName, SupplierPhone, SupplierAddress) VALUES (%s, %s, %s, %s)", (code,name, phone, address))
                ksql.commit()
                flash("Supplier added!")
                addsupdict = {"User": _username, "Activity": addsup, "time": _datetime}
                jsonproducer.send("supplierinfo", addsupdict)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            delsup = " deleted supplier code " + _code
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
                delsupdict = {"User": _username, "Activity": delsup, "time": _datetime}
                jsonproducer.send("supplierinfo", delsupdict)
                return redirect(url_for("suppliermenu"))
        return render_template("supplierdelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Supplier Search
#@app.route("/suppliersearch", methods=["GET", "POST"])
#def suppliersearch():
#    if "username" in session:
#        username = session["username"]
#        form = SupplierSearchForm()
#        if form.validate_on_submit():
#            return redirect(url_for("suppliersearch"))
#        return render_template("suppliersearch.html", form=form)
#    else:
#        return redirect(url_for("login"))

# Supplier View
@app.route("/supplierview", methods=["GET", "POST"])
def supplierview():
    if "username" in session:
        username = session["username"]
        headings = ("Supplier Code", "Supplier Name", "Supplier Phone", "Supplier Address")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Supplier LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No suppliers saved!")
            return redirect(url_for("suppliermenu"))
        else:
            cur.execute(
                "SELECT SupplierCode, SupplierName, SupplierPhone, SupplierAddress FROM Supplier")
            data = cur.fetchall()
            return render_template("supplierview.html", headings=headings, data=data)
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
            _datetime = dtnow()
            _username = str(username)
            _code = str(code)
            upsup = " updated supplier code " + _code
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
                upsupdict = {"User": _username, "Activity": upsup, "time": _datetime}
                jsonproducer.send("supplierinfo", upsupdict)
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
        form = AdminAddForm()
        if form.validate_on_submit():
            req = request.form
            name = request.form["name"]
            username1 = request.form["username"]
            password = request.form["password"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            type = "Admin"
            _datetime = dtnow()
            _username = str(username)
            _username1 = str(username1)
            addadm = " added admin username " + _username1
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username1,))
            exist = cur.fetchall()
            if not exist:
                cur.execute("INSERT INTO Admin (FullName, Username, AdminPW, AdminPhone, AdminAddress, AdminEmail, Type) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, username1, password, phone, address, email, type))
                ksql.commit()
                flash("Admin account created!")
                addadmindict = {"User": _username, "Activity": addadm, "time": _datetime}
                jsonproducer.send("admininfo", addadmindict)
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
            username1 = request.form["username"]
            _datetime = dtnow()
            _username = str(username)
            _username1 = str(username1)
            deladm = " deleted admin username " + _username1
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username1,))
            exist = cur.fetchall()
            if not exist:
                flash("Admin account does not exist! Please enter another username.")

                return redirect(url_for("admindelete"))
            else:
                cur.execute("DELETE FROM Admin WHERE Username = %s", (username1,))
                ksql.commit()
                flash("Admin deleted!")
                deladmindict = {"User": _username, "Activity": deladm, "time": _datetime}
                jsonproducer.send("admininfo", deladmindict)
                return redirect(url_for("adminmenu"))
        return render_template("admindelete.html", form=form)
    else:
        return redirect(url_for("login"))

# Admin Search
#@app.route("/adminsearch", methods=["GET", "POST"])
#def adminsearch():
#    if "username" in session:
#        username = session["username"]
#        form = AdminSearchForm()
#        if form.validate_on_submit():
#            return redirect(url_for("adminsearch"))
#        return render_template("adminsearch.html", form=form)
#    else:
#        return redirect(url_for("login"))

# Admin View
@app.route("/adminview", methods=["GET", "POST"])
def adminview():
    if "username" in session:
        username = session["username"]
        headings = ("Username", "FullName", "Password", "Phone Number", "Home Address", "Email Address")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Admin LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No admin accounts!")
            return redirect(url_for("adminmenu"))
        else:
            cur.execute("SELECT Username, FullName, AdminPW, AdminPhone, AdminAddress, AdminEmail FROM Admin")
            data = cur.fetchall()
            return render_template("adminview.html", headings=headings, data=data)
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
            username1 = request.form["username"]
            password = request.form["password"]
            phone = request.form["phone"]
            email = request.form["email"]
            address = request.form["address"]
            _datetime = dtnow()
            _username = str(username)
            _username1 = str(username1)
            upadm = " updated admin username " + _username1
            cur = ksql.cursor()
            cur.execute("SELECT Username FROM Admin WHERE Username = %s", (username1,))
            exist = cur.fetchall()
            if not exist:
                flash("Username does not exist! Please enter another username.")
                return render_template("adminupdate.html", form=form)
            else:
                cur.execute("UPDATE Admin SET FullName = %s, AdminPW = %s, AdminPhone = %s, AdminAddress = %s, AdminEmail = %s WHERE Username = %s", (name, password, phone, address, email, username1))
                ksql.commit()
                flash("Admin account updated!")
                upadmindict = {"User": _username, "Activity": upadm, "time": _datetime}
                jsonproducer.send("admininfo", upadmindict)
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
        headings = ("StockSKU", "StockName", "Supplier Code", "Quantity (Current)", "Date", "Time")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Stock LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No stocks in the warehouse!")
            return redirect(url_for("adminhome"))
        else:
            cur.execute("SELECT StockSKU, StockName, SupplierCode, QuantityCurrent, DateIn, TimeIn FROM Stock")
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

# View supervisor Profile
@app.route("/supervisorprofile", methods=["GET", "POST"])
def supervisorprofile():
    if "username" in session:
        username = session["username"]
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT Username, FullName, SupervisorPW, SupervisorPhone, SupervisorAddress, SupervisorEmail FROM Supervisor WHERE Username = %s", (username,))
        userfound = cur.fetchone()
        ksql.commit()
        return render_template("supervisorprofile.html", userfound=userfound)
    else:
        return redirect(url_for("login"))

# View Stock Return
@app.route("/viewstockreturn", methods=["GET", "POST"])
def viewstockreturn():
    if "username" in session:
        username = session["username"]
        headings = ("StockSKU", "StockName", "SupplierCode", "Quantity (Outgoing)", "Date", "Time", "Reason")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT * FROM Stock LIMIT 1")
        exist = cur.fetchall()
        if not exist:
            flash("No stocks in the warehouse!")
            return redirect(url_for("supervisorhome"))
        else:
            cur.execute("SELECT StockSKU, StockName, SupplierCode, QuantityOutgoing, DateOut, TimeOut, Reason FROM Stock")
            data = cur.fetchall()
            return render_template("viewstockreturn.html", headings=headings, data=data)
        # return render_template("viewstockreturn.html")
    else:
        return redirect(url_for("login"))


# ===========================
# View Monthly Report
@app.route("/viewreport", methods=["GET", "POST"])
def viewreport():
    if "username" in session:
        username = session["username"]
        return render_template("viewreport.html")
    else:
        return redirect(url_for("login"))

@app.route("/adjustmentout", methods=["GET", "POST"])
def adjustmentout():
    if "username" in session:
        username = session["username"]
        # fetch all supplier code
        cur = ksql.cursor()
        cur.execute("SELECT SupplierCode FROM Supplier")
        supplyexist = cur.fetchall()
        cur.close()

        # fetch all stock sku
        cur = ksql.cursor()
        cur.execute("SELECT StockSKU FROM Stock")
        stockexist = cur.fetchall()
        cur.close()

        sku = request.form.get("sku")
        name = request.form.get("name")
        code = request.form.get("code")
        quantity = request.form.get("quantity")
        reason = request.form.get("reason")
        today = date.today()
        curdate = today.strftime("%Y-%m-%d")
        now = datetime.now()
        curtime = now.strftime("%H:%M:%S")

        _datetime = dtnow()
        _username = str(username)
        _sku = str(sku)
        _quantity = int(quantity)
        _remark = str(reason)
        _code = str(code)
        activity = "adjustment out to" + _code

        if request.method == "POST":
            # check if stock sku
            cur = ksql.cursor()
            cur.execute("SELECT StockSKU FROM Stock WHERE StockSKU = %s", (sku,))
            exist = cur.fetchall()
            cur.close()
            # check if stock sku exist
            if not exist:
                empty = 0
                # insert new stock sku
                # should enter a valid stock sku
                cur = ksql.cursor()
                cur.execute("INSERT INTO Stock (StockSKU, StockName, SupplierCode, QuantityCurrent, QuantityOutgoing, DateOut, TimeOut, Reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(sku, name, code, empty, quantity, curdate, curtime, reason))
                ksql.commit()
                cur.close()
                flash("Successfully sent stocks!")
                return redirect(url_for("supervisorhome"))
            elif not quantity or not quantity.isnumeric() or int(quantity) <= 0:
                flash("Please enter a valid quantity.")
                return render_template("adjustmentout.html", supplyexist=supplyexist, stockexist=stockexist)
            elif not supplyexist:
                flash("Code does not exist! Please select a valid supplier code.")
                return render_template("adjustmentout.html", supplyexist=supplyexist, stockexist=stockexist)
            else:
                # check for stock sku
                cur = ksql.cursor()
                cur.execute("SELECT StockSKU FROM Stock WHERE StockSKU = %s", (sku,))
                cur.fetchall()
                cur.close()

                # check is outgoing quantity is NULL
                # record outgoing quantity
                cur = ksql.cursor()
                cur.execute("SELECT QuantityOutgoing FROM Stock WHERE QuantityOutgoing IS NULL")
                dataout = cur.fetchall()
                if not dataout:
                    flash("False Error")
                    return render_template("adjustmentout.html", supplyexist=supplyexist, stockexist=stockexist)
                else:
                    # insert value
                    cur = ksql.cursor()
                    cur.execute("SELECT QuantityOutgoing FROM Stock WHERE StockSKU = %s", (sku,))
                    data = cur.fetchone()
                    result = int(quantity) + int(data[0])
                    cur.close()

                    cur = ksql.cursor()
                    cur.execute(
                        "Update Stock SET QuantityOutgoing = %s, DateOut = %s, TimeOut = %s, Reason = %s WHERE StockSKU = %s",
                        (result, curdate, curtime, reason, sku))
                    ksql.commit()
                    cur.close()
                    flash("Outgoing stocks successfully sent!")
                    adjustmentoutdict = {"User": _username, "Activity": activity, "time": _datetime, "Quantity": _quantity, "Product": _sku, "Remark": _remark}
                    jsonproducer.send("adjustmentinfo", adjustmentoutdict)
                    return redirect(url_for("supervisorhome"))
        else:
            return render_template("adjustmentout.html", supplyexist=supplyexist, stockexist=stockexist)
    else:
        return redirect(url_for("login"))

#=========================================================
#kafka
@app.route("/kafka", methods = ["GET","POST"])
def kafka():
    consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'])
    topics = consumer.topics()
    topic = list(topics)

    #check kafka consumer status
    print(topics)
    if not topics:
        server_status = "server not running"
    else:
        server_status = "Server running"


    return render_template('consumer.html', server_status = server_status, len = len(topic),
                           topic = topic)



#consume and send to sql
@app.route("/topicsearch", methods=["GET", "POST"])
def topicsearch():

    #list topics and show server status
    consumermain = KafkaConsumer(bootstrap_servers=['localhost:9092'])
    topics = consumermain.topics()
    topic = list(topics)
    if not topics:
        server_status = "server not running"
    else:
        server_status = "Server running"

    form = TopicForm()
    if request.method == "POST":

    #if form.validate_on_submit():
        #print("not consumed")

        #topic = request.form["topic"]
        #cur1 = ksql.cursor()
        #consumer = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"],
                                 #auto_offset_reset="earliest", enable_auto_commit=True,
                                 #consumer_timeout_ms=1000,
                                 #value_deserializer=lambda m: json.loads(m.decode("utf-8"))
                                 #)
        #for i in consumer:
            #message = i.value
            #_message = str(message)
            #if "Quantity" in message:
                #msgdct = {"User": message["User"], "Activity": message["Activity"], "time": message["time"],
                          #"Quantity": message["Quantity"], "Product": message["Product"] , "Remark":message["Remark"] }
                #print("test1: " + _message)
                #cur1.execute("INSERT IGNORE INTO topic (user, activity, date, quantity, topic, product, remark) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                            #(msgdct["User"], msgdct["Activity"], msgdct["time"], msgdct["Quantity"], topic, msgdct["Product"], msgdct["Remark"],))


            #else:
                #msgdct = {"User": message["User"], "Activity": message["Activity"], "time": message["time"]}
                #print("test2: " + _message)
                #cur1.execute("INSERT IGNORE INTO topic (user, activity, date, topic) VALUES(%s,%s,%s,%s)",
                            #(msgdct["User"], msgdct["Activity"], msgdct["time"], topic,))

        #print(" consumed")
        #ksql.commit()

        return redirect(url_for('topicselect'))
    return render_template("topicsearch.html",  server_status = server_status, len = len(topic), topic = topic)


# topic select
@app.route('/topicselect', methods=['GET', 'POST'])
def topicselect():

    if request.method == 'POST':
        topic = request.form.get('topic')
        cur1 = ksql.cursor()
        consumer = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"],
                                 auto_offset_reset="earliest", enable_auto_commit=True,
                                 consumer_timeout_ms=1000,
                                 value_deserializer=lambda m: json.loads(m.decode("utf-8"))
                                 )
        for i in consumer:
            message = i.value
            _message = str(message)
            if "Quantity" in message:
                msgdct = {"User": message["User"], "Activity": message["Activity"], "time": message["time"],
                          "Quantity": message["Quantity"], "Product": message["Product"] , "Remark":message["Remark"] }
                print("test1: " + _message)
                cur1.execute("INSERT IGNORE INTO topic (user, activity, date, quantity, topic, product, remark) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                            (msgdct["User"], msgdct["Activity"], msgdct["time"], msgdct["Quantity"], topic, msgdct["Product"], msgdct["Remark"],))
                ksql.commit()
            else:
                msgdct = {"User": message["User"], "Activity": message["Activity"], "time": message["time"]}
                print("test2: " + _message)
                cur1.execute("INSERT IGNORE INTO topic (user, activity, date, topic) VALUES(%s,%s,%s,%s)",
                            (msgdct["User"], msgdct["Activity"], msgdct["time"], topic,))
                ksql.commit()
                # for the headers in the table

        heading1 = ("User", "Date", "Activity, Quantity, Product, Remark")
        #heading1 = ("User", "Date", "Activity, Quantity")
        heading = ("User", "Date", "Activity")
        cur = ksql.cursor(buffered=True)
        cur.execute("SELECT quantity FROM topic WHERE topic = %s", (topic,))
        exist = cur.fetchone()
        if "None" in str(exist):
            print(exist)
            cur.execute("SELECT user, date, activity FROM topic WHERE topic = %s", (topic,))
            record = cur.fetchall()
            return render_template("topicselect.html", record=record, heading=heading)
        else:
            print(exist)
            cur.execute("SELECT user, date, activity, quantity, product, remark FROM topic WHERE topic = %s", (topic,))
            record = cur.fetchall()
            return render_template("topicselect.html", record=record, heading=heading1)

    return render_template('topicselect.html')


if __name__ =="__main__":
    app.run(debug = True)
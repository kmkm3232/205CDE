from flask import Flask, render_template, request, session, redirect, flash, url_for
import pymysql
from datetime import *
app = Flask(__name__)
app.secret_key = " "
db = pymysql.connect("0.0.0.0","root","99765372","205DB")

@app.route('/')
def index():
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Product ORDER BY RAND() LIMIT 8""")
	suggest = cursor.fetchall()
	return render_template('index.html', suggest=suggest)

@app.route('/login', methods=['POST'])
def result():
	p_l_usrname = request.form["html_uname"]
	p_l_pwd = request.form["html_pwd"]
	cursor = db.cursor()
	if cursor.execute("""SELECT * FROM User WHERE (UserName, UserPassword) = (%s, %s)""",(p_l_usrname,p_l_pwd)):
		session['logged_in'] = True
		session['username'] = request.form['html_uname']
		session['password'] = request.form['html_pwd']
		flash('Logged in as ' + p_l_usrname)
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product ORDER BY RAND() LIMIT 8""")
		suggest = cursor.fetchall()
		return render_template("index.html", suggest=suggest)
	else:
		flash('Wrong Username or Password!')
		return render_template("login.html")

@app.route('/login')
def login():
	return render_template("login.html")
    
@app.route('/logout')
def logout():
	session['logged_in'] = False
	session['username'] = 'Login'
	flash('Logged out')
	return redirect("http://localhost:8000/")

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/registed', methods = ['POST', 'GET'])
def check_register():
	error = None
	p_r_usrname = request.form["html_r_uname"]
	p_r_pwd = request.form["html_r_pwd"]
	p_r_email = request.form["html_r_email"]
	p_r_fname = request.form["html_r_fname"]
	p_r_lname = request.form["html_r_lname"]
	p_r_phone = request.form["html_r_phone"]
	p_r_address = request.form["html_r_address"]
	p_r_birthdate = request.form["html_r_birthofdate"]
	cursor = db.cursor()
	if cursor.execute("""SELECT * FROM User WHERE UserName = (%s)""",(p_r_usrname)):
		flash('Username has been taken by others, Please another one!')
		return render_template("register.html")
	else:
		cursor.execute("""INSERT INTO User (UserName, UserPassword, Email, FirstName, LastName, Phone, Address, BirthDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(p_r_usrname, p_r_pwd, p_r_email, p_r_fname, p_r_lname, p_r_phone, p_r_address, p_r_birthdate))
		db.commit()
		flash('Congrazts You have registed Now Login to Shop!')
		return redirect("http://localhost:8000/")

@app.route('/aboutus')
def aboutus():
	return render_template('aboutus.html')

@app.route('/ptable')
def ptable():
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Product """)
	ap = cursor.fetchall()
	cursor = db.cursor()
	cursor.execute("""SELECT DISTINCT ProductType FROM Product """)
	tyype = cursor.fetchall()
	return render_template('ptable.html', ap=ap,tyype=tyype)

@app.route('/shoppingcart')
def sc():
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Product """)
	app = cursor.fetchall()
	session['app'] = app
	return render_template('shoppingcart.html')

@app.route('/addtocart', methods = ['POST', 'GET'])
def atc():
	if "cart" not in session:
		session['cart'] = []
	added = False
	targetPid = request.form["productid"]
	targetpName = request.form["productname"]
	targetpPrice = request.form["productprice"]
	targetpQuantity = request.form["addtocartquantity"]
	if session['cart'] == []:
		session['cart'].append([targetPid,targetpName,targetpPrice,targetpQuantity])
		session.modified = True
	else:
		for i in session['cart']:
			if targetPid == i[0]:
				a=int(i[3])
				b=int(targetpQuantity)
				newq = a+b
				i[3]=newq
				session.modified = True
				added = True
				break
		if not added:
			session['cart'].append([targetPid,targetpName,targetpPrice,targetpQuantity])
			session.modified = True
	flash('Added '+targetpQuantity+' '+targetpName+' '+'to shopping cart.' )
	return redirect("http://localhost:8000/ptable")

@app.route('/remove', methods=['POST', 'GET'])
def remove():
    removeitem = request.form["removeitem"]
    for i in session['cart']:
        if removeitem == i[0]:
           session['cart'].remove(i)
           session.modified = True
           break
    return render_template('shoppingcart.html')

@app.route('/update', methods=['POST', 'GET'])
def update():
    updateitem = request.form["updateitem"]
    updatequantity = request.form["qt"]
    for i in session['cart']:
        if updateitem == i[0]:
           i[3] = updatequantity
           session.modified = True
           break
    flash('Updated!')
    return render_template('shoppingcart.html')
@app.route('/checkoutCash', methods=['POST', 'GET'])
def coc():
	if session['logged_in'] == True:
		totalp = 0
		for i in session['cart']:
			totalp += float(i[2]) * float(i[3])
		deshop = request.form["shoplist"]
		uname = session['username']
		pmethod = 'Cash' 
		cursor = db.cursor()
		cursor.execute("""SELECT UserID FROM User WHERE (UserName) = (%s)""",(uname))
		userid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""INSERT INTO Orders (UserID, TotalPrice, OrderDate) VALUES (%s, %s, %s)""",(userid[0], totalp, date.today() ))
		cursor = db.cursor()
		cursor.execute("""SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1;""")
		oid = cursor.fetchall()
		cursor = db.cursor()
		for i in session['cart']:
			cursor.execute("""INSERT INTO Orders_Item (OrderID) VALUES(%s)""",(oid[0]))
			cursor = db.cursor()
			cursor.execute("""UPDATE Orders_Item SET ProductID = (%s) ORDER BY Orders_Item_ID DESC LIMIT 1;""",(i[0]))
			cursor = db.cursor()
			cursor.execute("""UPDATE Orders_Item SET Quantity = (%s) ORDER BY Orders_Item_ID DESC LIMIT 1;""",(int(i[3])))
		cursor = db.cursor()
		cursor.execute("""INSERT INTO Payment(PaymentMethod) VALUES (%s)""",(pmethod))
		cursor = db.cursor()
		cursor.execute("""INSERT INTO Cash_Payment(PaymentID) SELECT PaymentID FROM Payment ORDER BY PaymentID DESC LIMIT 1;""")
		cursor = db.cursor()
		cursor.execute("""UPDATE Cash_Payment SET DeilveryShop = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(deshop))
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentID FROM Payment ORDER BY PaymentID DESC LIMIT 1;""")
		payid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""UPDATE Orders SET PaymentID = (%s) ORDER BY OrderID DESC LIMIT 1;""",(payid[0]))
		db.commit()
		session['cart'] = []
		session.modified = True
		flash("Thank you! Your order was received! Go to my account for information or keep shopping!")
		return redirect("http://localhost:8000/")
	else:
		flash('Login for payment !')
		return render_template('login.html')
@app.route('/checkoutCredit', methods=['POST','GET'])
def cocc():
	if session['logged_in'] == True:
		totalp = 0
		for i in session['cart']:
			totalp += float(i[2]) * float(i[3])
		c1 = request.form["creditcardnum"]
		c2 = request.form["duedate"]
		c3 = request.form["pin"]
		c4 = request.form["fname"]
		c5 = request.form["lname"]
		c6 = request.form["address"]
		c7 = request.form["address2"]
		c8 = request.form["countryregion"]
		c9 = request.form["city"]
		c10	= request.form["pcode"]
		c11	= request.form["phonenum"]
		uname = session['username']
		pmethod = 'CreditCard' 
		cursor = db.cursor()
		cursor.execute("""SELECT UserID FROM User WHERE (UserName) = (%s)""",(uname))
		userid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""INSERT INTO Orders (UserID, TotalPrice, OrderDate) VALUES (%s, %s, %s)""",(userid[0], totalp, date.today() ))
		cursor = db.cursor()
		cursor.execute("""SELECT OrderID FROM Orders ORDER BY OrderID DESC LIMIT 1;""")
		oid = cursor.fetchall() 
		cursor = db.cursor()
		for i in session['cart']:
			cursor.execute("""INSERT INTO Orders_Item (OrderID) VALUES(%s)""",(oid[0]))
			cursor = db.cursor()
			cursor.execute("""UPDATE Orders_Item SET ProductID = (%s) ORDER BY Orders_Item_ID DESC LIMIT 1;""",(i[0]))
			cursor = db.cursor()
			cursor.execute("""UPDATE Orders_Item SET Quantity = (%s) ORDER BY Orders_Item_ID DESC LIMIT 1;""",(int(i[3])))
		cursor = db.cursor()
		cursor.execute("""INSERT INTO Payment(PaymentMethod) VALUES (%s)""",(pmethod))
		cursor = db.cursor()
		cursor.execute("""INSERT INTO CreditCard_Payment(PaymentID) SELECT PaymentID FROM Payment ORDER BY PaymentID DESC LIMIT 1;""")
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET CardNumber = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c1))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET DueDate = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c2))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET PIN = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c3))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET FirstName = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c4))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET LastName = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c5))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET Address = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c6))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET Address2 = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c7))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET CountryRegion = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c8))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET City = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c9))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET PostalCode = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c10))
		cursor = db.cursor()
		cursor.execute("""UPDATE CreditCard_Payment SET Phone = (%s) ORDER BY PaymentID DESC LIMIT 1;""",(c11))
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentID FROM Payment ORDER BY PaymentID DESC LIMIT 1;""")
		payid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""UPDATE Orders SET PaymentID = (%s) ORDER BY OrderID DESC LIMIT 1;""",(payid[0]))
		db.commit()
		session['cart'] = []
		session.modified = True
		flash("Thank you! Your order was received! Go to my account for information or keep shopping!")
		return redirect("http://localhost:8000/")
	else:
		flash('Login for payment !')
		return render_template('login.html')
@app.route('/vieworder')
def ohistory():
	uname = session['username']
	cursor = db.cursor()
	cursor.execute("""SELECT UserID FROM User WHERE (UserName) = (%s)""",(uname))
	userid = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders WHERE (UserID) = (%s)""",(userid))
	odata = cursor.fetchall()
	return render_template('vieworder.html', odata=odata)
@app.route('/editorder', methods=['POST','GET'])
def editorder():
	targetoid = request.form["editorder"]
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	currentorder = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	paymentid = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
	paymentmethod = cursor.fetchone()	
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	orderedproduct = []
	for i in itemlist:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
		prd = cursor.fetchone()
		orderedproduct.append(prd)
	db.commit()
	return render_template('editorder.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/editorderadmin', methods=['POST','GET'])
def editordera():
	targetoid = request.form["editorder"]
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	currentorder = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	paymentid = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
	paymentmethod = cursor.fetchone()	
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	orderedproduct = []
	for i in itemlist:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
		prd = cursor.fetchone()
		orderedproduct.append(prd)
	db.commit()
	return render_template('editorderadmin.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/removeorder',methods=['POST','GET'])
def rmo():
	targetoid = request.form["removeorder"]
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders_Item WHERE (OrderID) = (%s)""",(int(targetoid)))
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders WHERE (OrderID) = (%s)""",(int(targetoid)))
	db.commit()
	return redirect("http://localhost:8000/vieworder")
@app.route('/removeorderadmin',methods=['POST','GET'])
def rmoa():
	targetoid = request.form["removeorder"]
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders_Item WHERE (OrderID) = (%s)""",(int(targetoid)))
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders WHERE (OrderID) = (%s)""",(int(targetoid)))
	db.commit()
	return redirect("http://localhost:8000/admino")
@app.route('/removeitem',methods=['POST','GET'])
def rmi():
	targetitemid = request.form["removeitem"]
	targetoid = request.form["orderidd"]
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders_Item WHERE (OrderID) = (%s) AND (ProductID) = (%s)""",(int(targetoid), targetitemid))
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	newtotal = 0
	for i in itemlist:
		existpid = i[1]
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE (ProductID)= (%s)""",(existpid))
		existprice = cursor.fetchone()
		newtotal += int(i[2])*int(existprice[2])
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders SET TotalPrice = (%s) WHERE OrderID = (%s)""",(newtotal, targetoid))
	if newtotal == 0:
		cursor =db.cursor()
		cursor.execute("""DELETE FROM Orders WHERE (OrderID) = (%s)""",(int(targetoid)))
		db.commit()
		return redirect("http://localhost:8000/vieworder")
	else:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
		currentorder = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
		paymentid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
		paymentmethod = cursor.fetchone()	
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
		itemlist = cursor.fetchall()
		orderedproduct = []
		for i in itemlist:
			cursor = db.cursor()
			cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
			prd = cursor.fetchone()
			orderedproduct.append(prd)
		db.commit()
		return render_template('editorder.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/removeitema',methods=['POST','GET'])
def rmia():
	targetitemid = request.form["removeitem"]
	targetoid = request.form["orderidd"]
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders_Item WHERE (OrderID) = (%s) AND (ProductID) = (%s)""",(int(targetoid), targetitemid))
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	newtotal = 0
	for i in itemlist:
		existpid = i[1]
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE (ProductID)= (%s)""",(existpid))
		existprice = cursor.fetchone()
		newtotal += int(i[2])*int(existprice[2])
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders SET TotalPrice = (%s) WHERE OrderID = (%s)""",(newtotal, targetoid))
	if newtotal == 0:
		cursor =db.cursor()
		cursor.execute("""DELETE FROM Orders WHERE (OrderID) = (%s)""",(int(targetoid)))
		db.commit()
		return redirect("http://localhost:8000/vieworder")
	else:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
		currentorder = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
		paymentid = cursor.fetchone()
		cursor = db.cursor()
		cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
		paymentmethod = cursor.fetchone()	
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
		itemlist = cursor.fetchall()
		orderedproduct = []
		for i in itemlist:
			cursor = db.cursor()
			cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
			prd = cursor.fetchone()
			orderedproduct.append(prd)
		db.commit()	
		return render_template('admino.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/edititem',methods=['POST','GET'])
def emi():
	targetpid = request.form["edititempid"]
	targetoid = request.form["edititemoid"]
	targetpquantity = request.form["qt"]
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders_Item SET Quantity = (%s) WHERE OrderID = (%s) AND ProductID = (%s)""",(targetpquantity, targetoid, targetpid))
	newtotal = 0
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	for i in itemlist:
		existpid = i[1]
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE (ProductID)= (%s)""",(existpid))
		existprice = cursor.fetchone()
		newtotal += int(i[2])*int(existprice[2])
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders SET TotalPrice = (%s) WHERE OrderID = (%s)""",(newtotal, targetoid))
	db.commit()
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	currentorder = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	paymentid = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
	paymentmethod = cursor.fetchone()	
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	orderedproduct = []
	for i in itemlist:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
		prd = cursor.fetchone()
		orderedproduct.append(prd)
	return render_template('editorder.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/edititema',methods=['POST','GET'])
def emia():
	targetpid = request.form["edititempid"]
	targetoid = request.form["edititemoid"]
	targetpquantity = request.form["qt"]
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders_Item SET Quantity = (%s) WHERE OrderID = (%s) AND ProductID = (%s)""",(targetpquantity, targetoid, targetpid))
	newtotal = 0
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	for i in itemlist:
		existpid = i[1]
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE (ProductID)= (%s)""",(existpid))
		existprice = cursor.fetchone()
		newtotal += int(i[2])*int(existprice[2])
	cursor = db.cursor()
	cursor.execute("""UPDATE Orders SET TotalPrice = (%s) WHERE OrderID = (%s)""",(newtotal, targetoid))
	db.commit()
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	currentorder = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentID FROM Orders WHERE (OrderID) = (%s)""",(targetoid))
	paymentid = cursor.fetchone()
	cursor = db.cursor()
	cursor.execute("""SELECT PaymentMethod FROM Payment WHERE (PaymentID) = (%s)""",(paymentid[0]))
	paymentmethod = cursor.fetchone()	
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Orders_Item WHERE (OrderID)= (%s)""",(targetoid))
	itemlist = cursor.fetchall()
	orderedproduct = []
	for i in itemlist:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product WHERE ProductID = (%s)""",(i[1]))
		prd = cursor.fetchone()
		orderedproduct.append(prd)
	return render_template('editorderadmin.html', targetoid=targetoid, paymentmethod=paymentmethod, itemlist=itemlist, orderedproduct=orderedproduct)
@app.route('/personaldata')
def psd():
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM User WHERE UserName = (%s)""",(session['username']))
	pdata = cursor.fetchall()
	return render_template('personaldata.html', pdata=pdata)
@app.route('/editpersonaldata', methods=['POST','GET'])
def epd():
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM User WHERE UserName = (%s)""",(session['username']))
	pdata = cursor.fetchall()
	return render_template('editpersonaldata.html', pdata=pdata)
@app.route('/submitpersonaldata', methods=['POST','GET'])
def spd():
	uname = session['username']
	p_r_pwd = request.form["html_r_pwd"]
	p_r_email = request.form["html_r_email"]
	p_r_fname = request.form["html_r_fname"]
	p_r_lname = request.form["html_r_lname"]
	p_r_phone = request.form["html_r_phone"]
	p_r_address = request.form["html_r_address"]
	p_r_birthdate = request.form["html_r_birthofdate"]
	cursor = db.cursor()
	cursor.execute("""UPDATE User SET UserPassword = (%s), Email = (%s), FirstName = (%s), LastName = (%s), Phone = (%s), Address = (%s), BirthDate = (%s) WHERE UserName = (%s)""",(p_r_pwd, p_r_email, p_r_fname, p_r_lname, p_r_phone, p_r_address, p_r_birthdate, uname))
	db.commit()
	return redirect("http://localhost:8000/personaldata")

@app.route('/admin')
def adminp():
	return render_template('/admin.html')
@app.route('/adminlogin', methods=['POST','GET'])
def adminl():
	getid = request.form["adminname"]
	getpassword = request.form["adminpw"]
	if getid == 'admin' and getpassword =='password':
		session['adminloggedin'] = True
		return render_template('/adminpanel.html')
	else:
		flash('Wrong id or wrong password')
		return render_template('/admin.html')
@app.route('/admino')
def admino():
	if session['adminloggedin'] == True:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Orders""")
		alluser = cursor.fetchall()
		return render_template('/admino.html',alluser=alluser)
	else:
		flash('Logged in as admin to visit this page.')
		return render_template('/admin.html')
@app.route('/adminpr')
def adminpr():
	if session['adminloggedin'] == True:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM Product""")
		alluser = cursor.fetchall()
		return render_template('/adminpr.html',alluser=alluser)
	else:
		flash('Logged in as admin to visit this page.')
		return render_template('/admin.html')
@app.route('/adminu')
def adminu():
	if session['adminloggedin'] == True:
		cursor = db.cursor()
		cursor.execute("""SELECT * FROM User""")
		alluser = cursor.fetchall()
		return render_template('/adminu.html',alluser=alluser)
	else:
		flash('Logged in as admin to visit this page.')
		return render_template('/admin.html')
@app.route('/removeuser', methods=['POST','GET'])
def rmoveu():
	targetuid = request.form["removeuserbutton"]
	cursor = db.cursor()
	cursor.execute("""SELECT OrderID FROM Orders WHERE (UserID) = (%s)""",(targetuid))
	allorder = cursor.fetchall()
	for i in allorder:
		orderx = i[0]
		cursor =db.cursor()
		cursor.execute("""DELETE FROM Orders_Item WHERE (OrderID) = ( %s)""",(orderx))
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Orders WHERE (UserID) = (%s)""",(targetuid))
	cursor =db.cursor()
	cursor.execute("""DELETE FROM User WHERE (UserID) = (%s)""",(targetuid))
	db.commit()
	return redirect("http://localhost:8000/adminu")
@app.route('/removepr', methods=['POST','GET'])
def rmoveproduct():
	targetid = request.form["removepro"]
	cursor = db.cursor()
	cursor.execute("""DELETE FROM Orders_Item WHERE (ProductID) = (%s)""",(targetid))
	cursor =db.cursor()
	cursor.execute("""DELETE FROM Product WHERE (ProductID) = (%s)""",(targetid))
	db.commit()
	return redirect("http://localhost:8000/adminpr")
@app.route('/edituser', methods=['POST','GET'])
def editu():
	targetuid = request.form["edituserbutton"]
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM User WHERE UserID = (%s)""",(targetuid))
	pdata = cursor.fetchall()
	return render_template('adminuedit.html', pdata=pdata, targetuid=targetuid)
@app.route('/adminusereditsubmit', methods=['POST','GET'])
def aus():
	targetuid = request.form["tuid"]
	p_r_uname = request.form["html_r_uname"]
	p_r_pwd = request.form["html_r_pwd"]
	p_r_email = request.form["html_r_email"]
	p_r_fname = request.form["html_r_fname"]
	p_r_lname = request.form["html_r_lname"]
	p_r_phone = request.form["html_r_phone"]
	p_r_address = request.form["html_r_address"]
	p_r_birthdate = request.form["html_r_birthofdate"]
	cursor = db.cursor()
	cursor.execute("""UPDATE User SET UserName = (%s), UserPassword = (%s), Email = (%s), FirstName = (%s), LastName = (%s), Phone = (%s), Address = (%s), BirthDate = (%s) WHERE UserID = (%s)""",(p_r_uname, p_r_pwd, p_r_email, p_r_fname, p_r_lname, p_r_phone, p_r_address, p_r_birthdate, targetuid))
	db.commit()
	return redirect("http://localhost:8000/adminu")
@app.route('/editpr', methods=['POST','GET'])
def epr():
	targetpid = request.form["editpro"]
	cursor = db.cursor()
	cursor.execute("""SELECT * FROM Product WHERE (ProductID) = (%s) """,(targetpid))
	targetp = cursor.fetchall()
	return render_template('editproduct.html', targetp=targetp, targetpid=targetpid)
@app.route('/editproduct', methods=['POST','GET'])
def epro():
	targetpid = request.form["tpid"]
	p_name = request.form["html_pname"]
	p_price = request.form["html_pprice"]
	p_type = request.form["html_ptype"]
	p_image = request.form["html_pimage"]
	cursor = db.cursor()
	cursor.execute("""UPDATE Product SET ProductName = (%s), ProductPrice = (%s), ProductType = (%s), ProductImage = (%s) WHERE ProductID = (%s)""",(p_name, p_price, p_type, p_image, targetpid))
	db.commit()
	return redirect("http://localhost:8000/adminpr")
@app.route('/adminaddp')
def adminaddp():
	if session['adminloggedin'] == True:
		return render_template('/adminaddproduct.html')
	else:
		flash('Logged in as admin to visit this page.')
		return render_template('/admin.html')
@app.route('/addnewproductform', methods=['POST','GET'])
def aaaa():
	p1 = request.form["pname"]
	p2 = request.form["pprice"]
	p3 = request.form["ptype"]
	p4 = request.form["pimg"]
	cursor =db.cursor()
	cursor.execute("""INSERT INTO Product (ProductName, ProductPrice, ProductType, ProductImage) VALUES (%s, %s, %s, %s)""",(p1, p2, p3, p4))
	db.commit()
	return redirect("http://localhost:8000/adminpr")
@app.route('/adminlogout')
def adminlogout():
	session['adminloggedin'] = False
	flash('Logged out')
	return redirect("http://localhost:8000/admin")
if __name__ == '__main__':
	app.debug = True
	app.run(host="0.0.0.0", port = 8000)
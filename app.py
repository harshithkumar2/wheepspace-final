from flask import Flask,redirect,render_template,url_for, session, request, flash
import json
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
from passlib.hash import sha256_crypt
from flask_mail import Message,Mail

app = Flask(__name__)

with open("db.json","r") as f:
    data= json.load(f)["data"]

app.secret_key= os.urandom(24)
app.config['MYSQL_HOST'] = data["host"]
app.config['MYSQL_USER'] = data["db_user"]
app.config['MYSQL_PASSWORD'] = data["password"]
app.config['MYSQL_DB'] = data["db_name"]
app.config['MYSQL_PORT'] = data["port"]
#For mail system
app.config['MAIL_SERVER']= data["mail_host"]
app.config['MAIL_PORT'] = data["mail_port"]
app.config['MAIL_USERNAME'] = data["mail_username"]
app.config['MAIL_PASSWORD'] = data["mail_pass"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/userlayout')
def userlayout():
    return render_template('userlayout.html')

@app.route('/usercontact')
def usercontact():
    if "user" in session and session["user"] == True:
        return render_template('usercontact.html')
    else:
        return redirect(url_for('userlog'))
   

@app.route('/admreg')
def admreg():
    return render_template('admreg.html')

@app.route('/offline_user_book_admin')
def offline_user_book_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('offline_user_book_admin.html')
    else:
        return redirect(url_for('admlog'))

@app.route('/staffreg')
def staffreg():
    return render_template('staffreg.html')

@app.route('/staffreg_admin')
def staffreg_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('staffreg_admin.html')
    else:
        return redirect(url_for('admlog'))

@app.route('/dash_staff')
def dash_staff():
    if "staff" in session and session["staff"] == True:
        return render_template('dash_staff.html')
    else:
        return redirect(url_for('stafflog'))

@app.route('/dash_admin')
def dash_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('dash_admin.html')
    else:
        return redirect(url_for('admlog'))

@app.route('/dash_user')
def dash_user():
    if "user" in session and session["user"] == True:
        return render_template('dash_user.html')
    else:
        return redirect(url_for('userlog'))

@app.route('/search_results')
def search_results():
    return render_template('search_results.html')

@app.route('/search_admin_results')
def search_admin_results():
    if "admin" in session and session["admin"] == True:
        return render_template('search_admin_results.html')
    else:
        return redirect(url_for("admlog"))

@app.route('/search_results_admin')
def search_results_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('search_results_admin.html')
    else:
        return redirect(url_for("admlog"))


@app.route('/carreg')
def carreg():
    if "staff" in session and session["staff"]==True:
        return render_template('regcar.html')
    else:
        return redirect(url_for('stafflog'))

@app.route('/carreg_admin')
def carreg_admin():
    if "admin" in session and session["admin"]==True:
        return render_template('regcar_admin.html')
    else:
        return redirect(url_for('admlog'))

@app.route('/regular_user')
def regular():
    if "staff" in session and session["staff"] == True:
        return render_template('regular_user.html')
    else:
        return redirect(url_for('stafflog'))

@app.route('/regularadmin')
def regular_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('regular_user_admin.html')
    else:
        return redirect(url_for('admlog'))

@app.route('/usereg')
def usereg():
    return render_template('userreg.html')

@app.route('/usereg_admin')
def usereg_admin():
    if "admin" in session and session["admin"] == True:
        return render_template('userreg_admin.html')
    else:
        return redirect(url_for('admlog'))


@app.route('/onlinereg')
def onlinereg():
    return render_template('onlinebook.html')

@app.route('/admlog')
def admlog():
    return render_template('admlog.html')

@app.route("/onlines_list")
def onlines_list():
    if "staff" in session or "admin" in session:
        return render_template("onlines_list.html")
    else:
        return redirect(url_for("admlog"))

@app.route('/stafflog')
def stafflog():
    return render_template('stafflog.html')

@app.route('/userlog')
def userlog():
    return render_template('userlog.html')

@app.route('/admin_data', methods=['POST'])          #admin registration data
def admin_data():
    if request.method == 'POST':
        email = request.form['mail']
        name = request.form['nam']
        pas = request.form['pass']
        rpas = request.form['repass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select email from admin where email=%s",(email,))
        result = db.fetchone()
        if result is not None:
            flash("Email already taken", "error")
            db.close()
            return redirect(url_for('admreg'))
        else:
            if pas == rpas:
                hash_pas = sha256_crypt.hash(pas)
                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("INSERT INTO admin (email,name,password) VALUES (%s,%s,%s)",(email,name,hash_pas))
                mysql.connection.commit()
                db.close()
                return redirect(url_for("admlog"))
            else:
                flash("Password did not match", "error")
                return redirect(url_for('admreg'))
    else:
        flash("Some error occured try again","error")
        return redirect(url_for('admreg'))

@app.route('/staff_data',methods=['POST'])            #staff registration form data
def staff_data():
    if request.method == 'POST':
        name = request.form['nam']
        mail = request.form['mail']
        phone = request.form['phone']
        pas = request.form['pass']
        rpas = request.form['repass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select email from staff where email=%s",(mail,))
        result = db.fetchone()
        if result is not None:
            flash("Email already taken","error")
            db.close()
            return redirect(url_for("staffreg"))
        else:
            if pas == rpas:
                hash_pas = sha256_crypt.hash(pas)
                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("insert into staff (name,email,phone,password) values(%s,%s,%s,%s)",(name,mail,phone,hash_pas))
                mysql.connection.commit()
                db.close()
                return redirect(url_for("stafflog"))
            else:
                flash("Password did not match", "error")
                return redirect(url_for('staffreg'))
    else:
        flash("Some error occured try again","error")
        return redirect(url_for('staffreg'))

@app.route('/staff_data_admin',methods=['POST'])            #staff registration form data for admin dashboard
def staff_data_admin():
    if request.method == 'POST':
        name = request.form['nam']
        mail = request.form['mail']
        phone = request.form['phone']
        pas = request.form['pass']
        rpas = request.form['repass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select email from staff where email=%s",(mail,))
        result = db.fetchone()
        if result is not None:
            flash("Email already taken","error")
            db.close()
            return redirect(url_for("staffreg_admin"))
        else:
            if pas == rpas:
                hash_pas = sha256_crypt.hash(pas)
                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("insert into staff (name,email,phone,password) values(%s,%s,%s,%s)",(name,mail,phone,hash_pas))
                mysql.connection.commit()
                db.close()
                flash("Staff registration successfull","success")
                return redirect(url_for("dash_admin"))
            else:
                flash("Password did not match", "error")
                return redirect(url_for('staffreg_admin'))
    else:
        flash("Some error occured try again","error")
        return redirect(url_for('staffreg_admin'))

@app.route('/off_data',methods=['POST'])  # first time offline data registration for staff dashboard
def off_data():
    if request.method == 'POST':
        name = request.form['nam']
        mail = request.form['mail']
        phone = request.form['phone']
        vech_no = request.form['vech_no']
        vech_type = request.form['vech_type']
        lic_no = request.form['lic_no']
        duration = request.form['dur']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select license_no from offline_user where license_no=%s",(lic_no,))
        result = db.fetchone()
        #print(result)
        if result is not None:
            flash("License Number used","error")
            db.close()
            return redirect(url_for('carreg'))
        else:
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("select email from offline_user where email=%s", (mail,))
            result1 = db.fetchone()
            if result1 is not None:
                flash("Email already used","error")
                db.close()
                return redirect(url_for('carreg'))
            else:

                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("insert into offline_user values (%s,%s,%s,%s,%s,%s,%s)",(lic_no,name,mail,phone,vech_no,vech_type,duration))
                mysql.connection.commit()
                db.close()
                flash("Data inserted successfully","success")
                return redirect(url_for('carreg'))
    else:
        flash("some error occured","error")
        return redirect(url_for('stafflog'))

@app.route('/off_data_admin',methods=['POST'])  # first time offline data registration for admin dashboard
def off_data_admin():
    if request.method == 'POST':
        name = request.form['nam']
        mail = request.form['mail']
        phone = request.form['phone']
        vech_no = request.form['vech_no']
        vech_type = request.form['vech_type']
        lic_no = request.form['lic_no']
        duration = request.form['dur']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select license_no from offline_user where license_no=%s",(lic_no,))
        result = db.fetchone()
        #print(result)
        if result is not None:
            flash("License Number used","error")
            db.close()
            return redirect(url_for('carreg_admin'))
        else:
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("select email from offline_user where email=%s", (mail,))
            result1 = db.fetchone()
            if result1 is not None:
                flash("Email already used","error")
                db.close()
                return redirect(url_for('carreg_admin'))
            else:

                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("insert into offline_user values (%s,%s,%s,%s,%s,%s,%s)",(lic_no,name,mail,phone,vech_no,vech_type,duration))
                mysql.connection.commit()
                db.close()
                flash("Data inserted successfully","success")
                return redirect(url_for('dash_admin'))
    else:
        flash("some error occured","error")
        return redirect(url_for('admlog'))


@app.route('/off_extend_data', methods=["POST"])  #for multiple offline booking
def off_extend_user():
    if request.method == 'POST':
        lic_no = request.form['lic_no']
        date = request.form['dat']
        duration = request.form['dur']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #db.execute("select license_no from offline_user where license_no=%s",(lic_no,))
        #result = db.fetchone()
        try:
            db.execute("insert into offline_extended (license_no,dates,duration)values (%s,%s,%s)",(lic_no,date,duration))
            mysql.connection.commit()
            db.close()
            flash("Parking Booked Successfully","success")
            return redirect(url_for('dash_staff'))
        except MySQLdb._exceptions.IntegrityError:  #since license no is primary key in offline_user and foreign key in offline_extended table both license no should match
            flash("Insert a valid license number","error")
            return redirect(url_for('regular'))
    else:
        flash("Some error occured", "error")
        return redirect(url_for('stafflog'))

@app.route('/off_extend_data_admin', methods=["POST"])  #for multiple offline booking for admin dashboard
def off_extend_user_data():
    if request.method == 'POST':
        lic_no = request.form['lic_no']
        date = request.form['dat']
        duration = request.form['dur']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #db.execute("select license_no from offline_user where license_no=%s",(lic_no,))
        #result = db.fetchone()
        try:
            db.execute("insert into offline_extended (license_no,dates,duration)values (%s,%s,%s)",(lic_no,date,duration))
            mysql.connection.commit()
            db.close()
            flash("Parking Booked Successfully","success")
            return redirect(url_for('dash_admin'))
        except MySQLdb._exceptions.IntegrityError:  #since license no is primary key in offline_user and foreign key in offline_extended table both license no should match
            flash("Insert a valid license number","error")
            return redirect(url_for('regular_admin'))
    else:
        flash("Some error occured", "error")
        return redirect(url_for('admlog'))


@app.route('/admin_log', methods=['POST'])  #admin login
def admin_log():
    if request.method == 'POST':
        mail = request.form['mail']
        pas = request.form['pass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from admin where email=%s",(mail,))
        result = db.fetchone()
        db.close()
        if result is not None:
            dec_hash = sha256_crypt.verify(pas,result["password"])
            if dec_hash == True:
                session["email"] = result['email']
                session["name"] = result["name"]
                session["admin"] = True
                return redirect(url_for('dash_admin'))
            else:
                flash("Password incorrect","error")
                return redirect(url_for('admlog'))
        else:
            flash("Email not found", "error")
            return redirect(url_for('admlog'))

    else:
        flash("Some error occured try again", "error")
        return redirect(url_for('admlog'))

@app.route('/staff_log',methods=['POST']) #staff login
def staff_log():
    if request.method == 'POST':
        mail = request.form['mail']
        pas = request.form['pass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from staff where email=%s",(mail,))
        result=db.fetchone()
        db.close()
        if result is not None:
            pas_verify = sha256_crypt.verify(pas,result["password"])
            if pas_verify ==True:
                session["staff_mail"] = result["email"]
                session["staff_name"] = result["name"]
                session["staff_phone"] = result["phone"]
                session["staff"] = True
                flash(f" {result['name']}","success")
                return redirect(url_for('dash_staff'))
            else:
                flash("Password did not match","error")
                return redirect(url_for('stafflog'))
        else:
            flash("Email not found","error")
            return redirect(url_for('stafflog'))
    else:
        session.clear()
        flash("Some error occured","error")
        return redirect(url_for('stafflog'))


@app.route('/search_data', methods=['POST'])  #to search users license no and book slot for offline users staff
def search_data():
    if request.method == 'POST':
        query = request.form['search']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from offline_user where license_no=%s",(query,))
        result = db.fetchone()
        db.close()
        return render_template('search_results.html',data=result)


@app.route('/search_data_admin', methods=['POST'])  #to search users license no and book slot for offline users  for admin dashboard
def search_data_admin():
    if request.method == 'POST':
        query = request.form['search']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from offline_user where license_no=%s",(query,))
        result = db.fetchone()
        db.close()
        return render_template('search_results_admin.html',data=result)

@app.route('/book/<string:id>')  #books slot for offlne users for staff dashboard
def book(id):
    d = id
    db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    db.execute("select license_no from offline_user where license_no=%s",([d]))  #[d] bcz tuple is not iteratable so used list to traverse
    result = db.fetchone()
    db.close()
    if result is not None:
        return render_template('regular_user.html',data = result)
    else:
        return redirect(url_for('stafflog'))


@app.route('/book_admin/<string:id>')  #books slot for offlne users for admin dashboard
def book_admin(id):
    d = id
    db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    db.execute("select license_no from offline_user where license_no=%s",([d]))  #[d] bcz tuple is not iteratable so used list to traverse
    result = db.fetchone()
    db.close()
    if result is not None:
        return render_template('regular_user_admin.html',data = result)
    else:
        return redirect(url_for('admlog'))

@app.route("/online_data",methods=['POST'])          #online user registration for all users
def online_data():
    if request.method == 'POST':
        name = request.form['nam']
        email = request.form['mail']
        phone = request.form['phone']
        lic_no = request.form['lic_no']
        pas = request.form['pass']
        rpas = request.form['repass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select email from online_user where license_no=%s",(lic_no,))
        result = db.fetchone()
        db.close()
        if result is not None:
            flash("License number is already used","error")
            return redirect(url_for('usereg'))
        else:
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("select email from online_user where email=%s", (email,))
            result = db.fetchone()
            db.close()
            if result is not None:
                flash("Email is already used", "error")
                return redirect(url_for('usereg'))
            else:
                if pas == rpas:
                    hash_pas = sha256_crypt.hash(pas)
                    db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    db.execute("insert into online_user values(%s,%s,%s,%s,%s)",(lic_no,name,email,phone,hash_pas))
                    mysql.connection.commit()
                    db.close()
                    flash("Registration successfull","success")
                    return redirect(url_for('userlog'))
                else:
                    flash("Password did not match","error")
                    return redirect(url_for("usereg"))
    else:
        flash("Some error occured", "error")
        return redirect(url_for("usereg"))

@app.route("/online_data_admin",methods=['POST'])          #online user registration for admin dashboard
def online_data_admin():
    if request.method == 'POST':
        name = request.form['nam']
        email = request.form['mail']
        phone = request.form['phone']
        lic_no = request.form['lic_no']
        pas = request.form['pass']
        rpas = request.form['repass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select email from online_user where license_no=%s",(lic_no,))
        result = db.fetchone()
        db.close()
        if result is not None:
            flash("License number is already used","error")
            return redirect(url_for('usereg_admin'))
        else:
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("select email from online_user where email=%s", (email,))
            result = db.fetchone()
            db.close()
            if result is not None:
                flash("Email is already used", "error")
                return redirect(url_for('usereg_admin'))
            else:
                if pas == rpas:
                    hash_pas = sha256_crypt.hash(pas)
                    db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    db.execute("insert into online_user values(%s,%s,%s,%s,%s)",(lic_no,name,email,phone,hash_pas))
                    mysql.connection.commit()
                    db.close()
                    flash("User Registration successfull","success")
                    return redirect(url_for('dash_admin'))
                else:
                    flash("Password did not match","error")
                    return redirect(url_for("usereg_admin"))
    else:
        flash("Some error occured", "error")
        return redirect(url_for("usereg"))

@app.route("/user_log",methods=["POST"])      #online user login
def user_log():
    if request.method == 'POST':
        email = request.form['mail']
        pas = request.form['pass']
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_user where email=%s",(email,))
        result = db.fetchone()
        db.close()
        if result is not None:
            pas_verify = sha256_crypt.verify(pas, result["password"])
            if pas_verify == True:
                session["user_name"] = result["name"]
                session["user_mail"] = result['email']
                session["user"] = True
                session["lic_no"] = result["license_no"]
                session["phone"] = result["phone"]
                flash(f"{result['name']}","success")
                return redirect(url_for("dash_user"))
            else:
                flash("Password did not match", "error")
                return redirect(url_for("userlog"))
        else:
            flash("Email not found", "error")
            return redirect(url_for("userlog"))
    else:
        flash("Some error occured", "error")
        return redirect(url_for("userlog"))

@app.route("/booking/<id>") # online user booking
def booking(id):
    if "user" in session and session["user"] == True:
        data = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select license_no from online_user where license_no=%s",(data,))
        result = db.fetchone()
        db.close()
        if result is not None:
            return render_template("onlinebook.html", dat = result["license_no"])
        else:
            flash("Some error occured try again","error")        #if he uses to enter his own or other lic no in url provides error
            session.clear()
            return redirect(url_for('userlog'))

    else:
        session.clear()
        flash("Some error occured try again", "error")
        return redirect(url_for('userlog'))


@app.route("/confirm_booking",methods=["POST"])  # inserting vehicle details to db of online user after log in
def confirm_booking():
    if "user" in session and session["user"] == True:
        if request.method == 'POST':
            vech_no = request.form["vech_no"]
            vech_type = request.form["vech_type"]
            lic_no = request.form["lic_no"]
            duration = request.form["dur"]
            date = request.form["dat"]
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("insert into online_booking (license_no,vech_no,vech_type,duration,dates) values (%s,%s,%s,%s,%s)",(lic_no,vech_no,vech_type,duration,date))
            mysql.connection.commit()
            db.close()
            flash("Parking booked successfully","success")
            return redirect(url_for("dash_user"))
        else:
            session.clear()
            flash("some error occured", "error")
            return redirect(url_for("userlog"))
    else:
        session.clear()
        flash("some error occured","error")
        return redirect(url_for("userlog"))

@app.route("/online_list",methods=["POST","GET"])  #online booking list for admin  datewise
def online_list():
    if "admin" in session and session["admin"] ==True:
        db=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_booking order by dates desc")
        result = db.fetchall()
        db.close()
        if result is not None:
            return render_template("onlines_list.html", data=result)
    else:
        return redirect(url_for("admlog"))

@app.route("/online_list_staffs",methods=["POST","GET"])  #online booking list for staff  datewise
def online_list_staffs():
    if "staff" in session and session["staff"] ==True:
        db=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_booking order by dates desc")
        result = db.fetchall()
        db.close()
        if result is not None:
            return render_template("online_list_staff.html", data=result)
    else:
        return redirect(url_for("stafflog"))


@app.route("/search_admin_data",methods=["POST"])   #search bar data for admin
def search_admin_data():
    if "admin" in session and session["admin"] == True:
        if request.method == 'POST':
            query = request.form["search"]
            db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            db.execute("select * from online_user where license_no=%s",(query,))
            result = db.fetchone()
            db.close()
            if result is not None:
                return render_template("search_admin_results.html",data=result)
            else:
                db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                db.execute("select * from offline_user where license_no=%s", (query,))
                result = db.fetchone()
                db.close()
                if result is not None:
                    return render_template("search_admin_results.html", data=result)
                else:
                    db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    db.execute("select * from staff where name=%s", (query,))
                    result = db.fetchone()
                    db.close()
                    if result is not None:
                        return render_template("search_admin_results.html", data=result)
                    else:
                        return redirect(url_for("search_admin_results"))
    else:
        return redirect(url_for("admlog"))

@app.route("/online_list_edit")  #display all online users to the admin
def online_list_edit():
    if "admin" in session and session["admin"]==True:
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_user")
        result = db.fetchall()
        db.close()
        return render_template("online_list_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))

@app.route("/edit/<id>")  #display data of selected user for editing admin dashboard
def online_edit(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_user where license_no=%s",(lic,))
        result = db.fetchone()
        db.close()
        return render_template("online_data_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))
@app.route("/online_user_data_update/<id>",methods=["POST"]) #update edited online user data
def online_user_data_update(id):
    if "admin" in session and session["admin"]==True:
        lic = id
        name = request.form["nam"]
        mail = request.form["mail"]
        phone = request.form["phone"]
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("update online_user set name=%s,email=%s,phone=%s where license_no=%s", (name,mail,phone,lic))
        mysql.connection.commit()
        db.close()
        flash("Online User data updated Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))


@app.route("/delete/<id>")  #delete online user records from db admin dashboard
def online_delete(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("delete from online_user where license_no=%s",(lic,))
        mysql.connection.commit()
        db.close()
        flash("User deleted Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))

@app.route("/offline_list_edit")  #display all offline users to the admin (offline users)
def offline_list_edit():
    if "admin" in session and session["admin"]==True:
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from offline_user")
        result = db.fetchall()
        db.close()
        return render_template("offline_list_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))

@app.route("/edit_offline/<id>")  #display data of selected user for editing admin dashboard(offline users)
def offline_edit(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from offline_user where license_no=%s",(lic,))
        result = db.fetchone()
        db.close()
        return render_template("offline_data_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))
@app.route("/offline_user_data_update/<id>",methods=["POST"]) #update edited offline user data
def offline_user_data_update(id):
    if "admin" in session and session["admin"]==True:
        lic = id
        name = request.form["nam"]
        mail = request.form["mail"]
        phone = request.form["phone"]
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("update offline_user set name=%s,email=%s,phone=%s where license_no=%s", (name,mail,phone,lic))
        mysql.connection.commit()
        db.close()
        flash("Offline User data updated Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))


@app.route("/delete_offline/<id>")  #delete offline user records from db admin dashboard
def offline_delete(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("delete from offline_user where license_no=%s",(lic,))
        mysql.connection.commit()
        db.close()
        flash("User deleted Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))

@app.route("/staff_list_edit")  #display all staff users to the admin (staff users)
def staff_list_edit():
    if "admin" in session and session["admin"]==True:
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from staff")
        result = db.fetchall()
        db.close()
        return render_template("staff_list_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))

@app.route("/edit_staff/<int:id>")  #display data of staff  for editing admin dashboard
def staff_edit(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from staff where staff_id=%s",(lic,))
        result = db.fetchone()
        db.close()
        return render_template("staff_data_edit.html",data=result)
    else:
        return redirect(url_for("admlog"))
@app.route("/staff_user_data_update/<int:id>",methods=["POST"]) #update edited staff user data
def staff_user_data_update(id):
    if "admin" in session and session["admin"]==True:
        lic = id
        name = request.form["nam"]
        mail = request.form["mail"]
        phone = request.form["phone"]
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("update staff set name=%s,email=%s,phone=%s where staff_id=%s", (name,mail,phone,lic))
        mysql.connection.commit()
        db.close()
        flash("Staff data updated Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))


@app.route("/delete_staff/<int:id>")  #delete staff user records from db admin dashboard
def staff_delete(id):
    if "admin" in session and session["admin"] ==True:
        lic = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("delete from staff where staff_id=%s",(lic,))
        mysql.connection.commit()
        db.close()
        flash("Staff deleted Successfully","success")
        return redirect(url_for("dash_admin"))
    else:
        return redirect(url_for("admlog"))

@app.route('/all_mail',methods=["POST"])  #general query help line
def all_mail():
    if request.method == 'POST':
        data = request.form["mail"]
        msg1 = request.form["msg"]
        msg = Message("[GENERAL] Queries",sender=data,recipients=["harshithkumar40@gmail.com"])
        msg.body = msg1
        mail.send(msg)
        return redirect(url_for("index"))

@app.route('/user_mail',methods=["POST"]) #query related booking
def user_mail():
    if request.method == 'POST':
        data = request.form["mail"]
        msg1 = request.form["msg"]
        msg = Message("[BOOKING] related Query",sender=data,recipients=["harshithkumar40@gmail.com"])
        msg.body = msg1
        mail.send(msg)
        return redirect(url_for("dash_user"))


@app.route('/history/<id>') #history to track of users booking with date and vehicles
def history(id):
    if "user" in session and session["user"] == True:
        data = id
        db = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        db.execute("select * from online_booking where license_no=%s",(data,))
        result = db.fetchall()
        return render_template("bookhistory.html",data=result)
    else:
        return redirect(url_for("userlog"))

@app.route('/logout_admin')
def logout_admin():
    session.clear()
    return redirect(url_for('index'))

@app.route('/logout_staff')
def logout_staff():
    session.clear()
    return redirect(url_for('index'))

@app.route('/logout_user')
def logout_user():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
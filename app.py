from flask import Flask, render_template, request,flash, redirect, url_for
from user import UserOperation
from encryption import Encryption
from validate import myvalidate
from myemail import Email
from myrandom import randomnumber

app=Flask(__name__)  
app.secret_key= "df5ge4twfwef32f2"  #attribute

validobj = myvalidate()  #validation object
emailobj = Email(app)  #Email Object

@app.route('/')        
def index():             
    return render_template('index.html')

@app.route('/user_signup', methods=['GET','POST'])        
def user_signup():   
    if request.method=='GET':
        return render_template('user_signup.html')
    else:
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        user_name=request.form['user_name']
        password=request.form['password']

        #------------------validation------------#
        frm=[fname,lname,email,user_name,password]
        if(not validobj.required(frm)):
            flash("field cannot be empty")
            return redirect(url_for("user_signup"))

        #---------password Encryption------------#
        e = Encryption()
        e.convert(password)
        password = e.convert(password)
        #------------------------------------------#
        userobj = UserOperation()  # obj
        r=userobj.user_check(user_name)
        rc=userobj.user_check(email)

        if(r==0 and rc == 0):
            otp = randomnumber()
            subject = "Cloud Beats Email Verification"
            msg="Hi "+fname+"\nYour Email OTP is "+str(otp)+"\nThank You\nCloud Beats"
            emailobj.compose_mail(subject,email,msg)

            userobj.user_insert(fname,lname,email,user_name,password)
            # return "success"
            flash("Succesfully Registered.. Login Now")
            return redirect(url_for("user_login"))
        else:
            if(rc!=0):
                flash("Email name already exists")
            elif(rc!=0):
                flash("User name already exists")
            return redirect(url_for("user_signup"))

@app.route("/user_login")
def user_login():
    return render_template("user_login.html")

if __name__ == '__main__':             
    app.run(debug = True)
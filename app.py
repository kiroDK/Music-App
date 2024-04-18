from flask import Flask, render_template, request,flash, redirect, url_for, session
from user import UserOperation
from creator import CreatorOperation
from encryption import Encryption
from validate import myvalidate
from myemail import Email
from myrandom import randomnumber
from datetime import datetime
from audio import voice

app=Flask(__name__)  
app.secret_key= "df5ge4twfwef32f2"  #attribute

userobj = UserOperation()  # user obj
validobj = myvalidate()  #validation object
emailobj = Email(app)  #Email Object
creatorobj = CreatorOperation() #creator object

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
        password = e.convert(password)
        #------------------------------------------#
        r=userobj.user_check(user_name)
        rc=userobj.user_check(email)

        if(r==0 and rc == 0):
            global otp
            otp = randomnumber()
            subject = "Cloud Beats Email Verification"
            msg="Hi "+fname+"\nYour Email OTP is "+str(otp)+"\nThank You\nCloud Beats"
            emailobj.compose_mail(subject,email,msg)

            userobj.user_insert(fname,lname,email,user_name,password)

            # return "success"
            # flash("Succesfully Registered.. Login Now")
            flash("OTP sent to registered Email")
            # return redirect(url_for("user_login"))
            return redirect(url_for("otpverify",email=email))
        else:
            if(rc!=0):
                flash("Email name already exists")
            elif(rc!=0):
                flash("User name already exists")
            return redirect(url_for("user_signup"))


@app.route("/otpverify",methods=["GET", "POST"])
def otpverify():
    if("otp" in globals()):
        if(request.method == "GET"):
            email = request.args.get('email')
            return render_template("otpverify.html",email=email)
        else:
            n1=request.form['n1']
            n2=request.form['n2']
            n3=request.form['n3']
            n4=request.form['n4'] 
            otpinput=n1+n2+n3+n4
            if(str(otp)==otpinput):
                flash("Successfully registered....Login Now")
                return redirect(url_for('user_login'))
            else:
                email = request.form['email']
                userobj.user_delete(email)
                flash("Email verification failed...Register Again")
                return redirect(url_for('user_signup'))
    else:
        return "cannot access this page"

@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if(request.method=='GET'):
        return render_template("user_login.html")
    else:
        user_name=request.form['user_name']
        password=request.form['password']

        # PASSWORD ENCRYPTION *****************
        e=Encryption()
        password=e.convert(password)

        # ***********************
        r=userobj.user_login(user_name,password)
        if(r==0):
            flash("invalid credentials!!")
            return redirect(url_for("user_login"))
        else:
            # return "welcome "+ session["user_fname"]
            return render_template("user_dashboard.html")


@app.route("/user_dashboard",methods=['GET','POST'])
def user_dashboard():
    if('user_name' in session):
        if(request.method=='GET'):
            return render_template("user_dashboard.html")
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))

@app.route("/user_layout")
def user_layout():
    return render_template("user_layout.html")


@app.route("/user_logout",methods=['GET','POST']) #session destroy and then logout ho jayega
def user_logout():
    if('user_name' in session):
        if(request.method=='GET'):
            session.clear()  # destroy all users session
            flash("Logged out successfully")
            return redirect(url_for("user_login"))
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))

@app.route("/user_profile",methods=['GET','POST']) #session destroy and then logout ho jayega
def user_profile():
    if('user_name' in session):
        if(request.method=='GET'):
            record=userobj.user_profile()
            return render_template("user_profile.html",record=record)
        else:
            fname = request.form['fname']
            lname = request.form['lname']
            userobj.user_update(fname,lname)
            return redirect(url_for("user_profile")) #url me get method activate hota hai

    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("user_login"))


@app.route('/user_delete', methods=['POST'])
def user_delete():
    if 'user_name' in session:
        userobj.user_account_delete(session['user_name'])
        session.pop('user_name', None)
        flash("Account deleted successfully")
        return redirect(url_for('user_login'))
    else:
        return "You must be logged in to delete your account"



@app.route('/user_change_password', methods=['GET','POST'])
def user_change_password():
    if 'user_name' in session:
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']

            # Validate form fields
            frm = [old_password, new_password]
            if not validobj.required(frm):
                flash("Field can't be empty!!")
                return redirect(url_for('user_change_password'))

            # Encrypt passwords
            e = Encryption()
            old_password = e.convert(old_password)
            new_password = e.convert(new_password)

            # Check if old password is correct
            if userobj.user_login(session['user_name'], old_password) == 0:
                flash("Your Old Password is Not Valid!!")
                return redirect(url_for('user_change_password'))

            # Change the password
            userobj.change_password(session['user_name'], new_password)
            flash("Your Password is changed Successfully!!")
            return redirect(url_for('user_profile'))

        else:  # GET request
            return render_template('user_change_password.html')

    else:
        flash('You must be logged in to change your password')
        return redirect(url_for('user_login'))




@app.route('/user_blog_listen', methods=['GET','POST'])
def user_blog_listen():
    if 'user_name' in session:
        if(request.method == 'GET'):
            userobj.user_blog_listen()
            record = userobj.user_blog_listen()
            return render_template('user_blog_listen.html',record=record)
    else:
        return "You must be logged in to delete your account"


@app.route('/user_blog_view', methods=['GET','POST'])
def user_blog_view():
    if('user_name' in session):
        if(request.method=='POST'):
            audio_id=request.args.get('audio_id')
            record=userobj.user_blog_view(audio)
            return render_template("user_blog_view.html",record=record)
    else:
        flash("You cannot access this page ... please login in to continue")
        return redirect(url_for('user_login'))


@app.route('/user_blog_search', methods=['GET','POST'])
def user_blog_search():
    if 'user_name' in session:
        if(request.method == 'POST'):
            title = request.form['title']
            record = userobj.user_blog_search(title)
            return render_template('user_blog_listen.html',record=record,title=title)
    else:
       flash( "You must be logged in to delete your account")
       return redirect(url_for('user_login'))


@app.route('/user_song_listen', methods=['GET','POST'])
def user_song_listen():
    if 'user_name' in session:
        if(request.method == 'GET'):
            userobj.user_song_listen()
            record = userobj.user_song_listen()
            return render_template('user_song_listen.html',record=record)
    else:
        return "You must be logged in to delete your account"
        

@app.route('/user_song_search', methods=['GET','POST'])
def user_song_search():
    if 'user_name' in session:
        if(request.method == 'POST'):
            title = request.form['title']
            record = userobj.user_song_search(title)
            return render_template('user_song_listen.html',record=record,title=title)
    else:
       flash( "You must be logged in to delete your account")
       return redirect(url_for('user_login'))


#------------------For Testing---------------------------#
@app.route("/test")
def testing():
    return render_template("main_layout.html")

@app.route("/test1")
def testing1():
    return render_template("user_layout.html")

@app.route("/test2")
def testing2():
    return render_template("change_password_page.html")




#----------------------------------------------------------------
#-----------------Creater Module --------------------------------
#----------------------------------------------------------------

@app.route('/creator_signup',methods=['GET','POST'])
def creator_user_signup():
    if request.method == 'GET':
        return render_template('creator_signup.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        creator_name = request.form['creator_name']
        password = request.form['password']
        photo = request.files['photo']
        #----Form Validation-----
        frm = [fname,lname,email,creator_name,password]
        if(not validobj.required(frm)):
            flash("Field cannot be Empty!")
            return redirect(url_for('creator_signup'))
        #----Photo Upload--------------
        p = photo.filename
        if(p==''):
            flash("Photo must be uploaded!!")
            return redirect(url_for('creator_signup'))
        
        d = datetime.now()
        t = int(round(d.timestamp()))
        path = str(t)+'.'+p.split('.')[-1]

        photo.save("static/creator/"+path)

        #----password encryption-------
        e = Encryption()
        password = e.convert(password)
        #------------------------------    
        r = creatorobj.creator_check(creator_name)  

        if(r==1):
            flash("Creator name already Exists!")
            return redirect(url_for('creator_signup'))

        creatorobj.creator_insert(fname,lname,email,creator_name,password,path)

        flash("Congrats...Welcome Dear Creator!!")
        return redirect(url_for('creator_login'))

@app.route('/creator_login',methods=['GET','POST'])
def creator_login():
    if(request.method=='GET'):
        return render_template('creator_login.html')
    else:
        creator_name = request.form['creator_name']
        password = request.form['password']
        #------Password Encryption-------
        e = Encryption()
        password = e.convert(password)

        #--------------------------------
        r = creatorobj.creator_login(creator_name,password)
        if(r==0):
            flash("invalid creator name and password!!")
            return redirect(url_for('creator_login'))
        else:
            #return "Welcome "+session['user_fname']
            #return render_template('user_dashboard')
            return redirect(url_for('creator_dashboard'))


@app.route("/creator_dashboard",methods=['GET','POST'])
def creator_dashboard():
    if('creator_name' in session):
        if(request.method=='GET'):
            return render_template("creator_dashboard.html")
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("creator_login"))

@app.route("/creator_logout",methods=['GET','POST']) #session destroy and then logout ho jayega
def creator_logout():
    if('creator_name' in session):
        if(request.method=='GET'):
            session.clear()  # destroy all creators session
            flash("Logged out successfully")
            return redirect(url_for("creator_login"))
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("creator_login"))


@app.route("/creator_profile",methods=['GET','POST']) #session destroy and then logout ho jayega
def creator_profile():
    if('creator_id' in session):
        if(request.method=='GET'):
            record=creatorobj.creator_profile()
            return render_template("creator_profile.html",record=record)
        else:
            fname = request.form['fname']
            lname = request.form['lname']
            creatorobj.creator_update(fname,lname)
            return redirect(url_for("creator_profile")) #url me get method activate hota hai


@app.route('/creator_change_password', methods=['GET','POST'])
def creator_change_password():
    if 'creator_name' in session:
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']

            # Validate form fields
            frm = [old_password, new_password]
            if not validobj.required(frm):
                flash("Field can't be empty!!")
                return redirect(url_for('creator_change_password'))

            # Encrypt passwords
            e = Encryption()
            old_password = e.convert(old_password)
            new_password = e.convert(new_password)

            # Check if old password is correct
            if creatorobj.creator_login(session['creator_name'], old_password) == 0:
                flash("Your Old Password is Not Valid!!")
                return redirect(url_for('creator_change_password'))

            # Change the password
            creatorobj.change_password(session['creator_name'], new_password)
            flash("Your Password is changed Successfully!!")
            return redirect(url_for('creator_profile'))

        else:  # GET request
            return render_template('creator_change_password.html')

    else:
        flash('You must be logged in to change your password')
        return redirect(url_for('creator_login'))


@app.route('/creator_delete', methods=['POST'])
def creator_delete():
    if 'creator_name' in session:
        creatorobj.creator_account_delete(session['creator_name'])
        session.pop('creator_name', None)
        flash("Account deleted successfully")
        return redirect(url_for('creator_login'))
    else:
        return "You must be logged in to delete your account"



@app.route("/creator_audioblog",methods=['GET','POST'])
def creator_audioblog():
    if('creator_id' in session):
        if(request.method=='GET'):
            lang=request.args.get('lang')
            category=request.args.get('category')
            title = request.args.get('title')
            # print("GET Request - Category:", category)
            # print("GET Request - Title:", title)

            try:
                audiolist = voice(lang)
                d = datetime.now()
                t = int(round(d.timestamp()))
                audio = str(t)+'.wav'
                with open('static/audioblog/'+audio,'wb') as f:
                    f.write(audiolist[1].get_wav_data())
            
                creatorobj.creator_audioblog(audio,audiolist[0],category,title)
                flash("Your audio blog recorded successfully!!")
                return redirect(url_for("creator_audio"))
            except Exception as e :
                flash (str(e))
                # flash("Voice is not recognized")
                return redirect(url_for("creator_audio"))

        else:
            category = request.form['category']
            audio = request.files['audio']
            title= request.form['title']
            p = audio.filename
            if(p==''):
                flash("audio must be uploaded!!")
                return redirect(url_for('creator_audio'))
            
            d = datetime.now()
            t = int(round(d.timestamp()))
            path = str(t)+'.'+p.split('.')[-1]
            audio.save("static/audioblog/"+path)
            creatorobj.creator_audio_upload(path,category,title)

            flash("Your audioblog is uploaded successfully!!")
            return redirect(url_for("creator_audio"))

    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("creator_login"))


@app.route("/creator_audio",methods=['GET','POST'])
def creator_audio():
    if('creator_name' in session):
        if(request.method=='GET'):
            return render_template("creator_audio.html")
    else:
        flash("You cannot access this page..please login")
        return redirect(url_for("creator_login"))



@app.route("/creator_recorded",methods=['GET','POST'])
def creator_recorded():
    if('creator_id' in session):
        if(request.method=='GET'):
            record = creatorobj.get_creator_recorded(session['creator_id'])
        return render_template("creator_recorded.html",record=record)
    else:
        flash("Please Login to Access the Page...Please login")
        return redirect(url_for("creator_login"))


@app.route("/creator_uploaded",methods=['GET','POST'])
def creator_uploaded():
    if('creator_id' in session):
        record = creatorobj.get_creator_uploaded(session['creator_id'])
        return render_template("creator_uploaded.html",record=record)
    else:
        flash("Please Login to Access the Page...Please login")
        return redirect(url_for("creator_login"))




@app.route("/creator_delete_audioblog",methods=['GET','POST'])
def creator_delete_audioblog():
    if('creator_id' in session):
        if(request.method=='GET'):
            audioblog_id=int(request.args.get('audioblog_id'))
            creatorobj.creator_delete_audioblog(audioblog_id)
            flash("Audio blog deleted Successfully")
            return redirect(url_for("creator_recorded"))
    else:
        flash("Please Login to Access the Page...Please login")
        return redirect(url_for("creator_login"))


@app.route("/creator_edit_audio",methods=['GET','POST'])
def creator_edit_audio():
    if('creator_id' in session):
        if(request.method=='GET'):
            audio_id=request.args.get('audio_id')
            record=creatorobj.creator_edit_audio(audio_id)
            return render_template("creator_edit_audio.html",record=record)
        else:
            audio_id=request.args.get('audio_id')
            category = request.form['category']
            creatorobj.get_audio_update(audio_id,category)
            flash("Category changed successfully")
            return redirect(url_for("creator_uploaded"))
    else:
        flash("Please Login to Access the Page...Please login")
        return redirect(url_for("creator_login"))






@app.errorhandler(404)
def not_found(e):
    return "NOT FOUND"

if __name__ == '__main__':             
    app.run(debug = True)   
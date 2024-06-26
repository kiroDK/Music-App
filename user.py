import mysql.connector
from flask import session
from datetime import datetime

class UserOperation:
    def connection(self):  #to connect the user
        con = mysql.connector.connect(host="localhost", port="3306",user="root",password="root",database="cloud_beats")
        return con

    def user_insert(self,fname,lname,email,user_name,password):   #for inserting data into table
        db=self.connection()
        mycursor = db.cursor()

        sq = "insert into user (fname,lname,email,user_name,password) values (%s,%s,%s,%s,%s)"

        record=[fname,lname,email,user_name,password]
        mycursor.execute(sq,record)
        db.commit()    # insert, delete, display
        mycursor.close() # close
        db.close() # close
        return

    def user_check(self,user_name):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select user_name from user where user_name = %s"

        record =[user_name]
        mycursor.execute(sq,record)
        mycursor.fetchall()
        r = mycursor.rowcount
        if(r==0):
            return 0
        else:
            return 1

    #Email Wala khud se kro
    def email_check(self,email):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select email from user where email = %s"

        record =[email]
        mycursor.execute(sq,record)
        mycursor.fetchall()
        rc = mycursor.rowcount
        if(rc==0):
            return 0
        else:
            return 1

    def user_delete(self,email):   #for deleting data into table
        db=self.connection()
        mycursor = db.cursor()

        sq = "delete from user where email = %s"

        record=[email]
        mycursor.execute(sq,record)
        db.commit()    # insert, delete, display
        mycursor.close() # close
        db.close() # close
        return

    def user_login(self,user_name,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname,user_name from user where user_name=%s and password=%s"
        record=[user_name,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        rc=mycursor.rowcount

        mycursor.close()
        db.close()

        if(rc==0):
            return 0
        else:
            session["user_fname"]=row[0][0]
            session["user_name"]=row[0][1]
            return 1

    def user_profile(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname, lname, user_name, email from user where user_name=%s"
        record=[session['user_name']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_update(self,fname,lname):
        db=self.connection()
        mycursor=db.cursor()
        sq="update user set fname=%s, lname=%s where user_name=%s"
        record=[fname,lname,session['user_name']]    #username change hone pe session destroy ho jana chahiye
        mycursor.execute(sq,record)
        db.commit()
        session['user_fname']=fname
        mycursor.close()
        db.close()


    def user_account_delete(self, user_name):   #for deleting user account from the table
        db=self.connection()
        mycursor = db.cursor()

        sq = "delete from user where user_name = %s"

        record=[user_name]
        mycursor.execute(sq,record)
        db.commit()    # commit the transaction
        mycursor.close() # close the cursor
        db.close() # close the connection
        return

    def change_password(self, user_name, new_password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update user set password=%s where user_name=%s"
        record = [new_password, user_name]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()


    def user_blog_listen(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audioblog_id, title, category, audio, audiotext from audioblog"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_blog_search(self,title):
        db = self.connection()
        mycursor = db.cursor()
        # sq = "select creator_id,audio, title, audiotext, category from audioblog where title like %s"
        sq = "select audioblog_id, title, category, audio, audiotext from audioblog where title like %s"
        record = ["%" + title + "%"]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row


    def user_blog_view(self,audioblog_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audioblog_id, title, category, audio, audiotext from audioblog where audioblog_id = %s"
        record = [audioblog_id]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_song_view(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audio_upload_id, title, category, audio from audio_upload where audio_upload_id = %s"
        record = [audio_id]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row


    def user_song_listen(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audio_upload_id,title, audio,category from audio_upload"
        mycursor.execute(sq)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row


    def user_song_search(self,title):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select title, audio,category from audio_upload where title like %s"
        record = ["%" + title + "%"]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    
    def user_playlist_collection(self):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select playlist_name from playlist_collection where user_name = %s"
        record = [session['user_name']]
        mycursor.execute(sq,record)
        row = mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def user_add_playlist_collection(self,playlist_name):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into playlist_collection (user_name,playlist_name) values(%s,%s)"
        record = [session['user_name'],playlist_name]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return


    def user_add_playlist(self,playlist_name,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into playlist (username, playlist_name, audio_id) values (%s, %s, %s)"
        record = [session['user_name'],playlist_name,audio_id]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    
    def get_blog_review(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select comment,star,created_at,user_name from review where audio_id=%s"
        record=[audio_id]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def get_song_review(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select comment,star,created_at,user_name from review where audio_id=%s"
        record=[audio_id]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row


    def submit_blog_review(self,audio_id,comment,star):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into review(audio_id,user_name,comment,star,created_at)values(%s,%s,%s,%s,%s)"
        record=[audio_id,session['user_name'],comment,star,datetime.now()]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def submit_song_review(self,audio_id,comment,star):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into review(audio_id,user_name,comment,star,created_at)values(%s,%s,%s,%s,%s)"
        record=[audio_id,session['user_name'],comment,star,datetime.now()]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

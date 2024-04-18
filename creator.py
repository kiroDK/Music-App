import mysql.connector
from flask import session
from datetime import datetime 

class CreatorOperation:
    def connection(self):  #to connect the creator
        con = mysql.connector.connect(host="localhost", port="3306",user="root",password="root",database="cloud_beats")
        return con

    def creator_insert(self,fname,lname,email,creator_name,password,photo):   #for inserting data into table
        db=self.connection()
        mycursor = db.cursor()

        sq = "insert into creator (fname,lname,email,creator_name,password,photo) values (%s,%s,%s,%s,%s,%s)"

        record=[fname,lname,email,creator_name,password,photo]
        mycursor.execute(sq,record)
        db.commit()    # insert, delete, display
        mycursor.close() # close
        db.close() # close
        return

    def creator_check(self,creator_name):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select creator_name from creator where creator_name = %s"

        record =[creator_name]
        mycursor.execute(sq,record)
        mycursor.fetchall()
        r = mycursor.rowcount
        if(r==0):
            return 0
        else:
            return 1

    def creator_login(self,creator_name,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select creator_id,creator_name from creator where creator_name=%s and password=%s"
        record=[creator_name,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        rc=mycursor.rowcount

        mycursor.close()
        db.close()

        if(rc==0):
            return 0
        else:
            session["creator_id"]=row[0][0]
            session["creator_name"]=row[0][1]
            return 1

    def creator_profile(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname, lname, creator_name, email, photo, creator_id from creator where creator_name=%s"
        record=[session['creator_name']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def creator_update(self,fname,lname):
        db=self.connection()
        mycursor=db.cursor()
        sq="update creator set fname=%s, lname=%s where creator_name=%s"
        record=[fname,lname,session['creator_name']]    #creatorname change hone pe session destroy ho jana chahiye
        mycursor.execute(sq,record)
        db.commit()
        session['creator_fname']=fname
        mycursor.close()
        db.close()

    def change_password(self, creator_name, new_password):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update creator set password=%s where creator_name=%s"
        record = [new_password, creator_name]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()

    def creator_account_delete(self, creator_name):   #for deleting creator account from the table
        db=self.connection()
        mycursor = db.cursor()

        sq = "delete from creator where creator_name = %s"

        record=[creator_name]
        mycursor.execute(sq,record)
        db.commit()    # commit the transaction
        mycursor.close() # close the cursor
        db.close() # close the connection
        return


    def creator_audioblog(self,audio,audiotext,category,title):   #for inserting data into table
            db=self.connection()
            mycursor = db.cursor()
            sq = "insert into audioblog (creator_id,audio,audiotext,category,title,created_at) values (%s,%s,%s,%s,%s,%s)"
            created_at = datetime.now()
            record=[session['creator_id'],audio,audiotext,category,title,created_at]
            mycursor.execute(sq,record)
            db.commit()    # insert, delete, display
            mycursor.close() # close
            db.close() # close
            return

    def creator_audio_upload(self,path,category,title):
        db = self.connection()
        mycursor = db.cursor()
        sq = "insert into audio_upload (creator_id,audio,category,title,created_at) values (%s,%s,%s,%s,%s)"
        created_at = datetime.now()
        record=[session['creator_id'],path,category,title,created_at]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return


    def get_creator_recorded(self,creator_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audioblog_id, title , audio, audiotext,category, created_at from audioblog where creator_id = (%s)"
        record = [session['creator_id']]
        mycursor.execute(sq,record)
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows

    def get_creator_uploaded(self,creator_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select audio_upload_id,title, audio, category, created_at from audio_upload where creator_id = (%s)"
        record = [session['creator_id']]
        mycursor.execute(sq,record)
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows


    def creator_delete_audioblog(self, audioblog_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "DELETE FROM audioblog WHERE audioblog_id = (%s)"
        record = [audioblog_id]
        mycursor.execute(sq, record)
        db.commit()
        mycursor.close()
        db.close()
        return


    def creator_edit_audio(self,audio_id):
        db = self.connection()
        mycursor = db.cursor()
        sq = "select category from audio_upload where audio_upload_id = (%s)"
        record = [audio_id]
        mycursor.execute(sq,record)
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows


    def get_audio_update(self,audio_id,category):
        db = self.connection()
        mycursor = db.cursor()
        sq = "update audio_upload set category= %s where audio_upload_id = (%s)"
        record = [category,audio_id]
        mycursor.execute(sq,record)
        db.commit()
        rows = mycursor.fetchall()
        mycursor.close()
        db.close()
        return rows



import mysql.connector
from flask import session

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

    # #Email Wala khud se kro
    # def email_check(self,email):
    #     db = self.connection()
    #     mycursor = db.cursor()
    #     sq = "select email from user where email = %s"

    #     record =[email]
    #     mycursor.execute(sq,record)
    #     mycursor.fetchall()
    #     rc = mycursor.rowcount
    #     if(rc==0):
    #         return 0
    #     else:
    #         return 1

    # def user_delete(self,email):   #for deleting data into table
    #     db=self.connection()
    #     mycursor = db.cursor()

    #     sq = "delete from user where email = %s"

    #     record=[email]
    #     mycursor.execute(sq,record)
    #     db.commit()    # insert, delete, display
    #     mycursor.close() # close
    #     db.close() # close
    #     return

    # def user_login(self,user_name,password):
    #     db=self.connection()
    #     mycursor=db.cursor()
    #     sq="select fname,user_name from user where user_name=%s and password=%s"
    #     record=[user_name,password]
    #     mycursor.execute(sq,record)
    #     row=mycursor.fetchall()
    #     rc=mycursor.rowcount

    #     mycursor.close()
    #     db.close()

    #     if(rc==0):
    #         return 0
    #     else:
    #         session["user_fname"]=row[0][0]
    #         session["user_name"]=row[0][1]
    #         return 1

    # def user_profile(self):
    #     db=self.connection()
    #     mycursor=db.cursor()
    #     sq="select fname, lname, user_name, email from user where user_name=%s"
    #     record=[session['user_name']]
    #     mycursor.execute(sq,record)
    #     row=mycursor.fetchall()
    #     mycursor.close()
    #     db.close()
    #     return row

    # def user_update(self,fname,lname):
    #     db=self.connection()
    #     mycursor=db.cursor()
    #     sq="update user set fname=%s, lname=%s where user_name=%s"
    #     record=[fname,lname,session['user_name']]    #username change hone pe session destroy ho jana chahiye
    #     mycursor.execute(sq,record)
    #     db.commit()
    #     session['user_fname']=fname
    #     mycursor.close()
    #     db.close()


    # def user_account_delete(self, user_name):   #for deleting user account from the table
    #     db=self.connection()
    #     mycursor = db.cursor()

    #     sq = "delete from user where user_name = %s"

    #     record=[user_name]
    #     mycursor.execute(sq,record)
    #     db.commit()    # commit the transaction
    #     mycursor.close() # close the cursor
    #     db.close() # close the connection
    #     return

    # def change_password(self, user_name, new_password):
    #     db = self.connection()
    #     mycursor = db.cursor()
    #     sq = "update user set password=%s where user_name=%s"
    #     record = [new_password, user_name]
    #     mycursor.execute(sq, record)
    #     db.commit()
    #     mycursor.close()
    #     db.close()


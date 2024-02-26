import mysql.connector

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

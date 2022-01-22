import mysql.connector

class dbcon:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="kafka123@",
        port="3306",
        database="WManage",
        auth_plugin="mysql_native_password")
    mycursor = mydb.cursor()


    def checkdbconnet(self):
        if self.mydb:
            print("Connection Successful")
        else:
            print("Connection Unsuccessful")

object = dbcon()
object.checkdbconnet()
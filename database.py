import mysql.connector
import time
import datetime
from decimal import Decimal
import bcrypt
from mydbconn import mydb

# mysql connection
mydb = mydb()
def connect():
    if(type(mydb) != mysql.connector.connection.MySQLConnection):
        return mydb
    else:
        return True

if(type(mydb) == mysql.connector.connection.MySQLConnection):
    cursor=mydb.cursor()
# create cursor

customer_keys=("first_name", "last_name", "username", "customer_id", "email_id")
password_keys=("customer_id","username", "password")
transaction_keys=("currency_id", "total_bought", "total_sold", "amount_bought", "amount_sold", "customer_id")
bought_keys=("currency_id", "total_bought", "buying_amt", "time_bought", "customer_id")
sold_keys=("currency_id", "total_sold", "selling_amt", "time_sold", "customer_id")

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def get_dictionary(keys,values):
    dictionary = {}
    for i in range(len(values)):
        dictionary[keys[i]]=values[i]
    return dictionary

def insert_customer(first,last,user,pwd,email): 
    try:
        result = get_customer()
        flag=False
        for x in result:
            if(user==x["username"]):
                flag=True
        if(flag):
            return "Username Already Exists"
        hashpwd = get_hashed_password(pwd) 
        cursor.execute("INSERT INTO Customers(first_name, last_name, username, password, email_id) VALUES (\"" + first + "\",\"" + last +"\",\""+ user +"\",\"" + hashpwd + "\",\"" + email + "\")")

        # commit changes
        mydb.commit()
        return True
    except (Exception) as e:
        print(e)
        return e

def get_customer(customer_id=None):
    try:
        if(customer_id!=None):
            cursor.execute("SELECT first_name, last_name, username, customer_id, email_id FROM customers WHERE customer_id=\""+ str(customer_id) +"\"")        
        else:
            cursor.execute("SELECT first_name, last_name, username, customer_id, email_id FROM customers")
        result=cursor.fetchall()
        customer_list=[]
        for x in result:
            customer_list.append(get_dictionary(customer_keys,x))
        if(customer_id!=None):
            return customer_list[0]
        return customer_list
    except Exception as e:
        print(e)
        return e
def verify_customer(user,pwd):
    try:
        cursor.execute("SELECT customer_id, username, password FROM customers WHERE username=\""+user+"\"")        
        result=get_dictionary(password_keys,cursor.fetchall()[0])
        
        if(check_password(pwd,result["password"])):
            return result["customer_id"]
        else:
            return False
    except (Exception) as e:
        print(e)
        return False

def update_name(first,last,customer_id):
    try:
        cursor.execute("UPDATE customers SET first_name = \"" + first + "\", last_name = \"" + last + "\" WHERE customer_id="+str(customer_id))
        mydb.commit()
        return True
    except Exception as e:
        return "Cannot Update Name because: "+str(e)
    
def delete_customer(customer_id):
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id="+str(customer_id))
        mydb.commit()
        return True
    except Exception as e:
        return "Cannot Delete Account because: "+str(e)

def update_pwd(pwd,customer_id):
    try:
        hashpwd = get_hashed_password(pwd) 
        cursor.execute("UPDATE customers SET password = \"" + hashpwd + "\" WHERE customer_id="+str(customer_id))
        mydb.commit()
        return True
    except Exception:
        return "Cannot Update Password"

def buy_currency(currency_id, total_bought, amount_bought, customer_id): 
    try:
        total_bought = Decimal(str(total_bought))
        amount_bought = Decimal(str(amount_bought))
        result = get_transaction(currency_id,customer_id)
        if(len(result)!=0):
            result=result[0]
            cursor.execute("UPDATE Transactions SET total_bought = " + str(total_bought+result["total_bought"]) + ", amount_bought = " + str(amount_bought+result["amount_bought"]) + " WHERE customer_id="+str(customer_id)+" AND currency_id="+str(currency_id))
        else:
            cursor.execute("INSERT INTO Transactions(currency_id, total_bought, amount_bought, customer_id) VALUES (" + str(currency_id) + "," + str(total_bought) +","+ str(amount_bought) +"," + str(customer_id) + ")")

        # commit changes
        mydb.commit()

        cursor.execute("INSERT INTO Bought(currency_id, total_bought, buying_amt, time_bought, customer_id) VALUES (" + str(currency_id) + "," + str(total_bought) +","+ str(amount_bought) +",\""+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +"\"," + str(customer_id) + ")")
        
        # commit changes
        mydb.commit()
        return True
    
    except (Exception) as e:
        print(e)
        return False

def sell_currency(currency_id, total_sold, amount_sold, customer_id): 
    try:
        result = get_transaction(currency_id,customer_id)
        if(len(result)==0):
            return "You Don't own this Currency"
        result=result[0]
        total_sold = Decimal(str(total_sold))
        amount_sold = Decimal(str(amount_sold))
        if(result['total_bought']>=(total_sold+result['total_sold'])):
            cursor.execute("UPDATE Transactions SET total_sold = \"" + str(total_sold+result["total_sold"]) + "\", amount_sold = " + str(amount_sold+result["amount_sold"]) + " WHERE customer_id="+str(customer_id)+" AND currency_id="+str(currency_id))
        else: 
            return "Amount must be less than Owned Amount"
        # commit changes
        mydb.commit()

        cursor.execute("INSERT INTO Sold(currency_id, total_sold, selling_amt, time_sold, customer_id) VALUES (" + str(currency_id) + "," + str(total_sold) +","+ str(amount_sold) +",\""+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +"\"," + str(customer_id) + ")")
        
        # commit changes
        mydb.commit()
        return True
    
    except (Exception) as e:
        print(e)
        return False

def get_transaction(currency_id=None,customer_id=None):
    if(customer_id!=None):
        if(currency_id==None):
            cursor.execute("SELECT * FROM transactions WHERE customer_id="+str(customer_id))
        else:
            cursor.execute("SELECT * FROM transactions WHERE customer_id="+str(customer_id)+" AND currency_id="+str(currency_id))
    else:
        cursor.execute("SELECT * FROM transactions")
    result=cursor.fetchall()
    transaction_list=[]
    for x in result:
        transaction_list.append(get_dictionary(transaction_keys,x))
    return transaction_list

def get_buying_details(currency_id=None,customer_id=None):
    if(customer_id!=None):
        if(currency_id==None):
            cursor.execute("SELECT * FROM bought WHERE customer_id="+str(customer_id))
        else:
            cursor.execute("SELECT * FROM bought WHERE customer_id="+str(customer_id)+" AND currency_id="+str(currency_id))
    else:
        cursor.execute("SELECT * FROM bought")
    result=cursor.fetchall()
    buying_list=[]
    for x in result:
        buying_list.append(get_dictionary(bought_keys,x))
    return buying_list

def get_selling_details(currency_id=None,customer_id=None):
    if(customer_id!=None):
        if(currency_id==None):
            cursor.execute("SELECT * FROM sold WHERE customer_id="+str(customer_id))
        else:
            cursor.execute("SELECT * FROM sold WHERE customer_id="+str(customer_id)+" AND currency_id="+str(currency_id))
    else:
        cursor.execute("SELECT * FROM sold")
    result=cursor.fetchall()
    selling_list=[]
    for x in result:
        selling_list.append(get_dictionary(sold_keys,x))
    return selling_list


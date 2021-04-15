import mysql.connector

# mysql connection
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "admin", database = "crypto_storage")

# create cursor
cursor=mydb.cursor()

# create database
# cursor.execute("CREATE DATABASE crypto_storage ")

# cursor.execute("DROP TABLE Transactions")
# cursor.execute("DROP TABLE Bought")
# cursor.execute("DROP TABLE Sold")
# cursor.execute("DROP TABLE Customers")
# cursor.execute("CREATE TABLE Customers(customer_id INT AUTO_INCREMENT, CONSTRAINT PK_Customers PRIMARY KEY (customer_id), first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, email_id VARCHAR(255) NOT NULL, CHECK (email_id LIKE '%@%.%' AND email_id NOT LIKE '@%' AND email_id NOT LIKE '%@%@%'))")
# cursor.execute("CREATE TABLE Transactions (currency_id INT NOT NULL, total_bought DECIMAL(16,4) NOT NULL, total_sold DECIMAL(16,4) NOT NULL DEFAULT 0, amount_bought DECIMAL(16,4) NOT NULL, amount_sold DECIMAL(16,4) NOT NULL DEFAULT 0, customer_id INT, CONSTRAINT FK_Customers_Transaction FOREIGN KEY (customer_id) REFERENCES Customers(customer_id), CONSTRAINT PK_Transactions PRIMARY KEY(customer_id, currency_id)) ")
# cursor.execute("CREATE TABLE Bought (currency_id INT NOT NULL, total_bought DECIMAL(16,4) NOT NULL, buying_amt DECIMAL(16,4) NOT NULL, time_bought TIMESTAMP NOT NULL, customer_id INT, CONSTRAINT FK_Customers_Bought FOREIGN KEY (customer_id) REFERENCES Customers(customer_id), CONSTRAINT PK_Transactions PRIMARY KEY(customer_id, currency_id,time_bought))")
# cursor.execute("CREATE TABLE Sold (currency_id INT NOT NULL, total_sold DECIMAL(16,4) NOT NULL, selling_amt DECIMAL(16,4) NOT NULL, time_sold TIMESTAMP NOT NULL, customer_id INT, CONSTRAINT FK_Customers_Sold FOREIGN KEY (customer_id) REFERENCES Customers(customer_id), CONSTRAINT PK_Transactions PRIMARY KEY(customer_id, currency_id,time_sold))")

#https://www.geeksforgeeks.org/python-program-to-sort-and-find-the-data-in-the-student-records/#
import pymysql
import sys
import os
connection = pymysql.connect(
    host='sql9.freesqldatabase.com',
    user='sql9618784',
    password='ej2mLj1XvS',
    db='sql9618784'

)
def create_table():
    with connection.cursor() as cursor:
        sql="CREATE TABLE IF NOT EXISTS games (name VARCHAR(20), won int Not NULL, lost int Not NULL, draw int Not NULL, games int Not NULL)"
        cursor.execute(sql)
        connection.commit()
        print("Table created")


def view():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM games ORDER BY won DESC"
        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
            # Print column headers
            print("{:<10} {:<10} {:<10} {:<10} {:<10}".format("Name", "Won", "Lost", "Tie", "Total"))
            print("------------------------------------------------")
            for row in result:
                name, won, lost, tie, total = row
                print("{:<10} {:<10} {:<10} {:<10} {:<10}".format(name, won, lost, tie, total))
        else:
            print("No data found in the 'games' table.")

#update
def add():
    namee=input("Name: ")
    wonn=int(input("Wins: "))
    lostt=int(input("Losses: "))
    draww=int(input("Ties: "))
    gamess= int(wonn)+int(lostt)+int(draww)

    with connection.cursor() as cursor:
        sql="INSERT INTO games (name, won, lost, draw, games) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (namee, wonn, lostt, draww, gamess))
        connection.commit()
        print("{} was added to  database".format(namee))

def delete():
    namee=input("Name: ")
    with connection.cursor() as cursor:
        sql="delete from games where name={}".format(namee)
        cursor.execute(sql)
        connection.commit()
        print("{} was deleted from database".format(namee))




def option():
    print("Payer Manager\n")
    print("COMMAND VIEW")
    print("view - View  players")
    print("add  - Add a player")
    print("del  - Delete a player")
    print("exit - Exit program\n")
    print("Command: ", end="")
    choice=input()
    if choice=="view":
        view()
    elif choice=="add":
        add()
    elif choice=="del":
        delete()
    elif choice=="exit":
        sys.exit()
    elif choice=="table":
        create_table()






option()




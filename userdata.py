import mysql.connector
import streamlit as st

def connect_to_database():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1307',
            database='books_db'
        )
        return db
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

def login(email, password):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            detail = cursor.fetchone()
            if detail and detail[0] == password:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def get_books_from_db():
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT title, author, price FROM book")
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    else:
        return []

def signup(email, name, address, phnumber, sign_password):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (user_id, email, name, password, address, phonenumber) VALUES (DEFAULT, %s, %s, %s, %s, %s)",
                (email, name, sign_password, address, phnumber)
            )
            db.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def get_details(email):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT user_id, name, address, phonenumber, email FROM users WHERE email = %s", (email,))
            details = cursor.fetchone()
            if details:
                return details
            else:
                return []
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    else:
        return []

def place_order(user_id, total_amt, paymentmethod, book_list, qty_list):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO orders (user_id, ordertotal, paymentmethod) VALUES (%s, %s, %s)", (user_id, total_amt, paymentmethod))
            cursor.execute("SELECT LAST_INSERT_ID()")
            order_id = cursor.fetchone()[0]
            for book, qty in zip(book_list, qty_list):
                cursor.execute("INSERT INTO orderitems (order_id, item_name, quantity) VALUES (%s, %s, %s)", (order_id, book, qty))
            db.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def get_user_data():
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT user_id, email, name, address, phonenumber FROM users")
            details = cursor.fetchall()
            detail_dict = {
                'User Id': [i[0] for i in details],
                'Email Id': [i[1] for i in details],
                'Name': [i[2] for i in details],
                'Address': [i[3] for i in details],
                'Phone Number': [i[4] for i in details]
            }
            return detail_dict
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return {}
        finally:
            cursor.close()
            db.close()
    else:
        return {}

def get_order_data():
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM orders")
            details = cursor.fetchall()
            details_dict = {
                'Order Id': [i[0] for i in details],
                'User Id': [i[1] for i in details],
                'Total Amount': [i[2] for i in details],
                'Payment Method': [i[3] for i in details]
            }
            return details_dict
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return {}
        finally:
            cursor.close()
            db.close()
    else:
        return {}

def get_orderitem_data():
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM orderitems")
            details = cursor.fetchall()
            details_dict = {
                'order_id': [i[0] for i in details],
                'Book Item': [i[1] for i in details],
                'QTY': [i[2] for i in details]
            }
            return details_dict
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return {}
        finally:
            cursor.close()
            db.close()
    else:
        return {}

def update_details(user_id, email, name, address, number):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE users SET email = %s, name = %s, address = %s, phonenumber = %s WHERE user_id = %s",
                (email, name, address, number, user_id)
            )
            db.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def update_password(user_id, password):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (password, user_id))
            db.commit()
            return True
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    else:
        return False

def get_orderitem_detail(order_id):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM orderitems WHERE order_id = %s", (order_id,))
            details = cursor.fetchall()
            detail_dict = {
                'order_id': [i[0] for i in details],
                'Book Item': [i[1] for i in details],
                'QTY': [i[2] for i in details]
            }
            return detail_dict
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
            return {}
        finally:
            cursor.close()
            db.close()
    else:
        return {}

def delete_user(user_id):
    db = connect_to_database()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")
            cursor.execute(
                "DELETE users, orders, orderitems FROM users "
                "INNER JOIN orders ON users.user_id = orders.user_id "
                "INNER JOIN orderitems on orders.order_id = orderitems.order_id "
                "WHERE users.user_id = %s", (user_id,)
            )
            db.commit()
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

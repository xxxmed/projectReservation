from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Consider using environment variables or a secure configuration file for credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "azerty",
    "database": "reservation_project"
}


@app.route('/')
def signIN():
    return render_template("index.html")  # Assuming the template exists

email_x=""

@app.route('/exe', methods=['POST'])
def exe():
    connection = None
    cursor = None
    global email_x
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepared statement with parameter for email
        cursor.execute("SELECT email FROM users WHERE email = %s", (request.form['email'],))
        result = cursor.fetchone()  # Fetch only the first matching email (if any)
        
        
        if result:
            email_x=result[0]
            return render_template("rempli.html", email=result[0])  # Access email from the tuple
        else:
            return "Email not found. Please try again."

    except mysql.connector.Error as err:
        # Handle database errors appropriately (e.g., logging)
        return f"An error occurred: {err}"

    finally:
        # Ensure connections are closed even in case of exceptions
        if cursor:
            cursor.close()
        if connection:
            connection.close()


print(email_x)

@app.route('/end', methods=['POST'])
def end():
    global email_x
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepared statement with parameter for email
        cursor.execute("SELECT id FROM reservations WHERE date_r = %s and heure_r = %s", (request.form['date'],request.form['hour']))
        result = cursor.fetchone()  # Fetch only the first matching email (if any)
        if result:
            return  "date reservée" # Access email from the tuple
        
        cursor.execute("insert into reservations(date_r,heure_r) values(%s,%s)", (request.form['date'],request.form['hour']))
        connection.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        reservation_id = cursor.fetchone()[0]
        cursor.execute("update  users set id_r=%s where email=%s", (reservation_id,email_x))
        connection.commit()
        return "<h1>congrats</h1>"

    except mysql.connector.Error as err:
        # Handle database errors appropriately (e.g., logging)
        return f"An error occurred: {err}"

    finally:
        # Ensure connections are closed even in case of exceptions
        if cursor:
            cursor.close()
        if connection:
            connection.close()







if __name__ == '__main__':
    app.run()

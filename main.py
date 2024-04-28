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


@app.route('/exe', methods=['POST'])
def exe():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepared statement with parameter for email
        cursor.execute("SELECT email FROM users WHERE email = %s", (request.form['email'],))
        result = cursor.fetchone()  # Fetch only the first matching email (if any)
        print(result)
        if result:
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



@app.route('/rempli', methods=['POST'])
def rempli():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepared statement with parameter for email
        cursor.execute("SELECT  FROM users WHERE email = %s", (request.form['email'],))
        result = cursor.fetchone()  # Fetch only the first matching email (if any)
        print(result)
        if result:
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
    date = request.form['date']
    hour = request.form['hour']

@app.route('/end')
def end():
    return 'Hello Page'


if __name__ == '__main__':
    app.run()

from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the main page ('/')
@app.route('/')
def index():
    """
    This function runs when someone visits the homepage.
    It tells Flask to find 'index.html' inside the 'templates' folder and show it.
    """
    return render_template('index.html')

# This part runs the server when you execute the script with 'python app.py'
if __name__ == '__main__':
    # debug=True makes the server auto-reload when you save changes
    app.run(debug=True)
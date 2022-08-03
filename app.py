from flask import Flask, redirect, render_template, request
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_url = db.Column(db.String(2000), nullable=False)
    new_url = db.Column(db.String(100), nullable=False)

    def __init__(self, org_url, new_url):
        self.org_url = org_url 
        self.new_url = new_url 

# https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def url_generator(size=10, chars=string.printable + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        search_url = id 
        search_result = Url.query.filter_by(new_url=search_url).first()

        if search_result != None: 
            redirect(search_result.org_url)
        else:
            # handle_404('query not found')
            pass
    return render_template('home.html')

@app.route('/<string:id>', methods=['POST'])
def index():
    
    if request.method == 'POST':
        org_url = request.form.get('org_url') # input from form
        new_url = url_generator() # random generation

        # creat new database entry
        new_url_entry = Url(org_url, new_url)
        db.session.add(new_url_entry)
        db.session.commit()
        return new_url # return new url to user

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return render_template('errors/404.html'), 404

@app.errorhandler(exceptions.MethodNotAllowed)
def handle_500(err):
    return render_template('errors/500.html'), 500

@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405(err):
    return render_template('errors/405.html'), 405

if __name__ == "__main__":
    app.run(debug=True)
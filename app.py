from flask import Flask, redirect, render_template, request, url_for
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
import string
import random
import os
# from dotenv import load_dotenv

# load_dotenv()
# HOST_URL = os.getenv('HOST_URL')
HOST_URL = 'http://127.0.0.1:5000'
# DB_URI = os.getenv('DB_URI')

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
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
    choices = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    x = ''.join(random.choice(choices) for _ in range(size))
    return x.replace(' ', '')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def home():
    # create short links
    if request.method == 'POST':
        org_url = request.form.get('org_url') # input from form
        new_url = url_generator() # random generation

        print('org_url: ', org_url)
        print('new_url: ', new_url)

        # creat new database entry
        new_url_entry = Url(org_url, new_url)
        db.session.add(new_url_entry)
        db.session.commit()
        short_url = f"{HOST_URL}/{new_url}"

        return display_link(short_url)
    else: 
        return render_template('home.html')

@app.route('/link', methods=['POST', 'GET'])
def display_link(url):
    return render_template('link.html', url=url)
        
@app.route('/<string:id>', methods=['GET'])
def redirect(id):

    if(request.method == 'GET'):
        #print('id: ', id)
        #redirect from shortened url
        search_url = id 
        search_result = Url.query.filter_by(new_url=search_url).first()
        print(search_result)  #<-- Now always return None

    #     if search_result != None: 
    #         redirect(search_result.org_url)
    #     else:
    #         # handle_404('query not found')
    #         pass
    return render_template('home.html')

# Temp delete all rows route
@app.route('/d', methods=['GET'])
def delete():
    # create short links
    if request.method == 'GET':
        try:
            db.session.query(Url).delete()
            db.session.commit()
        except:
            print('nothing to delete')
        

@app.errorhandler(exceptions.NotFound)
def handle_404(err):
    return render_template('errors/404.html'), 404

@app.errorhandler(exceptions.InternalServerError)
def handle_500(err):
    return render_template('errors/500.html'), 500

@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405(err):
    return render_template('errors/405.html'), 405

if __name__ == "__main__":
    app.run(debug=True)
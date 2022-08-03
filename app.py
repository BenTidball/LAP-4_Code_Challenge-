from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
import string
import random

HOST_URL = 'http://127.0.0.1:5000'

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
        short_url = f"{HOST_URL}/wdoge/{new_url}"

        return display_link(short_url)
    else: 
        return render_template('home.html')

@app.route('/link', methods=['POST', 'GET'])
def display_link(url):
    return render_template('link.html', url=url)
        
@app.route('/wdoge/<url>', methods=['GET'])
def windoge(url):
    if request.method == 'GET':
        #redirect from shortened url
        search_result = Url.query.filter_by(new_url=url).first().org_url
        # try:
        print('result:', search_result)
        return redirect(f"{search_result}")
        # except:
        #     return handle_404('url not found')

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
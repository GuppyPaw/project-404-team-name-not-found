from crypt import methods
import os
import datetime

from pymysql import NULL, Time
from playhouse.shortcuts import model_to_dict

from flask import Flask, render_template, request, Response
from flask_mail import Mail, Message
from peewee import *


from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared',uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect() 
mydb.create_tables([TimelinePost])


app.config.update(dict(
    MAIL_SERVER = 'smtp.mail.yahoo.com',
    MAIL_PORT = '465',
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'form.responses@yahoo.com',
    MAIL_PASSWORD = "adydfilgvbjovvqe",
    MAIL_DEBUG = True
))
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"))
    

@app.route('/travels')
def travels():
    return render_template('travels.html', title="Oh, the places I've Been!", url=os.getenv("URL"))

@app.route('/contact',methods=["POST","GET"])
def contact():
    if request.method=="POST":
        first= str(request.form["first"])
        last=str(request.form["last"])
        email=str(request.form["email"])
        subject= str(request.form["subject"])
        message= str(request.form["message"])
        msg = Message(subject, sender='form.responses@yahoo.com', recipients=['smrithic@terpmail.umd.edu'])
        sendthis= first + ' ' + last + ' sent you a message, Smrithi!' + '\n' + 'Message: ' + message + '\n'+ "Respond at "+ email
        msg.body=sendthis
        mail.send(msg)
    return render_template('contact.html', title="Get in Touch!", url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    
    if 'name' in request.form:
        name = request.form['name']
    else:
        return Response("Invalid name",status=400)

    email = request.form['email']
    if '@' not in email:
        return Response("Invalid email",status=400)

    content = request.form['content']
    if content == "":
        return Response("Invalid content",status=400)

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return{
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def del_time_line_post():
    post = TimelinePost.get(TimelinePost.name == request.form['name'])
    post.delete_instance()
    return{
        "Instance deleted":200
    }

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")
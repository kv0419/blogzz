from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogzz:beproductive@localhost:8889/blogzz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer,primary_key = True)        
    username = db.Column(db.String(120),unique = True)
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog',backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged In')
            return redirect('/newpost')
        else:
            flash('Password incorrect or Username does not exist','error')

    return render_template('login.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect ('/newpost')
        else:
            return "<h1> This User already exists, try another!<h1>"

    return render_template('signup.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


@app.route('/blogview', methods = ['GET',"POST"])
def blogview():
    #query that gets a specific blog id
    ids = request.args.get('blog')
    blog = Blog.query.get(int(ids))
    return render_template("blogview.html",blog = blog)

##TODOS
@app.route('/blogs', methods = ['GET','POST'])
def blogs():
    #query that gets blogtitles and blogbodies
    return render_template("allblogs.html", stuff = Blog.query.all())

@app.route('/newpost', methods = ['GET', 'POST'])
def newpost():
    #using this route a NEW blog post is added to database
    
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_owner = User.query.filter_by()

        title_error =''
        if (blog_title ==''):
            title_error = "This is not a valid title"
        
        body_error =''
        if (blog_body ==''):
            body_error = "Try again, write a blog!!"

        if title_error or body_error:
            return render_template("newblog.html", title_error = title_error, body_error = body_error)
        
        else:
                   
            new_blog = Blog(blog_title, blog_body, blog_owner)
            db.session.add(new_blog)
            db.session.commit()
            strid = str(new_blog.id)
            return redirect('/blogview?blog=' + strid)

    return render_template("newblog.html")


@app.route('/', methods=['POST', 'GET'])
def index():
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body, owner)
        
        db.session.add(new_blog)
        db.session.commit()
    blogs = Blog.query.filter_by(owner = owner).all()
    
    return render_template('allblogs.html', stuff = Blog.query.all())


if __name__ == '__main__':
    app.run()
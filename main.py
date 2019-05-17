from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(10000))
    ##completed = db.Column(db.Boolean)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        ##self.completed = False

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

        title_error =''
        if (blog_title ==''):
            title_error = "This is not a valid title"
        
        body_error =''
        if (blog_body ==''):
            body_error = "Try again, write a blog!!"

        if title_error or body_error:
            return render_template("newblog.html", title_error = title_error, body_error = body_error)
        
        else:
        
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            strid = str(new_blog.id)
            return redirect('/blogview?blog=' + strid)

    return render_template("newblog.html")
# @app.route('/blogview' methods = ['post'])
# def blogview():
#     blogtitle = query for specific title
#     blogbody = query for specific body
#       return render_template("blogview.html" ?blogtitle and blogbody for id#?)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('/login.html')

#     if request.method == 'POST':
#         blog_title = request.form['blogtitle']
#         new_blog = Blog(blog_name)
#         db.session.add(new_blog)
#         db.session.commit()

#     blogs = Blog.query.filter_by(completed=False).all()
#     completed_blogs = Blog.query.filter_by(completed=True).all()
#     return render_template('blogs.html',title="Here is the Blog!", 
#         blogs=blogs, completed_blogs=completed_blogs)


if __name__ == '__main__':
    app.run()
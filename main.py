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


##TODOS
@app.route('/blogs', methods = ['get',"post"])
def blogs():
    #query that gets blocktitles
    #query that gets blogbodies
    return render_template("allblogs.html", stuff = Blog.query.all()) # ?blogtitles and blogbodies?)

@app.route('/newpost', methods = ['get', 'post'])
def newpost():
    #using this route a NEW blog post is added to database
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blogs')
    return render_template("newblog.html")

# @app.route('/blogview' methods = ['post'])
# def blogview():

#     blogtitle = query for specific title
#     blogbody = query for specific body

#     return render_template("blogview.html" ?blogtitle and blogbody for id#?)


# @app.route('/', methods=['POST', 'GET'])
# def index():

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
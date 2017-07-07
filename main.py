from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os 
import jinja2

# template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Nswdy@@@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(240))

    def __init__(self, title,content):
        self.title = title
        self.content = content
    
def get_blogList():
    return Blog.query.all() # From Blog database query all 

@app.route('/')
def index():
    return redirect('/blog') # redirect route "/" to "/blog" route

@app.route('/blog')
def blogPage():
    id_number = request.args.get("id")
    if id_number == None:
        return render_template('mainblog.html', blog=get_blogList(), blogID=id_number) # blog variable injects get_blogList function 
    else:
        single_blog = Blog.query.filter_by(id=id_number).first()
        return render_template("singlepage.html", blog=single_blog)

@app.route('/addnewform')
def go_to_AddForm():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     content = request.form['content']
    #     blog = Blog(title,content)
    #     if title.length < 10 or content.length < 100:
    #         return '<h3> please type title in corrent title and content, title should longer than 10 characters and content should longer than 100.</h3> '
    #     else:
    #     db.session.add(blog)
    #     db.session.commit()
    #     return redirect("/")
    return render_template('addnewform.html')

@app.route('/pushtoDB', methods=['POST'])
def add_new_form():

    title = request.form['title']
    content = request.form['content']
    blog = Blog(title,content)
    if len(title) == 0 or len(title) > 20:
        return '<p>please enter a valid title</p>'
    elif len(content) == 0 or len(content) > 100:
        return '<p>please enter a valid content</p>'
    else:
        db.session.add(blog)
        db.session.commit()
        return redirect("/blog?id=" + str(blog.id))



@app.route('/singlepage', methods=['POST'])
def single_page():
     return render_template('singlepage.html',title=title,blog=blog)


if __name__ == '__main__':
    app.run()
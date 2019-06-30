from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__, template_folder='template')
app.config.from_object(config)
db = SQLAlchemy(app)

@app.route('/')
def home():
    from models import Post
    posts = Post.query.all()
    return render_template('all_posts.html', posts=posts)

@app.route('/add_post/', methods=['GET', 'POST'])
def add_form():
    from forms import PostForm
    from models import Post
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate():
            post = Post(**form.data)
            db.session.add(post)
            db.session.commit()
            return home()
        else:
            return str(form.errors), 400
    elif request.method == 'GET':
        return render_template('add_post.html')
    else:
        return 'bad method', 400


if __name__ == '__main__':
    from models import db
    db.create_all()
    app.run()
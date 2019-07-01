from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__, template_folder='template')
app.config.from_object(config)
db = SQLAlchemy(app)

@app.route('/')
def home():
    from models import Post
    post_objects = Post.query.all()
    post_array = []
    for p in post_objects:
        post_array.append(
            {
                'id': p.id,
                'title': p.title,
                'text': p.text[:500],
                'date_created': p.date_created,
                'is_visible': p.is_visible,
                'str_end': '>>>',
            }
        )

    return render_template('all_posts.html', posts=post_array)

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

@app.route("/view_post/<p_id>")
def view_post(p_id):
    from models import Post, Comment
    id = int(p_id)
    post = Post.query.filter_by(id=id).first()
    comments = Comment.query.filter_by(post_id=id)
    p = {
        'post': post,
        'comments': comments
    }
    return render_template('view_post.html', post=p)

@app.route("/add_comment/", methods=['POST'])
def add_comment():
    from models import Comment
    from forms import CommentForm
    if request.method == 'POST':
        form = CommentForm(request.form)
        if form.validate():
            comment = Comment(**form.data)
            db.session.add(comment)
            db.session.commit()
            return view_post(comment.post_id)
        else:
            return str(form.errors), 400
    else:
        return 'bad method', 400



if __name__ == '__main__':
    from models import db
    db.create_all()
    app.run()
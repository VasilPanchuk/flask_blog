from app import db
from datetime import date


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    text = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'date_created': self.date_created,
            'is_visible': self.is_visible
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_comment = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False, index=True)
    post = db.relationship(Post, foreign_keys=[post_id, ])
    date_created = db.Column(db.Date, default=date.today)
    is_visible = db.Column(db.Boolean, default=True)

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'post_id': self.post_id,
            'date_created': self.date_created,
            'is_visible': self.is_visible
        }
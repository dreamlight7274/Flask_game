from datetime import datetime
from Project_public import db
from modules.forum.models import Article

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    head_portrait = db.Column(db.String(200), nullable=True)
    is_VIP = db.Column(db.Boolean, nullable=True, default=False)
    is_admin = db.Column(db.Boolean, nullable=True, default=False)
    add_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    article = db.relationship('Article', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.user_name
from datetime import datetime
from Project_public import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(60), nullable=False)
    category_slug = db.Column(db.String(60), nullable=False)
    public_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=True)

    def __repr__(self):
        return '<database_Category %r>' % self.category_name
    # If you want to show something inside, use that.

from datetime import datetime
from Project_public import db
from sqlalchemy.dialects.mysql import LONGTEXT
from enum import IntEnum
from ..auth.models import User
# class parent(db.Model):
#     __abstract__ = True

# LOL, Rainbow 6, Assassin's creed

# IntEnum, it can connect a number and string. string will have
# the attributes of an integer

# two statuses of article

class ArticleStatus(IntEnum):
    draft = 1
    online = 2
class Category(db.Model):  # if want to use parent: Category(parent)
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(60), nullable=False)
    category_slug = db.Column(db.String(60), nullable=False)
    article = db.relationship('Article', backref='category', lazy=True, cascade='all, delete-orphan, save-update')
    # Article: relationship with article.
    # backref: from article, we can get the information of the category
    # lazy: when the article are accessed,
    # the resource will be accessed, so, it's lazy
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships



    def __repr__(self):
        return '<database_Category %r>' % self.category_name
    # If you want to show some information about data inside, use that. for example, you create
    # an object of Category, when you want to "print" this category, it will show the attribute: category_name.
    # print(category)

# relationship table article and classification
articles_clas = db.Table('articles_clas',
                         db.Column('cla_id', db.Integer, db.ForeignKey('classification.cla_id'), primary_key=True),
                         db.Column('article_id', db.Integer, db.ForeignKey('article.article_id'), primary_key=True)

                         # Joint primary key
                         )
class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_name = db.Column(db.String(60), nullable=False)
    excerpt = db.Column(db.String(300), nullable=False)
    content = db.Column(LONGTEXT, nullable=False)
    article_status = db.Column(db.Enum(ArticleStatus), server_default='online', nullable=False)
    public_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=True)
    thumbnail = db.Column(db.String(200), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    # user

    # foreign key from Category
    classifications = db.relationship('Classification', secondary=articles_clas, lazy='subquery',
                                      backref=db.backref('article', lazy=True)) # secondary: the relationship table
    # lazy='subquery' ? make a subquery in main query, the lines of queries will be decreased.
    # backref: from classification find the information of article
    def __repr__(self):
        return '<database_Article %r>' % self.article_name


class Classification(db.Model):
    cla_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cla_name = db.Column(db.String(60), nullable=False, unique=True)
# strategy experience evaluation

    def __repr__(self):
        return '<database_classification %r>' % self.cla_name



# flask db init
# flask db migrate
# flask db upgrade
# flask shell
# from ... import table model
# from project import db
# variable = Model_name(attribute1='', attribute2='')
# db.session.add(variable)
# db.session.commit()
# Model_name.query.all()
# Model_name.query.first()

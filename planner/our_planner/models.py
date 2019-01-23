from our_planner import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename___ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # id is column and the main unique identifier for user
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='author', lazy=True)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class BudgetData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String, nullable=False)
    income_source = db.Column(db.String, nullable=True)
    income = db.Column(db.Float, nullable=True)
    expense_source = db.Column(db.String, nullable=True)
    expense = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"BuddgetData('{self.period}', '{self.user_id}')"


class Transaction(db.Model):
    __tablename___ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String)
    name = db.Column(db.String)
    transaction_type = db.Column(db.String)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __repr__(self):
    #    return f"Transaction('{self.period}', '{self.user_id}', '{self.amount}')"

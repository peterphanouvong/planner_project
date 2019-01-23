# import secrets
import os
from our_planner import app, db, bcrypt
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from our_planner.EventManager import Event
from our_planner.forms import EventForm, BudgetTrackerForm, RegistrationForm, LoginForm
from our_planner.models import User, BudgetData, Transaction


@app.route("/")
def hello():
    # include a taskbar at the top.
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    # say hello to the people
    title = "hi"
    return render_template("welcome.html", title=title)


@app.route("/planner", methods=['GET', 'POST'])
@login_required
def planner():
    title = "Planner"
    form = EventForm()
    user = current_user
    events = Event.query\
        .filter_by(author=user)\
        .order_by(Event.date_posted.desc())
    progress_events = db.session.query(Event).filter_by(status=True, author=user)
    completed_events = db.session.query(Event).filter_by(status=False, author=user)

    if form.validate_on_submit():
        event = Event(title=form.title.data, user_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('planner'))

    if request.method == 'POST':
        if request.form['submit'] == 'clear':
            for event in events:
                db.session.delete(event)
            db.session.commit()
            return redirect(url_for('planner'))

    return render_template("planner.html", title=title, form=form, progress_events=progress_events, completed_events=completed_events)


@app.route("/ajaxExampleProcess", methods=['POST'])
def ajaxExampleProcess():
    myWord = 'sugma'

    return jsonify({'data': myWord})


@app.route("/complete_event", methods=['POST'])
@login_required
def complete_event():

    if request.method == 'POST':
        event_id = request.json['id']
        event = Event.query.get_or_404(event_id)
        event.status = False  # false is completed
        db.session.commit()

    return jsonify({'event': render_template("response.html", event=event)})


@app.route("/add_event", methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()

    if form.validate_on_submit():
        event = Event(title=form.title.data, description=form.description.data)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('planner'))
    return render_template("add_event.html", title="Add Event", legend="New Event", form=form)


@app.route("/edit_event/<int:event_id>", methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()
    if request.method == 'POST':
        event.title = form.title.data
        event.description = form.description.data
        event.due_date = form.due_date.data
        db.session.commit()
        flash('Your event has been updated', 'success')
        return redirect(url_for('planner'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.due_date.data = event.due_date
    return render_template("add_event.html", title="Update", legend="Update Event", form=form)


@app.route("/timetable")
@login_required
def timetable():
    title = "Timetable"
    return render_template("timetable.html", title=title)


@app.route("/budget_tracker", methods=['POST', 'GET'])
@login_required
def budget_tracker():
    title = "Budget_tracker"
    form = BudgetTrackerForm()
    data_list = BudgetData.query.all()
    return render_template("budget_tracker.html", title=title, form=form, data_list=data_list)


@app.route("/get_transaction", methods=['POST', 'GET'])
def get_transaction():
    data = request.get_json()

    if data["amount"]:
        amount = float(data["amount"])
        name = data["name"]
        period = data["period"]
        transaction_type = data["transaction_type"]
        print(current_user.id)
        transaction = Transaction(user_id=current_user.id, period=period, transaction_type=transaction_type, name=name, amount=amount)
        db.session.add(transaction)

        # print(type())
        db.session.commit()

        # return jsonify({'name': name, 'amount': amount})
    # return jsonify({'error': 'Missing data!'})
    return "success"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('welcome'))
        else:
            flash(f'Login Unsuccessful. Please check your email and password ', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created. You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))

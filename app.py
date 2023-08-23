from flask import Flask, render_template, redirect, session, flash
from psycopg2 import IntegrityError
from forms import UserRegisterForm, UserLoginForm, FeedbackForm, DeleteForm
from model import connect_db, db, User, Feedback




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://zackery:zackery1234@localhost:5432/researchManagement"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "itsasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home_page():
    '''Shows application home page'''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''Register new user'''

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserRegisterForm()
    if form.validate_on_submit():
        user = User.register(username=form.username.data, password=form.password.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already in use. Please try another')
            return render_template('register.html', form=form)

        session['username'] = user.username
        flash('Your account has been created', 'success')
        return redirect(f'/users/{user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)

        if user:
            flash(f'Welcome back, {user.username}', 'success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('/login.html', form=form)

    return render_template('/login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("You have been logged out!", "warning")
    return redirect('/')


@app.route('/users/<username>')
def show_user_page(username):
    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('user_page.html', user=user, form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    '''Delete user from application'''
    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('User deleted', 'info')
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    '''Add feedback'''

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(title=form.title.data, content=form.content.data, username=username)

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback has been created!', 'success')
        return redirect(f'/users/{feedback.username}')

    return render_template('feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    '''Update feedback'''

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedback_update.html", form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''Delete feedback'''

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")


if __name__ == '__main__':
    app.debug = True
    app.run()
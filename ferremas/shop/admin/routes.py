from flask import render_template, session, request, redirect, url_for, flash
form .forms import RegistrationForm 
from shop import app, db

@app.route('/')
def homee():
    return "ÑEPE"

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
       # user = User(form.username,data, form.email.data,
       #             form. password.data)
       # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Refidteration page")
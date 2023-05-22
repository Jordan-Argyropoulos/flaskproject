import os
import re
from html import escape

from flask import Flask, session, request, render_template
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectField, SelectMultipleField)
from wtforms.validators import InputRequired, Length, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


class ContactForm(FlaskForm):
    nom = StringField('Nom', validators=[InputRequired()])
    prenom = StringField('Prénom', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    pays = SelectField('Pays', choices=['Belgique', 'Luxembourg', 'Pays-Bas'],
                       validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired(), Length(max=500)])
    genre = RadioField('Genre', choices=['Masculin', 'Féminin'], validators=[InputRequired()])
    sujets = SelectMultipleField('Sujets', choices=['Réparation', 'Commande', 'Autres'], default=['Autres'])


"""def is_email_address_valid(email):
    
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True"""


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == "GET":
        return render_template("form.html", form=form)
    else:
        if form.validate_on_submit():
            nom = escape(request.form['nom'].strip())
            prenom = escape(request.form['prenom'].strip())
            email = escape(request.form['email'].strip())
            pays = [escape(value) for value in request.form.getlist('pays')]
            message = escape(request.form.get('message'))
            genre = escape(request.form.get('genre', ''))
            sujets = [escape(value) for value in request.form.getlist('sujets')]

            data = {
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'pays': pays,
                'message': message,
                'genre': genre,
                'sujets': sujets
            }

            return render_template("result.html", data=data)
        return render_template("form.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)

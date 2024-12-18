from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
from models import db, Uzivatel
from itsdangerous import URLSafeSerializer

# Inicializace Flask aplikace a konfigurace databáze
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Cesta k databázovému souboru
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Zakázání sledování změn pro úsporu zdrojů
app.config['SECRET_KEY'] = 'mysecretkey'  # Tajný klíč pro ochranu proti CSRF

# Inicializace databáze
db.init_app(app)

# Inicializace URLSafeSerializer s tajným klíčem
serializer = URLSafeSerializer(app.config['SECRET_KEY'])

@app.context_processor
def utility_processor():
    def generate_delete_token(id):
        # Serializace ID do tokenu
        token = serializer.dumps(id)
        return token
    return dict(generate_delete_token=generate_delete_token)

# WTForm pro textová pole
class UzivatelForm(FlaskForm):
    jmeno = StringField('Jméno', [
        validators.InputRequired(),
        validators.Length(max=30),
        validators.Regexp(r'^[a-zA-Z ]*$', message="Jsou povoleny pouze ASCII znaky bez interpunkce a bez čísel.")
    ])
    prijmeni = StringField('Příjmení', [
        validators.InputRequired(),
        validators.Length(max=30),
        validators.Regexp(r'^[a-zA-Z ]*$', message="Jsou povoleny pouze ASCII znaky bez interpunkce a bez čísel.")
    ])
    submit = SubmitField('Submit')

# Vytvoření tabulek a naplnění počátečními daty, pokud ještě nejsou přítomny
with app.app_context():
    db.create_all()
    if not Uzivatel.query.first():
        db.session.add_all([
            Uzivatel(jmeno='Alice', prijmeni='Smith'),
            Uzivatel(jmeno='Bob', prijmeni='Johnson'),
            Uzivatel(jmeno='Charlie', prijmeni='Brown')
        ])
        db.session.commit()

@app.route('/')
def index():
    uzivatele = Uzivatel.query.all()
    return render_template('index.html', uzivatele=uzivatele)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = UzivatelForm()
    if form.validate_on_submit():
        new_uzivatel = Uzivatel(jmeno=form.jmeno.data, prijmeni=form.prijmeni.data)
        db.session.add(new_uzivatel)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<token>')
def delete(token):
    try:
        # Deserializace tokenu pro získání ID
        id = serializer.loads(token)
        uzivatel = Uzivatel.query.get_or_404(id)
        db.session.delete(uzivatel)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
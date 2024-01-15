from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import PetForm
import psycopg2

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "adoptSQLAlchemy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

# db.drop_all()
# db.create_all()

@app.route('/')
def home():
    """Home route. Displays all pets"""
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

# @app.route('/add', methods=["GET", "POST"])
# def add_pet():
#     """Handles adding pet form"""
#     form = PetForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         species = form.species.data
#         photo_url = form.photo_url.data
#         age = form.age.data
#         notes = form.notes.data
#         available = form.available.data

#         pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
#         db.session.add(pet)
#         db.session.commit()

#         return redirect('/')
#     else:
#         return render_template('pet-form.html', form=form)

@app.route('/add')
def add_pet_get():
    """Handles GET pet form (Further Study Version)"""
    form = PetForm()
    return render_template('pet-form.html', form=form)
    
@app.route('/add', methods=["POST"])
def add_pet_post():
    """Handles POST pet form (Further Study Version: gets ALL form data at once without have to iterate over each field and pass it in )"""
    form = PetForm(request.form)

    if form.validate_on_submit():
        pet = Pet()
        form.populate_obj(pet)
        db.session.add(pet)
        db.session.commit()
    
    return redirect('/')
    
@app.route('/<int:pet_id>')
def pet_info(pet_id):
    """Shows pet information"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet-info.html', pet=pet)
    
@app.route('/<int:pet_id>/edit', methods=['GET', 'POST'])
def pet_edit(pet_id):
    """Handles editing pet info form"""
    pet = Pet.query.get_or_404(pet_id)
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.photo_url = form.photo_url.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        return redirect(f'/{pet.id}')
    else:
        return render_template('pet-edit.html', form=form, pet=pet)
    

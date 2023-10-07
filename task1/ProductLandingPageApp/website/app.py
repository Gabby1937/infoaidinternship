from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename 
import pytz
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()  # Load variables from .env file into environment
import os

secret_key = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")

# stage your app
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
UPLOAD_FOLDER = './static/images'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = secret_key  # Set a secret key for sessions

db = SQLAlchemy(app)

# Initialize the Flask-Migrate extension
migrate = Migrate(app, db)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image1 = db.Column(db.String(100), nullable=False)
    image2 = db.Column(db.String(100), nullable=False)
    image3 = db.Column(db.String(100), nullable=False)
    image4 = db.Column(db.String(100), nullable=False)
    image5 = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    specification = db.Column(db.String(10))
    
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(250), nullable=False)
    facebook_link = db.Column(db.String(1000))
    twitter_link = db.Column(db.String(1000))
    github_link = db.Column(db.String(1000))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(1000), nullable=False)
    subject = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    
#route

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/about')
def about():
    teams = Team.query.all()
    return render_template('about.html', teams=teams)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        
        new_message = Message(firstname=firstname, lastname=lastname, email=email, subject=subject, content=content)
        db.session.add(new_message)
        db.session.commit()
    return render_template('contact.html')

@app.route('/admin-messages')
def admin_message():
    messages = Message.query.all()
    return render_template('admin-message.html', messages=messages)

# Delete Team
@app.route('/message/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_message(id):
    messages = Message.query.get_or_404(id)
    db.session.delete(messages)
    db.session.commit()
    # flash("Team-member deleted successfully")
    return redirect(url_for('admin_message'))

#for product veiw
@app.route('/product')
def product():
    products = Product.query.all()
    return render_template('product.html', products=products)

@app.route('/services')
def services():
    return render_template('services.html')



@app.route('/add_to_cart/<int:product_id>', methods=['GET', "POST"])
def add_to_cart(product_id):
    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        price = request.form.get('price')
        size = request.form.get('size')

        # Retrieve the cart from the session or create a new one if not exists
        cart = session.get('cart', {})
        
        # Update the cart with the new item
        cart[product_id] = {
            'quantity': quantity,
            'price': price,
            'size': size
        }
        
        session['cart'] = cart  # Store the updated cart in the session
        
        flash('Item added to cart', 'success')

        return redirect(url_for('product'))
    return redirect(url_for('product'))

@app.route('/cart', methods=["GET"])
def cart():
    cart = session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())  # Calculate the cart count
    
    return render_template('cart.html', cart=cart, cart_count=cart_count)


@app.route('/product/<int:id>/details', methods=['GET'])
def product_details(id):
    products = Product.query.get(id)
    return render_template('single.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        # Extract other form fields as needed
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')
        image5 = request.files.get('image5')
        # Read image file as bytes

        description = request.form['description']
        price = request.form['price']
        specification = request.form['specification']
        # current_day = datetime.now(pytz.UTC).strftime('%A')
        # present_time = datetime.now(pytz.UTC)

        # Create a new Product instance
        new_product = Product(name=name, description=description, price=price, specification=specification)

        # Handle the updated image file
        if image1:
            filename = secure_filename(image1.filename)
            image1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image1 = filename
            
        if image2:
            filename = secure_filename(image2.filename)
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image2 = filename
        
        if image3:
            filename = secure_filename(image3.filename)
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image3 = filename
            
        if image4:
            filename = secure_filename(image4.filename)
            image4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image4 = filename
            
        if image5:
            filename = secure_filename(image5.filename)
            image5.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_product.image5 = filename

        # Add and commit the new product to the database
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('add_product'))  # Redirect to the add_product page after submission
    
    return render_template('add_product.html')

@app.route('/add_team', methods=['GET', 'POST'])      
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        # Extract other form fields as needed
        bio = request.form['bio']
        image = request.files.get('image')
        occupation = request.form['occupation']
        facebook_link = request.form['facebook_link']
        twitter_link = request.form['twitter_link']
        github_link = request.form['github_link']
        
        # Create a new Team instance
        new_team = Team(name=name, bio=bio, occupation=occupation, facebook_link=facebook_link, twitter_link=twitter_link, github_link=github_link)
        
        # Handle the updated image file
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_team.image = filename
        
        # Add and commit the new team to the database
        db.session.add(new_team)
        db.session.commit()
        
        return redirect(url_for('add_team'))  # Redirect to the add_team page after submission
    
    return render_template('add_team.html')


# Edit Data in Database routes
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        # Handle updated images
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')
        image5 = request.files.get('image5')
        
        if image1:
            filename = secure_filename(image1.filename)
            image1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image1 = filename
        
        if image2:
            filename = secure_filename(image2.filename)
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image2 = filename
            
        if image3:
            filename = secure_filename(image3.filename)
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image3 = filename
            
        if image4:
            filename = secure_filename(image4.filename)
            image4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image4 = filename
            
        if image5:
            filename = secure_filename(image5.filename)
            image5.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.image5 = filename

        product.specification = request.form['specification']
        product.description = request.form['description']
        # Update other fields as needed
        
        db.session.commit()
        return redirect(url_for('edit_product', product_id=product.id))  # Redirect to the same edit page after update
    
    return render_template('edit-product.html', product=product)

@app.route('/edit_team/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get(team_id)

    if request.method == 'POST':
        team.name = request.form['name']
        team.bio = request.form['bio']
        image = request.files.get('image')
        team.occupation = request.form['occupation']
        team.twitter_link = request.form['twitter_link']
        team.facebook_link = request.form['facebook_link']
        team.github_link = request.form['github_link']
        # Update other fields as needed
        
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            team.image = filename
        
        db.session.commit()
        return redirect(url_for('edit_team', team_id=team.id))  # Redirect to the same edit page after update
    
    return render_template('edit_team.html', team=team)

# View Data in Database
@app.route('/admin-index')
def admin_index():
    return render_template('admin-index.html')

@app.route('/admin_team')
def admin_team():
    teams = Team.query.all()  # Fetch all teams from the database
    return render_template('admin-team.html', teams=teams)

@app.route('/admin_product')
def admin_product():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('admin-product.html', products=products)

# Delete product
@app.route('/products/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    #flash("Product deleted successfully")
    return redirect(url_for('admin_product'))

# Delete Team
@app.route('/teams/<int:id>/delete', methods=['GET', 'DELETE'])
def delete_team(id):
    teams = Team.query.get_or_404(id)
    db.session.delete(teams)
    db.session.commit()
    # flash("Team-member deleted successfully")
    return redirect(url_for('admin_team'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
  
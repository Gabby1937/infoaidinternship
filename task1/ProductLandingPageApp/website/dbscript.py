from app import app, db

# Create an application context
with app.app_context():
    # Now you can work with the database
    db.create_all()
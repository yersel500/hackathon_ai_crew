from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from werkzeug.security import generate_password_hash
from ..models.user import User, db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')
            age = request.form.get('age')
            location = request.form.get('location')
            medical_condition = request.form.getlist('medical_condition')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            
            print("\n=== Registration Attempt ===")
            print(f"Email: {email}")
            print(f"Name: {name}")
            print(f"Age: {age}")
            print(f"Location: {location}")
            print(f"Medical Conditions: {medical_condition}")
            
            # Check database connection
            try:
                db.session.execute(text('SELECT 1'))  # Fixed: Using text()
                print("Database connection successful")
            except Exception as e:
                print(f"Database connection error: {str(e)}")
                raise
            
            # Check for existing user
            try:
                user = User.query.filter_by(email=email).first()
                if user:
                    print("Email already exists in database")
                    flash('Email already exists')
                    return redirect(url_for('user_routes.register'))
                print("Email is unique")
            except Exception as e:
                print(f"Error checking existing user: {str(e)}")
                raise
                
            # Create new user object
            try:
                new_user = User(
                    email=email,
                    name=name,
                    age=int(age) if age else None,
                    location=location,
                    medical_condition=','.join(medical_condition) if medical_condition else None,
                    latitude=float(latitude) if latitude else None,
                    longitude=float(longitude) if longitude else None
                )
                new_user.set_password(password)
                print("User object created successfully")
            except Exception as e:
                print(f"Error creating user object: {str(e)}")
                raise
                
            # Save to database
            try:
                print("Attempting to save to database...")
                db.session.add(new_user)
                db.session.commit()
                print("User successfully saved to database")
                flash('Registration successful! Please login.')
                return redirect(url_for('user_routes.login'))
            except Exception as e:
                print(f"Error saving to database: {str(e)}")
                db.session.rollback()
                raise
                
        except Exception as e:
            print(f"\nFinal error handler: {type(e).__name__}: {str(e)}")
            db.session.rollback()
            flash('An error occurred during registration')
            return redirect(url_for('user_routes.register'))
    
    return render_template('auth/register.html')

@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.')
            return redirect(url_for('user_routes.login'))
            
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
        
    return render_template('auth/login.html')

@user_routes.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        try:
            print("\n=== Profile Update Attempt ===")
            
            # Get form data
            name = request.form.get('name')
            age = request.form.get('age')
            location = request.form.get('location')
            medical_condition = request.form.getlist('medical_condition')
            
            print(f"Name: {name}")
            print(f"Age: {age}")
            print(f"Location: {location}")
            print(f"Medical Conditions: {medical_condition}")
            
            # Update user data
            try:
                current_user.name = name
                current_user.age = int(age) if age else None
                current_user.location = location
                current_user.medical_condition = ','.join(medical_condition) if medical_condition else None
                
                db.session.commit()
                print("User profile updated successfully")
                flash('Profile updated successfully!')
                return redirect(url_for('main.profile'))
            
            except Exception as e:
                print(f"Error updating user profile: {str(e)}")
                db.session.rollback()
                flash('An error occurred while updating your profile')
                return redirect(url_for('main.profile'))
                
        except Exception as e:
            print(f"\nFinal error handler: {type(e).__name__}: {str(e)}")
            db.session.rollback()
            flash('An error occurred during profile update')
            return redirect(url_for('main.profile'))
            
    # GET request - show current profile data
    return render_template('auth/profile.html')

@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


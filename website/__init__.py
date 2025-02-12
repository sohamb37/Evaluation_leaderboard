from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.sqlite3"


def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = fr"Z:\Leaderboard_website\datasets\uploaded_files"
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')    

    from .models import Admin, TransformerModel, Dataset, Users
    
    with (app.app_context()):
        db.create_all()


        # Create a default admin user
        if not Users.query.filter_by(username='admin').first():
            admin_user = Users(username='admin', password='password', email='admin@gmail.com', first_name='admin',
                               user_role='admin', isLoggedIn=False)
            admin_user.set_password('password')
            # Add the user to the session
            db.session.add(admin_user)
            # Commit the session to save the user to the database
            db.session.commit()
            print('Default admin user created.')

    return app
    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    #@login_manager.user_loader
    #def load_user(id):
    #    return User.query.get(int(id))

    # return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
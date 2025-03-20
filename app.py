import os
import eventlet
from flask import Flask, request, jsonify, send_file
from minesweep.game_handler import GameHandler
from config import Config
from routes.auth import auth_bp
from routes.main import main_bp
from routes.minesweep import minesweep_bp

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

app.config.from_object(Config)


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)
app.register_blueprint(minesweep_bp)

from models.user import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_database():
    try:
        # Connect to the default 'postgres' database to check if our database exists
        conn = psycopg2.connect(
            dbname='postgres',  # Connect to the 'postgres' database (default database)
            user='postgres',  # Your PostgreSQL username
            password='your_password',  # Your PostgreSQL password
            host='localhost'
        )
        conn.autocommit = True  # Enable autocommit to execute commands like CREATE DATABASE
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'minesweepdb';")
        exists = cursor.fetchone()

        if not exists:
            # If the database doesn't exist, create it
            cursor.execute("CREATE DATABASE minesweepdb;")
            print("Database 'minesweepdb' created successfully!", flush=True)
        else:
            print("Database 'minesweepdb' already exists.", flush=True)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")

# Call the create_database function before running the app
create_database()

# Initialize the database and create tables if they don't exist
with app.app_context():
    db.create_all()


game_handler = GameHandler(socketio)
game = game_handler.game

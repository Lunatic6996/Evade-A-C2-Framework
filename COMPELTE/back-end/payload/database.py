from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy ORM instance
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the given Flask app context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(255), unique=True, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    protocol = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Assuming your database supports JSON storage, here's an example:
    extra_data = db.Column(db.JSON)

class Command(db.Model):
    """Command model definition."""
    __tablename__ = 'commands'
    
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False)
    command = db.Column(db.Text, nullable=False)
    sent_time = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

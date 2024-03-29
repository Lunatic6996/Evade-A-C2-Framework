from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

# Base for non-Flask models
Base = declarative_base()

# Setup for standalone database access (for TCP server and other uses)
engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5432/evade-c2')
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db(app):
    """Attach the Flask app to the Flask-SQLAlchemy db instance and create the tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)

class Agent(db.Model):  # For use with Flask
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    agent_id = Column(String(255), unique=True, nullable=True)
    address = Column(String(255), nullable=True)
    last_seen = Column(DateTime, nullable=True, default=datetime.utcnow)
    protocol = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    extra_data = Column(JSON)

class Command(db.Model):  # For use with Flask
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    command = Column(Text, nullable=False)
    sent_time = Column(DateTime, default=datetime.utcnow)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

from flask import Flask, render_template, session, request, redirect, url_for
import secret
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

#https://www.sqlalchemy.org/ --- for better work w/ sql

app = Flask(__name__)
app.config['SECRET_KEY'] = secret.SESSION_KEY

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine("sqlite:///example.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="Alice", age=25)

session.add(new_user)
session.commit()

users = session.query(User).all()
print(users)

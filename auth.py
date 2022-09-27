import os

import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv

import database as db

load_dotenv(".env")
APP_KEY = os.getenv("APP_KEY")


users = db.get_users()

usernames = [user["key"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = stauth.Authenticate(
    usernames,
    usernames,
    hashed_passwords,
    "visualiser",
    APP_KEY,
    cookie_expiry_days=3,
)

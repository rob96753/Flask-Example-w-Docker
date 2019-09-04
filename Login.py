from flask import Flask, Response, redirect, url_for, request, session, abort
from flask_login import  LoginManager, current_user, login_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect(url_for('index'))

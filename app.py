from flask import Flask, render_template, request, redirect, url_for, make_response
from meteo import get_weather_data, valid_ville, get_img_src
from db import add_to_db, log_user, add_to_history, show_history
from flask_bcrypt import Bcrypt
from functools import wraps
from dotenv import load_dotenv
import os
import jwt


app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("secret")
bcrypt = Bcrypt(app)


def verify_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_token = request.cookies.get('jwtToken')
        if jwt_token is None:
            return "Erreur : JWT manquant ou incorrect.", 401
        try:
            payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
            kwargs['email'] = payload['email']
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return 'Token expiré. Veuillez vous reconnecter.', 401
        except (jwt.InvalidTokenError, KeyError):
            return 'Token invalide. Veuillez vous reconnecter.', 401
    return wrapper

@app.route('/', methods=['GET'])
def frontpage():
    return render_template('frontpage.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        success_message = "Compte créé avec succès !"
        error_message = add_to_db(email, hashed_password)
        if not error_message:
            return render_template('register.html', success=success_message, error=None)
        else:
            return render_template('register.html', success=None, error=error_message)
    return render_template('register.html', success=None, error=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error_message = log_user(email, password)
        if not error_message:
            payload = {'email': email}
            jwt_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            resp = make_response(redirect('/meteo'))
            resp.set_cookie('jwtToken', jwt_token)
            return resp
        return render_template('login.html', error=error_message)
    return render_template('login.html', error=None)


@app.route('/meteo', methods=['GET'])
def weather_form():
    error_message = request.args.get('error')
    return render_template('weather_form.html', error=error_message)


@app.route('/weather', methods=['GET'])
@verify_jwt
def weather(email):
    try:
        city_name = request.args.get('city')
        if valid_ville(city_name):
            weather_data = get_weather_data(city_name)
            if weather_data:
                img_src = get_img_src(city_name)
                add_to_history(email, city_name, weather_data)
                return render_template('weather.html', city=city_name, weather=weather_data, image_name=img_src, email=email)
            else:
                return "Erreur : Impossible de récupérer les données météo."
        else:
            error_message = "Veuillez rentrer le nom d'une ville valide."
            return redirect(url_for('weather_form', error=error_message))
    except jwt.ExpiredSignatureError:
        return 'Token expiré. Veuillez vous reconnecter.', 401
    except (jwt.InvalidTokenError, KeyError):
        return 'Token invalide. Veuillez vous reconnecter.', 401


@app.route('/history', methods=['GET'])
@verify_jwt
def get_history(email):
    history = show_history(email)
    return render_template('history.html', history=history)


if __name__ == '__main__':
    app.run(debug=True)

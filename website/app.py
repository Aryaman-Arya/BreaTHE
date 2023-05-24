import os
import numpy as np
import tensorflow as tf
from keras.models import load_model
import librosa
from flask import Flask, session, render_template, url_for, request, redirect
import sqlite3
from skimage.transform import resize

app = Flask(__name__)
audio = None
app.secret_key = os.environ['SESSION_SECRET_KEY']
db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

# Create users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
db.commit()


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', user_logged_in = True)
    else:
        return render_template('home.html', user_logged_in = False)


@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html', user_logged_in = True)
    else:
        return render_template('about.html', user_logged_in = False)


@app.route('/subscriptions')
def subscriptions():
    if 'username' in session:
        return render_template('subscriptions.html', user_logged_in = True)
    else:
        return render_template('subscriptions.html', user_logged_in = False)


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', user_logged_in = True)
    else:
        return render_template('index.html', user_logged_in = False)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        # Assuming you have a database connection named 'db' and a cursor named 'cursor'
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            error_message =  "Username already exists!"
            return render_template('signup.html', error_text=error_message)

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()

        # Perform login after successful signup
        session['username'] = username

        return render_template('index.html', user_logged_in = True)

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the database
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
    
        if existing_user:
            # Check if the password is correct
            if password == existing_user[2]:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                error_message = 'Invalid username or password'
                return render_template('login.html', error_text=error_message)
             
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_text=error_message)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' in session:
        audio = request.files["audio"]

        if (not audio):
            return render_template('index.html', error_text="No Audio File Found", user_logged_in = True)

        classes = ["Bronchiectasis", "Bronchiolitis",
                "COPD", "Healthy", "Pneumonia", "URTI"]

        y, sr = librosa.load(audio, res_type='kaiser_fast', duration=10)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        S_dB_resized = resize(S_dB, (224, 224))
        S_dB_resized = np.repeat(S_dB_resized[..., np.newaxis], 3, -1)
        features = np.expand_dims(S_dB_resized, axis=0)

        model = load_model('/home/yash20100/BreaTHE/models/custom_model.h5')
        test_pred = model.predict(features)
        class_pred = classes[np.argmax(test_pred)]
        confidence = test_pred.max()

        output = [class_pred, confidence]

        return render_template('prediction.html', prediction_text="{}".format(output[0]), prediction_confidence="{}".format(output[1]*100))
    else:
        return render_template('login.html', user_logged_in = False)


@app.route('/mlarchitecture')
def mlarchitecture():
    if 'username' in session:
        return render_template('mlarchitecture.html', user_logged_in = True)
    else:
        return render_template('mlarchitecture.html', user_logged_in = False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import numpy as np
import tensorflow as tf
from keras.models import load_model
import librosa
from flask import Flask, render_template, request
from skimage.transform import resize

app = Flask(__name__)
audio = None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    audio = request.files['audio']
    
    if(not audio):
        return render_template('index.html', error_text="No Audio File Found")
    
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

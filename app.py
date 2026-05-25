from flask import Flask, render_template, request
import os, serial
from predict import predict_disease

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Hardware Connection
try:
    ser = serial.Serial('COM3', 9600, timeout=1)
except:
    ser = None

# Sabse pehle ye Database fix kiya
DISEASE_DATA = {
    # TOMATOES
    "Tomato Healthy": {"en": "Great! Maintain regular watering.", "hi": "नियमित सिंचाई जारी रखें।", "color": "#22c55e", "icon": "smile", "is_healthy": True},
    "Tomato Mosaic Virus": {"en": "Remove infected plants; control aphids.", "hi": "संक्रमित पौधों को हटा दें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato Yellow Leaf Curl Virus": {"en": "Use neem oil to control whiteflies.", "hi": "सफेद मक्खियों के लिए नीम तेल का प्रयोग करें।", "color": "#ef4444", "icon": "alert-triangle", "is_healthy": False},
    "Tomato Septoria Leaf Spot": {"en": "Improve air circulation; avoid overhead watering.", "hi": "हवा का संचार बढ़ाएं और ऊपर से पानी न डालें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato Target Spot": {"en": "Apply fungicides containing chlorothalonil.", "hi": "कवकनाशी (Fungicide) का प्रयोग करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato leaf mold": {"en": "Reduce humidity in the greenhouse.", "hi": "नमी कम करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato late blight": {"en": "Use copper-based fungicides immediately.", "hi": "कॉपर कवकनाशी का प्रयोग करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato early blight": {"en": "Prune lower leaves to prevent soil splash.", "hi": "नीचे की पत्तियों की छंटाई करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato bacterial spot": {"en": "Avoid working with plants when they are wet.", "hi": "गीले पौधों पर काम न करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "Tomato spider mites": {"en": "Spray water or insecticidal soap on leaves.", "hi": "कीटनाशक साबुन के घोल का छिड़काव करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},

    # STRAWBERRY
    "Strawberry Healthy": {"en": "Plant is healthy! Good job.", "hi": "पौधा स्वस्थ है!", "color": "#22c55e", "icon": "smile", "is_healthy": True},
    "Strawberry leaf scorch": {"en": "Remove old leaves and ensure proper spacing.", "hi": "पुरानी पत्तियों को हटा दें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},
    "squash powdery mildew": {"en": "Apply sulfur or potassium bicarbonate.", "hi": "सल्फर का छिड़काव करें।", "color": "#ef4444", "icon": "alert-circle", "is_healthy": False},

    # SOYABEAN
    "Soyabean healthy": {"en": "Soil nutrients are perfect.", "hi": "मिट्टी के पोषक तत्व एकदम सही हैं।", "color": "#22c55e", "icon": "smile", "is_healthy": True},

    # PEACH
    "Peach Healthy": {"en": "Tree is healthy. Prune in late winter.", "hi": "पेड़ स्वस्थ है। सर्दियों में छंटाई करें।", "color": "#22c55e", "icon": "smile", "is_healthy": True},
    "Peach Bacterial Spot": {"en": "Apply zinc sulfate or copper sprays.", "hi": "जिंक सल्फेट का छिड़काव करें।", "color": "#ef4444", "icon": "alert-triangle", "is_healthy": False}
}
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/home', methods=['POST', 'GET'])
def home():
    user = request.form.get('username') or request.args.get('username') or "Farmer"
    sensors = {"temp": "26", "humidity": "65", "moisture": "52", "co2": "410"}
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip().split(',')
            if len(line) >= 4:
                sensors["temp"] = line[0]
                sensors["humidity"] = line[1]
                sensors["moisture"] = round(100 - (float(line[2])/10.23), 1)
                sensors["co2"] = line[3]
        except: pass
    return render_template('home.html', sensors=sensors, name=user)

@app.route('/disease', methods=['GET', 'POST'])
def disease():
    user = request.args.get('name', 'Farmer')
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            res, conf = predict_disease(path)
            
            # Ab yahan error nahi aayega
            info = DISEASE_DATA.get(res['en'], {"en": "Consult expert.", "hi": "सलाह लें।", "color": "#ef4444", "icon": "alert-triangle", "is_healthy": False})
            
            return render_template('result.html', result=res, confidence=conf, 
                                 image_file=file.filename, info=info, name=user)
    return render_template('disease.html', name=user)

if __name__ == '__main__':
    app.run(debug=True)
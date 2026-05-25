import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Model path setup
MODEL_PATH = os.path.join('model', 'leaf_model.h5')
model = None

try:
    if os.path.exists(MODEL_PATH):
        # compile=False fixes DepthwiseConv2D keyword errors
        model = load_model(MODEL_PATH, compile=False)
        print(f"--- CropPlus AI Brain Active at {MODEL_PATH} ---")
except Exception as e:
    print(f"Model Load Error: {e}")

def predict_disease(img_path):
    if model is None: 
        return {"en": "Model Error", "hi": "मॉडल त्रुटि"}, 0
    
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    
    # YOUR EXACT ORDER (0-14)
    label_map = {
        0: {"en": "Tomato Healthy", "hi": "टमाटर स्वस्थ है"},
        1: {"en": "Tomato Mosaic Virus", "hi": "टमाटर मोज़ेक वायरस"},
        2: {"en": "Tomato Yellow Leaf Curl Virus", "hi": "टमाटर पीला पत्ता मरोड़ वायरस"},
        3: {"en": "Target Spot", "hi": "टारगेट स्पॉट"},
        4: {"en": "Tomato Septoria Leaf Spot", "hi": "टमाटर सेप्टोरिया पत्ता धब्बा"},
        5: {"en": "Tomato Leaf Mold", "hi": "टमाटर पत्ता मोल्ड"},
        6: {"en": "Tomato Late Blight", "hi": "टमाटर पछेती झुलसा"},
        7: {"en": "Tomato Early Blight", "hi": "टमाटर अगेती झुलसा"},
        8: {"en": "Tomato Bacterial Spot", "hi": "टमाटर बैक्टीरियल स्पॉट"},
        9: {"en": "Strawberry Healthy", "hi": "स्ट्रॉबेरी स्वस्थ है"},
        10: {"en": "Strawberry Leaf Scorch", "hi": "स्ट्रॉबेरी पत्ता झुलsa"},
        11: {"en": "Squash Powdery Mildew", "hi": "कद्दू पाउडर फफूंदी"},
        12: {"en": "Soyabean Healthy", "hi": "सोयाबीन स्वस्थ है"},
        13: {"en": "Peach Healthy", "hi": "आड़ू स्वस्थ है"},
        14: {"en": "Peach Bacterial Spot", "hi": "आड़ू बैक्टीरियल स्पॉट"}
    }
    
    idx = np.argmax(preds)
    result = label_map.get(idx, {"en": "Scanning...", "hi": "जांच जारी है..."})
    conf = round(float(np.max(preds)) * 100, 2)
    
    return result, conf
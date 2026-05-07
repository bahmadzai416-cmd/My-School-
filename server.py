from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import cv2
import numpy as np
import pandas as pd
from io import BytesIO
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/ocr', methods=['POST'])
def ocr_image():
    """Receive image, extract handwritten numbers using simple contour detection"""
    data = request.json
    image_data = data.get('image', '').split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    
    # Simple digit detection (in real app, use Tesseract or TensorFlow)
    # This simulates OCR by finding contours
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    numbers = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # filter small noise
            roi = thresh[y:y+h, x:x+w]
            # Here you would run digit classification
            numbers.append({'x': x, 'y': y, 'value': 0})  # placeholder
    
    return jsonify({'success': True, 'numbers': numbers, 'message': 'OCR complete'})

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """Send SMS (simulated - integrate with Twilio or local gateway)"""
    data = request.json
    numbers = data.get('numbers', [])
    message = data.get('message', '')
    
    # In production: use Twilio, local GSM modem, or Afghan SMS provider
    print(f"SMS to {numbers}: {message}")
    
    return jsonify({'success': True, 'sent': len(numbers)})

@app.route('/api/send-whatsapp', methods=['POST'])
def send_whatsapp():
    """Send WhatsApp message (simulated)"""
    data = request.json
    numbers = data.get('numbers', [])
    message = data.get('message', '')
    
    # In production: use WhatsApp Business API
    print(f"WhatsApp to {numbers}: {message}")
    
    return jsonify({'success': True, 'sent': len(numbers)})

@app.route('/api/export-excel', methods=['POST'])
def export_excel():
    """Generate Excel file from data"""
    data = request.json
    students = data.get('students', [])
    marks = data.get('marks', [])
    
    # Create DataFrame
    df = pd.DataFrame(students)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='لیست', index=False)
    
    output.seek(0)
    return send_file(output, download_name='school_results.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

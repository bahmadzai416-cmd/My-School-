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
    data
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

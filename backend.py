from flask import send_file

@app.route('/api/download_record', methods=['GET'])
def download_record():
    return send_file(RECORD_FILE, as_attachment=True)
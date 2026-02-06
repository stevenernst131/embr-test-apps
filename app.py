import os
from datetime import datetime

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)

# In-memory visitor counter
visitor_count = 0


@app.route('/')
def index():
   global visitor_count
   visitor_count += 1
   print('Request for index page received')
   return render_template('index.html', visit_count=visitor_count, server_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name=name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/api/stats')
def stats():
    """API endpoint returning visitor stats as JSON."""
    return jsonify({
        'visitor_count': visitor_count,
        'server_time': datetime.now().isoformat(),
        'status': 'healthy'
    })

@app.route('/api/echo', methods=['POST'])
def echo():
    """Echo back posted JSON data with a timestamp."""
    data = request.get_json(force=True)
    return jsonify({
        'echo': data,
        'received_at': datetime.now().isoformat()
    })

@app.route('/dashboard')
def dashboard():
    """Dashboard page showing stats and server info."""
    return render_template('dashboard.html', 
                           visit_count=visitor_count,
                           server_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
   app.run(port=8080)

import os
from datetime import datetime

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)

# In-memory state
visitor_count = 0
guestbook = []
app_start_time = datetime.now()


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
       return render_template('hello.html', name=name, 
                              greeting_time=datetime.now().strftime('%I:%M %p'))
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/guestbook')
def guestbook_page():
    """Guestbook page where visitors can leave messages."""
    return render_template('guestbook.html', messages=guestbook)

@app.route('/guestbook/sign', methods=['POST'])
def sign_guestbook():
    """Add a message to the guestbook."""
    name = request.form.get('name', 'Anonymous')
    message = request.form.get('message', '')
    if message.strip():
        guestbook.append({
            'name': name,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return redirect(url_for('guestbook_page'))

@app.route('/api/stats')
def stats():
    """API endpoint returning visitor stats as JSON."""
    uptime = datetime.now() - app_start_time
    return jsonify({
        'visitor_count': visitor_count,
        'guestbook_entries': len(guestbook),
        'uptime_seconds': int(uptime.total_seconds()),
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

@app.route('/api/time')
def server_time():
    """Return current server time in multiple formats."""
    now = datetime.now()
    return jsonify({
        'iso': now.isoformat(),
        'readable': now.strftime('%B %d, %Y at %I:%M %p'),
        'unix': int(now.timestamp())
    })

@app.route('/api/health')
def health():
    """Health check endpoint."""
    uptime = datetime.now() - app_start_time
    return jsonify({
        'status': 'ok',
        'uptime': str(uptime).split('.')[0],
        'started_at': app_start_time.isoformat()
    })

@app.route('/dashboard')
def dashboard():
    """Dashboard page showing stats and server info."""
    uptime = datetime.now() - app_start_time
    return render_template('dashboard.html', 
                           visit_count=visitor_count,
                           guestbook_count=len(guestbook),
                           uptime=str(uptime).split('.')[0],
                           server_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
   app.run(port=8080)

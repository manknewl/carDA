from flask import Flask, render_template, request, Response
import requests
import logging

app = Flask(__name__)

# Replace <raspberry_pi_ip> with the actual IP address of your Raspberry Pi
RASPBERRY_PI_IP = '45bb-216-209-40-155.ngrok-free.app'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    # 1) Try to parse JSON
    body = request.get_json(silent=True)  # silent=True prevents errors if not JSON
    if body and 'direction' in body:
        # JSON param found
        direction = body['direction']
    else:
        # fallback to original form data usage
        direction = request.form.get('direction')
    
    try:
        # 2) Forward as form data to the Pi (no Pi changes needed)
        response = requests.post(
            f'http://{RASPBERRY_PI_IP}/move',
            data={'direction': direction}
        )
        response.raise_for_status()
        return response.text, response.status_code
    except Exception as e:
        app.logger.error(f"Error in /move route: {e}")
        return str(e), 500

@app.route('/image.jpg')
def image():
    try:
        response = requests.get(f'http://{RASPBERRY_PI_IP}/image.jpg', stream=True)
        response.raise_for_status()
        return Response(response.raw, content_type=response.headers['Content-Type'])
    except Exception as e:
        app.logger.error(f"Error in /image.jpg route: {e}")
        return str(e), 500

if __name__ == "__main__":
    # Enable debug mode and set logging level to debug
    app.debug = True
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)


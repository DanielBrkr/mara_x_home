from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

temperature = 0.0
timestamp = 0.0

# Route for updating the temperature
@app.route('/coffee', methods=['POST'])
def update_temperature():

    global temperature
    global timestamp

    data = request.get_json()
    try:
        temperature = float(data['temperature'])
        print('Received temperature:', temperature)
        timestamp = data["timestamp"]
        print('Received time_stamp:', timestamp)

    except (KeyError, ValueError, TypeError):
        temperature = 0.0
        print("Invalid reading")
    return jsonify({'temperature': temperature, "timestamp": timestamp})



stored_data = list()

# Route for rendering the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for returning the current temperature
@app.route('/get_temperature')
def get_temperature():
    #global temperature
    return jsonify({'temperature': temperature, "timestamp": timestamp})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4999)


# Todo: Post Requests gehen nicht mehr durch, könnte damit zusammenhänge das an ein paar stellen die time stamp variable dazu gekommen ist
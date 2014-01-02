import time
from itertools import cycle
from flask import Flask, render_template
from robot_brain.gpio_pin import GPIOPin

app = Flask(__name__)
on_pins = {
    'Telescope': GPIOPin(18),
    'Pixar': GPIOPin(23),
    'Fountain': GPIOPin(24),
}
off_pins = {
    'Telescope': GPIOPin(17),
    'Pixar': GPIOPin(21),
    'Fountain': GPIOPin(22),
}
state_cycle = cycle(['on', 'off'])

@app.route("/")
@app.route("/<channel>/<state>")
def update_lamp(channel=[], state=None):
    if channel == 'all':
        channel = on_pins.keys()
    elif channel:
        channel = [channel]

    for c in channel:
        if c not in on_pins.keys():
            continue
        if state == 'on':
            on_pins[c].set(1)
            time.sleep(.2)
            on_pins[c].set(0)
        if state == 'off':
            off_pins[c].set(1)
            time.sleep(.2)
            off_pins[c].set(0)
        if state == 'toggle':
            state = next(state_cycle)
            update_lamp(c, state)

    template_data = {
        'title' : state,
        'num_channels': len(on_pins),
        'channels': sorted(on_pins.keys()),
    }
    return render_template('main.html', **template_data)

if __name__ == "__main__":
    #app.debug = True
    app.run(host='0.0.0.0', port=80)

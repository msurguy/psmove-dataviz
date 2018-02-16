from websocket_server import WebsocketServer
import logging
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'build'))
import time
import psmove
import json

if psmove.count_connected() < 1:
    print('No controller connected')
    sys.exit(1)

move = psmove.PSMove()
# Important to enable getting orientation values as a calculated quaternion
move.enable_orientation(True)

if move.connection_type == psmove.Conn_Bluetooth:
    print('bluetooth controller connected')

if move.connection_type != psmove.Conn_Bluetooth:
    print('Please connect controller via Bluetooth')
    sys.exit(1)

# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id {:d}".format(client['id']))
    server.send_message_to_all('{ "connected" : "true" }')

# Called for every client disconnecting
def client_left(client, server):
    print("Client({:d}) disconnected".format(client['id']))

# Called when a client sends a message
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print("Client({:d}) said: {}".format(client['id'], message))

print('WebSocket server started')
PORT = 9001
server = WebsocketServer(PORT, host='127.0.0.1', loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

# OrientationFusion_MadgwickIMU
#OrientationFusion_MadgwickIMU = _psmove.OrientationFusion_MadgwickIMU
#OrientationFusion_MadgwickMARG = _psmove.OrientationFusion_MadgwickMARG
#OrientationFusion_ComplementaryMARG = _psmove.OrientationFusion_ComplementaryMARG

while True:
    # Get the latest input report from the controller
    while move.poll():
        pressed, released = move.get_button_events()
        if pressed & psmove.Btn_MOVE:
            move.reset_orientation()
        elif pressed & psmove.Btn_PS:
            sys.exit(0)

    trigger_value = move.get_trigger()

    ax, ay, az = move.get_accelerometer_frame(psmove.Frame_SecondHalf)
    gx, gy, gz = move.get_gyroscope_frame(psmove.Frame_SecondHalf)
    qw, qx, qy, qz = move.get_orientation()
    m = {}

    if trigger_value > 20:
        m = {
            'gx': round(gx, 3), 'gy': round(gy, 3), 'gz': round(gz, 3),
            'ax': round(ax, 3), 'ay': round(ay, 3), 'az': round(az, 3),
            'qx': round(ax, 3), 'qy': round(ay, 3), 'qz': round(az, 3),
            'qw': round(qw, 3)
            }

        server.send_message_to_all(json.dumps(m))

    time.sleep(0.05)




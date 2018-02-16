# This file prints accelerometer, gyro and quaternion data into the terminal

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

        print(json.dumps(m))

    time.sleep(0.05)




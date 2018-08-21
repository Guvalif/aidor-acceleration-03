# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


# 外部プログラムの読み込み
# =============================================================================
from bottle import Bottle, request, response, static_file
from cv2 import VideoCapture, imencode
from paste import httpserver
from wiringpi import *

from adc import analogRead


# 定数定義・初期化処理
# =============================================================================
LIGHT_PIN    = 0
THERMO_PIN   = 1
VOLUME_PIN   = 2
MOTION_PIN   = 26
SERVO_PIN    = 18
CAMERA_INDEX = 0

camera = VideoCapture(CAMERA_INDEX)
router = Bottle()

wiringPiSetupGpio()
pinMode(SERVO_PIN, PWM_OUTPUT)
pwmSetMode(PWM_MODE_MS)
pwmSetRange(1024)
pwmSetClock(375)


# URIの定義・HTTPサーバの起動
# =============================================================================
@router.route('/<file_path:path>', method=['GET'])
def assets_get(file_path):
    return static_file(file_path, root='.')


@router.route('/v2/image', method=['GET'])
def image_get():
    _, frame = camera.read()
    _, image = imencode('.jpg', frame)

    response.headers['Cache-Control'] = 'no-cache'
    response.content_type = 'image/jpg'

    return image.tobytes()


@router.route('/v2/sensor', method=['GET'])
def sensor_get():
    response_json = {
        'resource': 'sensor',
        'data': {
            'light': analogRead(LIGHT_PIN),
            'thermo': analogRead(THERMO_PIN),
            'volume': analogRead(VOLUME_PIN),
            'motion': digitalRead(MOTION_PIN)
        }
    }

    response.headers['Cache-Control'] = 'no-cache'
    response.content_type = 'application/json'

    return response_json


@router.route('/v2/servo', method=['PUT'])
def servo_put():
    pwm = request.json['pwm']

    response_json = {
        'resource': 'servo',
        'data': {
            'command': 'pwm_write',
            'result': pwmWrite(SERVO_PIN, max(min(pwm, 123), 26))
        }
    }

    response.headers['Cache-Control'] = 'no-cache'
    response.content_type = 'application/json'

    return response_json


httpserver.serve(router, host='0.0.0.0', port=80)
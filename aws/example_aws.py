# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


# 外部プログラムの読み込み
# =============================================================================
from json import dumps, loads
from random import choice
from string import ascii_letters, digits
from thread import start_new_thread
import time

from boto3.session import Session
from cv2 import VideoCapture, imencode
from websocket import WebSocketApp
from wiringpi import *

from adc import analogRead
from aws_credentials import *


# 定数定義・初期化処理
# =============================================================================
LIGHT_PIN    = 0
THERMO_PIN   = 1
VOLUME_PIN   = 2
MOTION_PIN   = 26
SERVO_PIN    = 18
CAMERA_INDEX = 0

camera = VideoCapture(CAMERA_INDEX)

session = Session(
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

s3_bucket = session.resource('s3').Bucket(S3_BUCKET_NAME)

wiringPiSetupGpio()
pinMode(SERVO_PIN, PWM_OUTPUT)
pwmSetMode(PWM_MODE_MS)
pwmSetRange(1024)
pwmSetClock(375)


# 独自命令の定義
# =============================================================================
def make_hash(n=4):
    return ''.join( choice(ascii_letters + digits) for _ in xrange(n) )


def make_filename(category, ext):
    timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    return '{}-{}-{}.{}'.format(category, make_hash(), timestamp, ext)


def get_sensor_json():
    return dumps({
        'light': analogRead(LIGHT_PIN),
        'thermo': analogRead(THERMO_PIN),
        'volume': analogRead(VOLUME_PIN),
        'motion': digitalRead(MOTION_PIN)
    })


def get_image(frame_buffer=5):
    [ camera.read() for _ in xrange(frame_buffer) ]

    _, frame = camera.read()
    _, image = imencode('.jpg', frame)

    return image.tobytes()


# WebSocketクライアントの起動
# =============================================================================
def on_message(ws, message):
    message_json = loads(message)

    if message_json['sender'] == IOT_HOST_ID and message_json['target'] == IOT_CLIENT_ID:
        pwm = message_json['data']

        pwmWrite(SERVO_PIN, max(min(pwm, 123), 26))


def on_open(ws):
    def main(*args):
        while True:
            image_name = make_filename('image', 'jpg')

            s3_image = s3_bucket.Object(image_name)
            s3_image.put(
                ACL='public-read',
                Body=get_image(),
                ContentType='image/jpg'
            )


            sensor_json_name = make_filename('sensor', 'json')

            s3_sensor_json = s3_bucket.Object(sensor_json_name)
            s3_sensor_json.put(
                ACL='public-read',
                Body=get_sensor_json(),
                ContentEncoding='utf-8',
                ContentType='application/json'
            )


            message_json = dumps({
                'sender': IOT_CLIENT_ID,
                'target': IOT_HOST_ID,
                'data': {
                    'image': image_name,
                    'sensor': sensor_json_name
                }
            })

            ws.send(message_json)

            time.sleep(5)

    start_new_thread(main, ())


ws = WebSocketApp(
    WS_ENDPOINT,
    on_message=on_message,
    on_error=lambda _0, _1: None,
    on_close=lambda _: None
)

ws.on_open = on_open

ws.run_forever()

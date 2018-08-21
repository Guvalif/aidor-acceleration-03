# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


# 外部プログラムの読み込み
# =============================================================================
from json import dumps
from random import choice
from string import ascii_letters, digits
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from boto3.session import Session
from cv2 import VideoCapture, imencode
from wiringpi import *

from adc import analogRead


# 定数定義・初期化処理
# =============================================================================
LIGHT_PIN    = 0
THERMO_PIN   = 1
VOLUME_PIN   = 2
MOTION_PIN   = 26
CAMERA_INDEX = 0

S3_ACCESS_KEY_ID     = 'PUT_YOUR_ACCESS_KEY_ID_HERE'
S3_SECRET_ACCESS_KEY = 'PUT_YOUR_SECRET_KEY_HERE'
REGION_NAME          = 'ap-northeast-1'
BUCKET_NAME          = 'raspberry-pi-cloud-NN'

CLIENT_ID     = 'raspberry-pi-sender'
MQTT_ENDPOINT = 'PUT_YOUR_MQTT_ENDPOINT_HERE'
TOPIC_NAME    = 'raspberry-pi-cloud/mqtt-bridge'


camera = VideoCapture(CAMERA_INDEX)

session = Session(
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

s3     = session.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

client = AWSIoTMQTTClient(CLIENT_ID)
client.configureEndpoint(MQTT_ENDPOINT, 8883)
client.configureCredentials('root-ca.crt', 'private.pem.key', 'certificate.pem.crt')
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.connect()

wiringPiSetupGpio()


# 独自命令の定義
# =============================================================================
def make_hash(n=4):
    return ''.join([ choice(ascii_letters + digits) for _ in xrange(n) ])


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


# メインループ
# =============================================================================
while True:
    image_name = make_filename('image', 'jpg')

    s3_image = bucket.Object(image_name)
    s3_image.put(
        ACL='public-read',
        Body=get_image(),
        ContentType='image/jpg'
    )


    sensor_json_name = make_filename('sensor', 'json')

    s3_sensor_json = bucket.Object(sensor_json_name)
    s3_sensor_json.put(
        ACL='public-read',
        Body=get_sensor_json(),
        ContentEncoding='utf-8',
        ContentType='application/json'
    )


    mqtt_message = dumps({
        'sender': CLIENT_ID,
        'data': {
            'image': image_name,
            'sensor': sensor_json_name
        }
    })

    client.publish(TOPIC_NAME, mqtt_message, 1)


    time.sleep(5)
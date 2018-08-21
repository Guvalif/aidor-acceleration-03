# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


# 外部プログラムの読み込み
# =============================================================================
from json import loads
from time import sleep

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from wiringpi import *


# 定数定義・初期化処理
# =============================================================================
CLIENT_ID     = 'raspberry-pi-receiver'
HOST_ID       = 'raspberry-pi-cloud-gui'
MQTT_ENDPOINT = 'PUT_YOUR_MQTT_ENDPOINT_HERE'
TOPIC_NAME    = 'raspberry-pi-cloud/mqtt-bridge'

SERVO_PIN = 18


client = AWSIoTMQTTClient(CLIENT_ID)
client.configureEndpoint(MQTT_ENDPOINT, 8883)
client.configureCredentials('root-ca.crt', 'private.pem.key', 'certificate.pem.crt')
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)
client.connect()

wiringPiSetupGpio()
pinMode(SERVO_PIN, PWM_OUTPUT)
pwmSetMode(PWM_MODE_MS)
pwmSetRange(1024)
pwmSetClock(375)


# 独自命令の定義
# =============================================================================
def mqtt_callback(client, userdata, message):
    message_json = loads(message.payload)

    if message_json['sender'] == HOST_ID:
        pwm = message_json['data']

        pwmWrite(SERVO_PIN, max(min(pwm, 123), 26))


# メインループ
# =============================================================================
client.subscribe(TOPIC_NAME, 1, mqtt_callback)

while True: sleep(1)
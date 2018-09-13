# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


# AWSのリージョン
# =============================================================================
REGION_NAME = 'ap-northeast-1'


# AWS S3の認証情報 (IAM: raspberry-pi-cloud-s3)
# =============================================================================
S3_BUCKET_NAME       = 'raspberry-pi-cloud-NN'
S3_ACCESS_KEY_ID     = 'PUT_YOUR_S3_ACCESS_KEY_ID_HERE'
S3_SECRET_ACCESS_KEY = 'PUT_YOUR_S3_SECRET_KEY_HERE'


# AWS IoT Coreの認証情報 (IAM: raspberry-pi-cloud-iot)
# =============================================================================
IOT_ENDPOINT          = 'PUT_YOUR_IOT_ENDPOINT_HERE'
IOT_ACCESS_KEY_ID     = 'PUT_YOUR_IOT_ACCESS_KEY_ID_HERE'
IOT_SECRET_ACCESS_KEY = 'PUT_YOUR_IOT_SECRET_KEY_HERE'
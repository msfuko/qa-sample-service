#http://flask.pocoo.org/docs/0.10/tutorial/setup/


class Config(object):

    DEBUG = True
    TESTING = False
    KIND = 'vsphere'

    #CACHE_DEFAULT_TIMEOUT = 500


class ProductionConfig(Config):

    # host
    HOST = '0.0.0.0'

    # dynamodb
    DYNAMODB_REGION = 'us-west-1'
    CRITERIA_TABLE = 'QAPortal-vSphere-Staging-Criteria'
    RAW_TABLE = 'QAPortal-vSphere-Staging-RawData'
    RESULT_TABLE = 'QAPortal-vSphere-Staging-QAResult'

    # sqs
    SQS_REGION = 'us-west-1'
    SQS_NAME = 'QATaskQueue-vSphere-Staging'
    
    # cache
    # http://pythonhosted.org/Flask-Cache/#configuring-flask-cache
    CACHE_TYPE = 'memcached'
    CACHE_MEMCACHED_SERVERS = ''
    CACHE_MEMCACHED_USERNAME = ''
    CACHE_MEMCACHED_PASSWORD = ''


class DevelopmentConfig(Config):

    # host
    HOST = '127.0.0.1'

    # dynamodb
    DYNAMODB_REGION = 'us-east-1'
    CRITERIA_TABLE = 'QAPortal-vSphere-POC-Criteria'
    RAW_TABLE = 'QAPortal-vSphere-POC-RawData'
    RESULT_TABLE = 'QAPortal-vSphere-POC-QAResult'

    # sqs
    SQS_REGION = 'us-east-1'
    SQS_NAME = 'QATaskQueue-vSphere-POC'
    
    # cache
    CACHE_TYPE = 'simple'


class DevelopmentContainerConfig(DevelopmentConfig):

    # host
    HOST = '0.0.0.0'


class TestConfig(Config):

    TESTING = True
    KIND = 'zenoss'

    # host
    HOST = '0.0.0.0'

    # dynamodb
    DYNAMODB_REGION = 'us-east-1'
    CRITERIA_TABLE = 'test-Criteria'
    RAW_TABLE = 'test-RawData'
    RESULT_TABLE = 'test-QAResult'

    # sqs
    SQS_REGION = 'us-east-1'
    SQS_NAME = 'test-POC'
    
    # cache
    CACHE_TYPE = 'simple'

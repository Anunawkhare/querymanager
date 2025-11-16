import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'queries.db')

    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

    # AI/ML Settings
    CLASSIFIER_MODEL_PATH = os.getenv('CLASSIFIER_MODEL_PATH', 'query_classifier.pkl')
    CLASSIFIER_CONFIDENCE_THRESHOLD = float(os.getenv('CLASSIFIER_CONFIDENCE_THRESHOLD', 0.6))

    # Email Processing
    SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@company.com')
    AUTO_RESPONSE_ENABLED = os.getenv('AUTO_RESPONSE_ENABLED', 'False').lower() == 'true'

    # Teams Configuration
    TEAMS_CONFIG = {
        'support': {
            'name': 'Support Team',
            'email': 'support@company.com',
            'categories': ['question', 'technical', 'general']
        },
        'billing': {
            'name': 'Billing Team',
            'email': 'billing@company.com',
            'categories': ['billing', 'payment', 'refund']
        },
        'complaints': {
            'name': 'Complaints Team',
            'email': 'complaints@company.com',
            'categories': ['complaint', 'urgent']
        }
    }

    # Priority Settings
    PRIORITY_KEYWORDS = {
        'high': ['urgent', 'emergency', 'critical', 'broken', 'not working', 'help immediately', 'down'],
        'medium': ['question', 'query', 'information', 'details', 'how to'],
        'low': ['feedback', 'suggestion', 'when', 'future', 'thank you']
    }

    # Query Categories
    QUERY_CATEGORIES = [
        'question',
        'complaint',
        'billing',
        'technical',
        'feedback',
        'other'
    ]


class DevelopmentConfig(Config):
    """Development specific configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production specific configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing specific configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'test_queries.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    return config[config_name]()
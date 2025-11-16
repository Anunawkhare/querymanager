"""
Query Management System Backend Package
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'Unified system for managing audience queries with AI-powered categorization'

# Import main components for easier access
from .app import app
from .database import init_db, get_db_connection
from .classifier import QueryClassifier
from .email_parser import EmailParser, SampleQueryGenerator

__all__ = [
    'app',
    'init_db',
    'get_db_connection',
    'QueryClassifier',
    'EmailParser',
    'SampleQueryGenerator'
]
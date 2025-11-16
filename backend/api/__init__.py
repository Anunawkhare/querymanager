"""
API package for Query Management System
"""

from .queries import queries_bp
from .analytics import analytics_bp

# List all available API blueprints
__all__ = ['queries_bp', 'analytics_bp']

# API version
API_VERSION = '1.0.0'

# API documentation
API_DOCS = {
    'queries': {
        'GET /api/queries': 'Get all queries with optional filtering',
        'POST /api/queries': 'Create a new query',
        'PUT /api/queries/<id>': 'Update a query',
        'GET /api/queries/stats': 'Get query statistics'
    },
    'analytics': {
        'GET /api/analytics/response-times': 'Get average response times',
        'GET /api/analytics/team-performance': 'Get team performance metrics'
    }
}
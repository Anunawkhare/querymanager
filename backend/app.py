from flask import Flask, jsonify
from flask_cors import CORS
from backend.database import init_db
from backend.api.queries import queries_bp
from backend.api.analytics import analytics_bp
from backend.email_parser import SampleQueryGenerator
from config.settings import get_config
from datetime import datetime
import sqlite3

# Get configuration
config = get_config()

app = Flask(__name__)
app.config.from_object(config)

# Enable CORS
CORS(app, origins=config.CORS_ORIGINS)

# Register blueprints
app.register_blueprint(queries_bp, url_prefix='/api')
app.register_blueprint(analytics_bp, url_prefix='/api')


# Initialize database
@app.before_first_request
def initialize():
    init_db()

    # Add sample data if no queries exist
    conn = sqlite3.connect(config.DATABASE_URL)
    count = conn.execute('SELECT COUNT(*) FROM queries').fetchone()[0]
    conn.close()

    if count == 0:
        add_sample_data()


def add_sample_data():
    from backend.classifier import QueryClassifier
    classifier = QueryClassifier()

    sample_queries = SampleQueryGenerator.generate_sample_queries()
    conn = sqlite3.connect(config.DATABASE_URL)

    for query_data in sample_queries:
        category, confidence = classifier.categorize_query(query_data['content'])
        priority = classifier.determine_priority(query_data['content'], category)
        assigned_to = classifier.assign_to_team(category, priority)

        conn.execute('''
            INSERT INTO queries (source, customer_email, subject, content, category, priority, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            query_data['source'],
            query_data['customer_email'],
            query_data['subject'],
            query_data['content'],
            category,
            priority,
            assigned_to,
            query_data['created_at']
        ))

    conn.commit()
    conn.close()
    print("✅ Sample data added!")


@app.route('/')
def home():
    return jsonify({
        "message": "Query Management API is running!",
        "version": "1.0.0",
        "environment": app.config.get('ENV', 'development'),
        "endpoints": {
            "queries": "/api/queries",
            "analytics": "/api/analytics",
            "stats": "/api/queries/stats"
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "classifier": "ready"
    })


@app.route('/api/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint"""
    from backend.api import API_DOCS
    return jsonify(API_DOCS)


if __name__ == '__main__':
    print("🚀 Starting Query Management System...")
    print(f"📧 API: http://localhost:{config.API_PORT}")
    print("📊 Dashboard: Open frontend/index.html in your browser")
    print(f"🔧 Environment: {app.config.get('ENV', 'development')}")

    app.run(
        debug=config.DEBUG,
        host=config.API_HOST,
        port=config.API_PORT
    )
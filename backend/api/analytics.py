from flask import Blueprint, jsonify
from backend.database import get_db_connection
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics/response-times', methods=['GET'])
def get_response_times():
    conn = get_db_connection()

    # Calculate average response time (simplified)
    queries_with_responses = conn.execute('''
        SELECT q.id, q.created_at, MIN(r.created_at) as first_response
        FROM queries q
        JOIN responses r ON q.id = r.query_id
        GROUP BY q.id
    ''').fetchall()

    total_response_time = 0
    count = 0

    for query in queries_with_responses:
        query_time = datetime.fromisoformat(query['created_at'])
        response_time = datetime.fromisoformat(query['first_response'])
        total_response_time += (response_time - query_time).total_seconds() / 3600  # hours
        count += 1

    avg_response_time = total_response_time / count if count > 0 else 0

    conn.close()

    return jsonify({
        'average_response_time_hours': round(avg_response_time, 2),
        'queries_with_responses': count
    })


@analytics_bp.route('/analytics/team-performance', methods=['GET'])
def get_team_performance():
    conn = get_db_connection()

    team_stats = conn.execute('''
        SELECT assigned_to, 
               COUNT(*) as total_queries,
               SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved_queries
        FROM queries
        GROUP BY assigned_to
    ''').fetchall()

    conn.close()

    performance = {}
    for stat in team_stats:
        resolution_rate = (stat['resolved_queries'] / stat['total_queries']) * 100 if stat['total_queries'] > 0 else 0
        performance[stat['assigned_to']] = {
            'total_queries': stat['total_queries'],
            'resolved_queries': stat['resolved_queries'],
            'resolution_rate': round(resolution_rate, 2)
        }

    return jsonify(performance)
from flask import Blueprint, request, jsonify
from backend.database import get_db_connection
from backend.classifier import QueryClassifier
from backend.email_parser import EmailParser
from backend.models.schemas import QuerySchema, CreateQueryRequest, UpdateQueryRequest
from datetime import datetime
import sqlite3

queries_bp = Blueprint('queries', __name__)
classifier = QueryClassifier()


@queries_bp.route('/queries', methods=['GET'])
def get_queries():
    """Get all queries with optional filtering"""
    try:
        status = request.args.get('status', 'all')
        category = request.args.get('category', 'all')
        priority = request.args.get('priority', 'all')
        limit = int(request.args.get('limit', 100))

        conn = get_db_connection()

        query = "SELECT * FROM queries WHERE 1=1"
        params = []

        if status != 'all':
            query += " AND status = ?"
            params.append(status)

        if category != 'all':
            query += " AND category = ?"
            params.append(category)

        if priority != 'all':
            query += " AND priority = ?"
            params.append(priority)

        query += " ORDER BY priority DESC, created_at DESC LIMIT ?"
        params.append(limit)

        queries = conn.execute(query, params).fetchall()
        conn.close()

        # Convert to schema format
        queries_list = [QuerySchema.to_dict(query) for query in queries]

        return jsonify(queries_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queries_bp.route('/queries', methods=['POST'])
def create_query():
    """Create a new query"""
    try:
        data = request.get_json()

        # Validate request data
        create_request = CreateQueryRequest(data)
        create_request.validate()

        processed_data = create_request.to_dict()

        # Parse email if source is email
        if processed_data.get('source') == 'email' and 'raw_content' in processed_data:
            subject, content = EmailParser.parse_email_content(processed_data['raw_content'])
            processed_data['subject'] = subject
            processed_data['content'] = content
            processed_data['customer_email'] = EmailParser.extract_email_address(processed_data['raw_content'])

        # Classify query using AI
        category, confidence = classifier.categorize_query(processed_data['content'])
        priority = classifier.determine_priority(processed_data['content'], category)
        assigned_to = classifier.assign_to_team(category, priority)

        conn = get_db_connection()

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO queries (source, customer_email, subject, content, category, priority, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            processed_data.get('source', 'web'),
            processed_data.get('customer_email', 'unknown@example.com'),
            processed_data.get('subject', 'No Subject'),
            processed_data.get('content', ''),
            category,
            priority,
            assigned_to
        ))

        query_id = cursor.lastrowid
        conn.commit()

        # Get the created query
        new_query = conn.execute('SELECT * FROM queries WHERE id = ?', (query_id,)).fetchone()
        conn.close()

        return jsonify(QuerySchema.to_dict(new_query)), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@queries_bp.route('/queries/<int:query_id>', methods=['PUT'])
def update_query(query_id):
    """Update a query"""
    try:
        data = request.get_json()

        # Validate update data
        update_request = UpdateQueryRequest(data)
        update_request.validate()

        update_data = update_request.to_dict()

        if not update_data:
            return jsonify({'error': 'No valid fields to update'}), 400

        conn = get_db_connection()

        # Build update query
        update_fields = []
        params = []

        for field, value in update_data.items():
            update_fields.append(f"{field} = ?")
            params.append(value)

        update_fields.append("updated_at = ?")
        params.append(datetime.now().isoformat())

        params.append(query_id)

        conn.execute(f'''
            UPDATE queries 
            SET {', '.join(update_fields)}
            WHERE id = ?
        ''', params)

        conn.commit()

        updated_query = conn.execute('SELECT * FROM queries WHERE id = ?', (query_id,)).fetchone()
        conn.close()

        if not updated_query:
            return jsonify({'error': 'Query not found'}), 404

        return jsonify(QuerySchema.to_dict(updated_query))

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queries_bp.route('/queries/stats', methods=['GET'])
def get_query_stats():
    """Get query statistics"""
    try:
        from backend.models.schemas import AnalyticsSchema

        conn = get_db_connection()

        # Total queries
        total = conn.execute('SELECT COUNT(*) FROM queries').fetchone()[0]

        # By status
        status_stats = conn.execute('''
            SELECT status, COUNT(*) as count 
            FROM queries 
            GROUP BY status
        ''').fetchall()

        # By category
        category_stats = conn.execute('''
            SELECT category, COUNT(*) as count 
            FROM queries 
            GROUP BY category
        ''').fetchall()

        # By priority
        priority_stats = conn.execute('''
            SELECT priority, COUNT(*) as count 
            FROM queries 
            GROUP BY priority
        ''').fetchall()

        conn.close()

        # Format statistics
        by_status = {stat['status']: stat['count'] for stat in status_stats}
        by_category = {stat['category']: stat['count'] for stat in category_stats}
        by_priority = {f"priority_{stat['priority']}": stat['count'] for stat in priority_stats}

        stats = AnalyticsSchema.query_stats(total, by_status, by_category, by_priority)

        return jsonify(stats)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queries_bp.route('/queries/<int:query_id>', methods=['GET'])
def get_query(query_id):
    """Get a specific query by ID"""
    try:
        conn = get_db_connection()

        query = conn.execute('SELECT * FROM queries WHERE id = ?', (query_id,)).fetchone()
        conn.close()

        if not query:
            return jsonify({'error': 'Query not found'}), 404

        return jsonify(QuerySchema.to_dict(query))

    except Exception as e:
        return jsonify({'error': str(e)}), 500
from datetime import datetime
from typing import Optional, List, Dict, Any


class QuerySchema:
    """Schema for query data"""

    @staticmethod
    def to_dict(query_row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        return {
            'id': query_row['id'],
            'source': query_row['source'],
            'customer_email': query_row['customer_email'],
            'subject': query_row['subject'],
            'content': query_row['content'],
            'category': query_row['category'],
            'priority': query_row['priority'],
            'status': query_row['status'],
            'assigned_to': query_row['assigned_to'],
            'created_at': query_row['created_at'],
            'updated_at': query_row['updated_at']
        }

    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize query creation data"""
        required_fields = ['source', 'content']

        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")

        return {
            'source': data.get('source', 'web'),
            'customer_email': data.get('customer_email', 'unknown@example.com'),
            'subject': data.get('subject', 'No Subject'),
            'content': data.get('content', ''),
            'raw_content': data.get('raw_content', '')
        }


class TeamSchema:
    """Schema for team data"""

    @staticmethod
    def to_dict(team_row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        return {
            'id': team_row['id'],
            'name': team_row['name'],
            'email': team_row['email'],
            'categories': team_row['categories'],
            'is_active': bool(team_row['is_active'])
        }


class ResponseSchema:
    """Schema for response data"""

    @staticmethod
    def to_dict(response_row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        return {
            'id': response_row['id'],
            'query_id': response_row['query_id'],
            'agent_id': response_row['agent_id'],
            'response_text': response_row['response_text'],
            'created_at': response_row['created_at']
        }


class AnalyticsSchema:
    """Schema for analytics data"""

    @staticmethod
    def query_stats(total: int, by_status: Dict, by_category: Dict, by_priority: Dict) -> Dict[str, Any]:
        """Format query statistics"""
        return {
            'total_queries': total,
            'by_status': by_status,
            'by_category': by_category,
            'by_priority': by_priority,
            'timestamp': datetime.now().isoformat()
        }

    @staticmethod
    def response_times(avg_hours: float, query_count: int) -> Dict[str, Any]:
        """Format response time analytics"""
        return {
            'average_response_time_hours': avg_hours,
            'queries_with_responses': query_count,
            'timestamp': datetime.now().isoformat()
        }

    @staticmethod
    def team_performance(team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format team performance data"""
        return {
            'teams': team_data,
            'timestamp': datetime.now().isoformat()
        }


# Validation schemas for API requests
class CreateQueryRequest:
    def __init__(self, data: Dict[str, Any]):
        self.source = data.get('source', 'web')
        self.customer_email = data.get('customer_email', 'unknown@example.com')
        self.subject = data.get('subject', 'No Subject')
        self.content = data.get('content', '')
        self.raw_content = data.get('raw_content', '')

    def validate(self) -> bool:
        """Validate the request data"""
        if not self.content.strip():
            raise ValueError("Content cannot be empty")
        if self.source not in ['email', 'social', 'chat', 'web']:
            raise ValueError("Invalid source")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for processing"""
        return {
            'source': self.source,
            'customer_email': self.customer_email,
            'subject': self.subject,
            'content': self.content,
            'raw_content': self.raw_content
        }


class UpdateQueryRequest:
    def __init__(self, data: Dict[str, Any]):
        self.status = data.get('status')
        self.assigned_to = data.get('assigned_to')
        self.priority = data.get('priority')

    def validate(self) -> bool:
        """Validate update data"""
        valid_statuses = ['new', 'in-progress', 'resolved', 'closed']
        if self.status and self.status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")

        if self.priority and self.priority not in [1, 2, 3]:
            raise ValueError("Priority must be 1, 2, or 3")

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for processing"""
        update_data = {}
        if self.status:
            update_data['status'] = self.status
        if self.assigned_to:
            update_data['assigned_to'] = self.assigned_to
        if self.priority:
            update_data['priority'] = self.priority

        return update_data
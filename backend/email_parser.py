import re
from datetime import datetime


class EmailParser:
    @staticmethod
    def parse_email_content(raw_content):
        """Parse email content to extract subject and body"""
        lines = raw_content.split('\n')
        subject = ""
        body = ""

        for i, line in enumerate(lines):
            if line.lower().startswith('subject:'):
                subject = line[8:].strip()
            elif line.strip() and not line.lower().startswith(('from:', 'to:', 'date:')):
                body += line + '\n'

        # If no subject found, use first line
        if not subject and lines:
            subject = lines[0].strip()[:100]

        # If no body, use everything
        if not body.strip():
            body = raw_content

        return subject, body.strip()

    @staticmethod
    def extract_email_address(text):
        """Extract email address from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else "unknown@example.com"


class SampleQueryGenerator:
    @staticmethod
    def generate_sample_queries():
        """Generate sample queries for testing"""
        sample_queries = [
            {
                'source': 'email',
                'customer_email': 'customer1@example.com',
                'subject': 'Urgent: Website not loading',
                'content': 'Hello, your website is completely down and not loading. This is affecting our business operations urgently. Please fix immediately.',
                'created_at': datetime.now().isoformat()
            },
            {
                'source': 'email',
                'customer_email': 'customer2@example.com',
                'subject': 'Billing inquiry',
                'content': 'I have a question about my recent invoice. Can you explain the charges from last month?',
                'created_at': datetime.now().isoformat()
            },
            {
                'source': 'social',
                'customer_email': 'user@twitter.com',
                'subject': 'Feature request',
                'content': 'Love your product! Would be great to have dark mode in the next update.',
                'created_at': datetime.now().isoformat()
            }
        ]
        return sample_queries
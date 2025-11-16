import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import re


class QueryClassifier:
    def __init__(self):
        self.model = None
        self.categories = ['question', 'complaint', 'billing', 'technical', 'feedback', 'other']
        self.priority_keywords = {
            'high': ['urgent', 'emergency', 'critical', 'broken', 'not working', 'help immediately'],
            'medium': ['question', 'query', 'information', 'details'],
            'low': ['feedback', 'suggestion', 'when', 'future']
        }

    def train_model(self):
        print("Training query classification model...")

        # Training data for query categorization
        training_data = [
            ("how do I reset my password login issue cannot access", "technical"),
            ("billing invoice payment charge refund money", "billing"),
            ("complaint bad service terrible experience angry", "complaint"),
            ("question information how to when can where is", "question"),
            ("feedback suggestion improve love great awesome", "feedback"),
            ("hello hi thanks thank you regards", "other")
        ]

        texts, labels = zip(*training_data)

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('clf', MultinomialNB())
        ])

        self.model.fit(texts, labels)
        joblib.dump(self.model, 'query_classifier.pkl')
        print("Model trained and saved!")

    def load_model(self):
        try:
            self.model = joblib.load('query_classifier.pkl')
        except:
            print("No trained model found. Training new model...")
            self.train_model()

    def categorize_query(self, text):
        if not self.model:
            self.load_model()

        # Clean text
        text = re.sub(r'[^\w\s]', '', text.lower())

        try:
            category = self.model.predict([text])[0]
            confidence = max(self.model.predict_proba([text])[0])
            return category, confidence
        except:
            return "other", 0.5

    def determine_priority(self, text, category):
        text_lower = text.lower()
        priority_score = 1  # Default: low priority

        # High priority indicators
        if any(word in text_lower for word in self.priority_keywords['high']):
            priority_score = 3
        elif category == 'complaint':
            priority_score = 3
        elif any(word in text_lower for word in self.priority_keywords['medium']):
            priority_score = 2
        elif 'urgent' in text_lower or 'emergency' in text_lower:
            priority_score = 3

        return priority_score

    def assign_to_team(self, category, priority):
        conn = get_db_connection()
        teams = conn.execute('SELECT * FROM teams WHERE is_active = 1').fetchall()
        conn.close()

        for team in teams:
            team_categories = eval(team['categories'])
            if category in team_categories:
                return team['name']

        # Default assignment based on priority
        if priority == 3:
            return "Complaints Team"
        elif category == 'billing':
            return "Billing Team"
        else:
            return "Support Team"


def get_db_connection():
    import sqlite3
    conn = sqlite3.connect('queries.db')
    conn.row_factory = sqlite3.Row
    return conn
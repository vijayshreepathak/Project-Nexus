import streamlit as st
import pandas as pd
import numpy as np
import json
import sqlite3
import hashlib
import re
import random
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
import requests
from textblob import TextBlob
from dotenv import load_dotenv
import os
from PIL import Image
import io

load_dotenv()
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_TOKEN')}"}

# Safe imports with fallbacks
try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

try:
    import validators
    HAS_VALIDATORS = True
except ImportError:
    HAS_VALIDATORS = False

# Configure page
st.set_page_config(
    page_title="Project Nexus - Walmart Sparkathon",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced logging
logging.basicConfig(filename='nexus_audit.log', level=logging.INFO, 
                   format='%(asctime)s %(levelname)s %(message)s')

def log_action(user, action, details=None):
    logging.info(f"User: {user}, Action: {action}, Details: {details}")

# Password utilities
def hash_password(password):
    if HAS_BCRYPT:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    if HAS_BCRYPT:
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    else:
        return hashlib.sha256(password.encode()).hexdigest() == hashed

def is_valid_email(email):
    if HAS_VALIDATORS:
        return validators.email(email)
    else:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

# Enhanced Session State Management
def initialize_session_state():
    defaults = {
        'logged_in': False,
        'username': "",
        'user_role': "",
        'user_profile': {},
        'aura_state': "Balanced",
        'current_intent': "General Shopping",
        'stress_level': 5,
        'energy_level': 7,
        'sustainability_preference': False,
        'cart': [],
        'wishlist': [],
        'purchase_history': [],
        'family_members': ["Sam", "Taylor"],
        'friends': ["Alex", "Jamie", "Chris"],
        'community_trends': ["Plant-based snacks", "Local honey", "Sustainable packaging"],
        'weather': "Sunny",
        'location': "Bentonville, AR",
        'calendar_events': ["Friend's Birthday", "Weekend BBQ", "Gym Session"],
        'biometric_data': {'heart_rate': 72, 'sleep_quality': 8.5, 'activity_level': 6},
        'voice_enabled': False,
        'ar_enabled': False,
        'recommendations': [],
        'eco_score': 85,
        'carbon_footprint': 20,
        'prediction_accuracy': 92,
        'last_active': datetime.now(),
        'theme_preference': "auto",
        'notification_preferences': {"email": True, "push": True, "sms": False},
        'shopping_patterns': {},
        'social_influence_score': 7.2,
        'personalization_level': 8.5,
        'voice_command': "I need something cozy for this weekend's weather",
        'show_register': False,
        'user_id': None,
        'session_token': None,
        'preferred_language': "en",
        'accessibility_mode': False,
        'dark_mode': True,
        'tutorial_completed': False,
        'privacy_settings': {"data_sharing": True, "analytics": True, "marketing": False},
        'loyalty_points': 1250,
        'membership_tier': "Gold",
        'saved_addresses': [],
        'payment_methods': [],
        'order_history': [],
        'browsing_history': [],
        'search_history': [],
        'favorite_brands': ["Organic Valley", "Great Value", "Mainstays"],
        'dietary_restrictions': [],
        'allergies': [],
        'health_goals': ["Weight Management", "Heart Health"],
        'fitness_data': {"steps": 8450, "calories": 2100, "water": 6},
        'mood_tracking': {"happiness": 7, "energy": 6, "focus": 8},
        'social_connections': {"facebook": False, "instagram": False, "twitter": False},
        'ai_preferences': {"prediction_level": "high", "personalization": "maximum", "privacy": "balanced"},
        'shopping_behavior': {"impulse_buyer": False, "research_heavy": True, "price_sensitive": True},
        'environmental_commitment': {"carbon_conscious": True, "waste_reduction": True, "local_sourcing": True}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Database Setup
def get_db_connection():
    conn = sqlite3.connect('nexus_sparkathon.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_comprehensive_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'user',
        profile_data TEXT,
        preferences TEXT,
        created_date TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT,
        is_active INTEGER DEFAULT 1,
        failed_attempts INTEGER DEFAULT 0
    )''')
    
    # Products table
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        eco_score INTEGER,
        carbon_footprint REAL,
        sustainability_rating TEXT,
        description TEXT,
        image_url TEXT,
        stock_quantity INTEGER,
        popularity_score REAL
    )''')
    
    # User interactions table
    c.execute('''CREATE TABLE IF NOT EXISTS user_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        interaction_type TEXT,
        timestamp TEXT,
        context_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    
    # Recommendations table
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        recommendation_type TEXT,
        confidence_score REAL,
        context TEXT,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )''')
    
    # Shopping sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        session_start TEXT,
        session_end TEXT,
        items_viewed INTEGER,
        items_purchased INTEGER,
        total_amount REAL,
        aura_state TEXT,
        context_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Initialize admin user
    c.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if c.fetchone()[0] == 0:
        admin_password = hash_password("admin123")
        c.execute('''INSERT INTO users (username, password, email, role, is_active) 
                     VALUES (?, ?, ?, ?, ?)''',
                  ('admin', admin_password, 'admin@walmart.com', 'admin', 1))
    
    # Initialize sample products
    sample_products = [
        ("Organic Quinoa", "Health Food", 12.99, 9, 1.2, "A+", "Premium organic quinoa", "", 100, 8.5),
        ("Bluetooth Speaker", "Electronics", 79.99, 6, 3.5, "B", "Portable wireless speaker", "", 50, 7.8),
        ("Bamboo Toothbrush", "Sustainability", 4.99, 10, 0.1, "A+", "Eco-friendly bamboo toothbrush", "", 200, 9.2),
        ("Greek Yogurt", "Dairy", 5.49, 7, 0.8, "A", "High-protein Greek yogurt", "", 150, 8.8),
        ("Reusable Water Bottle", "Sustainability", 24.99, 9, 0.5, "A+", "Stainless steel water bottle", "", 75, 8.9),
        ("Protein Powder", "Fitness", 34.99, 6, 2.1, "B+", "Whey protein powder", "", 60, 7.5),
        ("LED Desk Lamp", "Home", 45.99, 8, 1.8, "A", "Energy-efficient LED lamp", "", 40, 8.1),
        ("Organic Honey", "Food", 8.99, 9, 0.3, "A+", "Local organic honey", "", 120, 9.0),
        ("Yoga Mat", "Fitness", 29.99, 7, 1.5, "B+", "Non-slip yoga mat", "", 90, 8.3),
        ("Plant-Based Milk", "Dairy Alternative", 4.99, 8, 0.6, "A", "Oat milk alternative", "", 180, 8.7),
        ("Smart Watch", "Electronics", 199.99, 5, 4.2, "B-", "Fitness tracking smartwatch", "", 30, 9.1),
        ("Organic Apples", "Produce", 3.99, 10, 0.2, "A+", "Fresh organic apples", "", 500, 8.9),
        ("Eco Laundry Detergent", "Sustainability", 15.99, 9, 0.8, "A+", "Plant-based laundry detergent", "", 80, 8.4),
        ("Wireless Headphones", "Electronics", 129.99, 4, 3.8, "C+", "Noise-canceling headphones", "", 25, 8.7),
        ("Meditation Cushion", "Wellness", 39.99, 8, 1.0, "A", "Comfortable meditation cushion", "", 60, 7.9),
        ("Solar Phone Charger", "Sustainability", 49.99, 10, 0.3, "A+", "Portable solar charger", "", 40, 8.6),
        ("Organic Coffee Beans", "Food", 14.99, 9, 1.1, "A+", "Fair trade organic coffee", "", 120, 9.3),
        ("Ergonomic Mouse Pad", "Office", 19.99, 6, 1.4, "B", "Wrist-support mouse pad", "", 150, 7.8),
        ("Reusable Food Wraps", "Sustainability", 12.99, 10, 0.1, "A+", "Beeswax food wraps", "", 200, 8.8),
        ("Air Purifying Plant", "Home", 22.99, 10, 0.0, "A+", "Snake plant for clean air", "", 85, 8.5)
    ]
    
    for product in sample_products:
        c.execute("SELECT COUNT(*) FROM products WHERE name = ?", (product[0],))
        if c.fetchone()[0] == 0:
            c.execute('''INSERT INTO products (name, category, price, eco_score, carbon_footprint, 
                         sustainability_rating, description, image_url, stock_quantity, popularity_score) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', product)
    
    conn.commit()
    conn.close()

init_comprehensive_db()

# Authentication functions
def authenticate_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
    user = c.fetchone()
    if user:
        stored_password = user[2]
        if check_password(password, stored_password):
            c.execute('UPDATE users SET last_login = ?, failed_attempts = 0 WHERE username = ?', 
                     (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
            conn.commit()
            conn.close()
            return user
        else:
            c.execute('UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?', (username,))
            conn.commit()
    conn.close()
    return None

def create_user(username, password, email, role='user'):
    conn = get_db_connection()
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute('''INSERT INTO users (username, password, email, role, is_active) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (username, hashed_password, email, role, 1))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Enhanced CSS with Walmart branding
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 30%, #0f172a 100%) !important;
        color: #f8fafc !important;
    }
    
    .main { background: transparent !important; }
    
    .walmart-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0071ce 0%, #ffe600 50%, #0071ce 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 40px rgba(0, 113, 206, 0.3);
        margin-bottom: 2rem;
        animation: pulse-glow 3s ease-in-out infinite alternate;
        letter-spacing: 2px;
    }
    
    @keyframes pulse-glow {
        from { 
            text-shadow: 0 0 20px rgba(0, 113, 206, 0.3), 0 0 30px rgba(255, 230, 0, 0.2);
            transform: scale(1);
        }
        to { 
            text-shadow: 0 0 30px rgba(0, 113, 206, 0.5), 0 0 40px rgba(255, 230, 0, 0.3);
            transform: scale(1.02);
        }
    }
    
    .nexus-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(0, 113, 206, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 113, 206, 0.15);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .nexus-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 230, 0, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .nexus-card:hover::before {
        left: 100%;
    }
    
    .nexus-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 113, 206, 0.25);
        border-color: rgba(255, 230, 0, 0.5);
    }
    
    .aura-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem;
        animation: aura-pulse 2s ease-in-out infinite;
    }
    
    @keyframes aura-pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
    }
    
    .aura-balanced { background: linear-gradient(45deg, #10b981, #3b82f6); color: white; }
    .aura-stressed { background: linear-gradient(45deg, #ef4444, #f97316); color: white; }
    .aura-energetic { background: linear-gradient(45deg, #eab308, #f59e0b); color: white; }
    .aura-eco { background: linear-gradient(45deg, #22c55e, #16a34a); color: white; }
    .aura-calm { background: linear-gradient(45deg, #10b981, #059669); color: white; }
    .aura-cozy { background: linear-gradient(45deg, #8b5cf6, #7c3aed); color: white; }
    .aura-vibrant { background: linear-gradient(45deg, #f59e0b, #eab308); color: white; }
    .aura-low-energy { background: linear-gradient(45deg, #6b7280, #4b5563); color: white; }
    .aura-restful { background: linear-gradient(45deg, #6366f1, #4f46e5); color: white; }
    .aura-productive { background: linear-gradient(45deg, #0071ce, #0284c7); color: white; }
    .aura-relaxed { background: linear-gradient(45deg, #10b981, #059669); color: white; }
    
    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 113, 206, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0071ce;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .product-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .product-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 113, 206, 0.3);
        border-color: rgba(255, 230, 0, 0.5);
    }
    
    .sustainability-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .eco-excellent { background: #22c55e; color: white; }
    .eco-good { background: #3b82f6; color: white; }
    .eco-fair { background: #f59e0b; color: white; }
    .eco-poor { background: #ef4444; color: white; }
    
    .stButton>button {
        background: linear-gradient(135deg, #0071ce 0%, #ffe600 100%);
        color: #1e293b;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 113, 206, 0.3);
        width: 100%;
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 113, 206, 0.4);
        background: linear-gradient(135deg, #ffe600 0%, #0071ce 100%);
    }
    
    .voice-indicator {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(45deg, #0071ce, #ffe600);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        cursor: pointer;
        animation: voice-pulse 2s infinite;
        z-index: 1000;
    }
    
    @keyframes voice-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .prediction-timeline {
        position: relative;
        padding: 2rem 0;
    }
    
    .prediction-item {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #0071ce;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        position: relative;
    }
    
    .prediction-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 50%;
        transform: translateY(-50%);
        width: 12px;
        height: 12px;
        background: #0071ce;
        border-radius: 50%;
    }
    
    .social-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(45deg, #0071ce, #ffe600);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0.2rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .progress-ring {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(#0071ce 0deg, #ffe600 180deg, #0071ce 360deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem auto;
        position: relative;
    }
    
    .progress-ring::before {
        content: '';
        position: absolute;
        width: 90px;
        height: 90px;
        background: #0f172a;
        border-radius: 50%;
    }
    
    .progress-text {
        position: relative;
        z-index: 1;
        font-size: 1.5rem;
        font-weight: 700;
        color: #0071ce;
    }
    
    .notification-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ef4444;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        font-size: 0.7rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .trend-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.2rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .trend-up { background: rgba(34, 197, 94, 0.2); color: #22c55e; }
    .trend-down { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    .trend-stable { background: rgba(156, 163, 175, 0.2); color: #9ca3af; }
    
    @media (max-width: 768px) {
        .walmart-header {
            font-size: 2.5rem;
        }
        .nexus-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .metric-value {
            font-size: 2rem;
        }
    }
    </style>
''', unsafe_allow_html=True)

# Enhanced AI Engine Classes
class AuraEngine:
    def __init__(self):
        self.context_weights = {
            'stress': 0.3,
            'energy': 0.25,
            'weather': 0.15,
            'time': 0.1,
            'location': 0.1,
            'social': 0.1
        }
    
    def calculate_aura(self, user_data):
        stress = user_data.get('stress_level', 5)
        energy = user_data.get('energy_level', 7)
        weather = user_data.get('weather', 'Sunny')
        hour = datetime.now().hour
        
        # Stress-based aura
        if stress > 7:
            return "Stressed", "#ef4444"
        elif stress < 3:
            return "Calm", "#10b981"
        
        # Energy-based aura
        if energy > 8:
            return "Energetic", "#f59e0b"
        elif energy < 3:
            return "Low Energy", "#6b7280"
        
        # Weather influence
        if weather == "Rainy" and stress > 5:
            return "Cozy", "#8b5cf6"
        elif weather == "Sunny" and energy > 6:
            return "Vibrant", "#f59e0b"
        
        # Time-based influence
        if hour < 6 or hour > 22:
            return "Restful", "#6366f1"
        elif 6 <= hour < 12:
            return "Energetic", "#f59e0b"
        elif 12 <= hour < 18:
            return "Productive", "#0071ce"
        else:
            return "Relaxed", "#10b981"
    
    def get_aura_recommendations(self, aura_state):
        recommendations = {
            "Stressed": {
                "categories": ["Wellness", "Relaxation", "Comfort"],
                "products": ["Aromatherapy oils", "Herbal tea", "Stress ball", "Meditation app"],
                "ui_theme": "calm",
                "colors": ["#ef4444", "#f97316"]
            },
            "Energetic": {
                "categories": ["Fitness", "Sports", "Adventure"],
                "products": ["Protein powder", "Workout gear", "Energy drinks", "Sports equipment"],
                "ui_theme": "vibrant",
                "colors": ["#f59e0b", "#eab308"]
            },
            "Calm": {
                "categories": ["Books", "Art", "Music"],
                "products": ["Books", "Art supplies", "Classical music", "Puzzles"],
                "ui_theme": "serene",
                "colors": ["#10b981", "#059669"]
            },
            "Eco": {
                "categories": ["Sustainable", "Organic", "Green"],
                "products": ["Organic foods", "Eco-friendly products", "Reusable items", "Solar products"],
                "ui_theme": "green",
                "colors": ["#22c55e", "#16a34a"]
            },
            "Cozy": {
                "categories": ["Comfort", "Indoor", "Warmth"],
                "products": ["Blankets", "Hot beverages", "Candles", "Indoor plants"],
                "ui_theme": "cozy",
                "colors": ["#8b5cf6", "#7c3aed"]
            },
            "Vibrant": {
                "categories": ["Outdoor", "Active", "Social"],
                "products": ["Outdoor gear", "Party supplies", "Bright clothing", "Social games"],
                "ui_theme": "vibrant",
                "colors": ["#f59e0b", "#eab308"]
            },
            "Low Energy": {
                "categories": ["Energy Boost", "Comfort", "Rest"],
                "products": ["Energy bars", "Coffee", "Comfortable seating", "Sleep aids"],
                "ui_theme": "restful",
                "colors": ["#6b7280", "#4b5563"]
            },
            "Restful": {
                "categories": ["Sleep", "Relaxation", "Night"],
                "products": ["Sleep masks", "Pillows", "Night tea", "Meditation apps"],
                "ui_theme": "night",
                "colors": ["#6366f1", "#4f46e5"]
            },
            "Productive": {
                "categories": ["Work", "Efficiency", "Focus"],
                "products": ["Office supplies", "Productivity tools", "Healthy snacks", "Organizers"],
                "ui_theme": "professional",
                "colors": ["#0071ce", "#0284c7"]
            },
            "Relaxed": {
                "categories": ["Leisure", "Entertainment", "Comfort"],
                "products": ["Entertainment", "Comfort food", "Leisure activities", "Relaxation tools"],
                "ui_theme": "leisure",
                "colors": ["#10b981", "#059669"]
            }
        }
        return recommendations.get(aura_state, recommendations["Calm"])

class PredictiveEngine:
    def __init__(self):
        self.prediction_models = {
            'seasonal': self._seasonal_predictions,
            'behavioral': self._behavioral_predictions,
            'social': self._social_predictions,
            'lifecycle': self._lifecycle_predictions,
            'contextual': self._contextual_predictions,
            'health': self._health_predictions
        }
    
    def _seasonal_predictions(self, user_data):
        current_month = datetime.now().month
        seasonal_needs = {
            12: ["Winter clothes", "Holiday gifts", "Comfort food", "Indoor activities", "Heating supplies"],
            1: ["Fitness equipment", "Healthy food", "Organization tools", "New year supplies", "Winter gear"],
            2: ["Valentine's gifts", "Winter clearance", "Indoor activities", "Heart health products", "Love-themed items"],
            3: ["Spring cleaning", "Garden supplies", "Allergy relief", "Fresh produce", "Outdoor preparation"],
            4: ["Spring fashion", "Outdoor gear", "Fresh produce", "Easter items", "Allergy medication"],
            5: ["Summer prep", "Sunscreen", "BBQ supplies", "Mother's Day gifts", "Graduation gifts"],
            6: ["Summer clothes", "Travel gear", "Ice cream", "Father's Day gifts", "Outdoor furniture"],
            7: ["Vacation items", "Swimwear", "Cooling products", "Summer sports", "Outdoor entertainment"],
            8: ["Back to school", "Summer clearance", "Prep for fall", "School supplies", "Fall fashion preview"],
            9: ["Fall fashion", "School supplies", "Warm beverages", "Halloween prep", "Comfort foods"],
            10: ["Halloween items", "Autumn decor", "Comfort foods", "Warm clothing", "Seasonal produce"],
            11: ["Thanksgiving prep", "Winter prep", "Holiday planning", "Gratitude gifts", "Warm clothing"]
        }
        return seasonal_needs.get(current_month, [])
    
    def _behavioral_predictions(self, user_data):
        purchase_history = user_data.get('purchase_history', [])
        if not purchase_history:
            return ["Basic necessities", "Popular items", "Trending products"]
        
        # Analyze patterns
        categories = {}
        for item in purchase_history:
            category = item.get('category', 'General')
            categories[category] = categories.get(category, 0) + 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        return [f"More {cat[0]} items" for cat in top_categories]
    
    def _social_predictions(self, user_data):
        calendar_events = user_data.get('calendar_events', [])
        social_predictions = []
        
        for event in calendar_events:
            if 'birthday' in event.lower():
                social_predictions.append("Gift ideas for birthday celebration")
            elif 'party' in event.lower():
                social_predictions.append("Party supplies and decorations")
            elif 'meeting' in event.lower():
                social_predictions.append("Professional attire and accessories")
            elif 'bbq' in event.lower():
                social_predictions.append("BBQ essentials and outdoor dining")
            elif 'gym' in event.lower():
                social_predictions.append("Fitness gear and protein supplements")
        
        return social_predictions or ["Social gathering items"]
    
    def _lifecycle_predictions(self, user_data):
        # Predict based on life stage and patterns
        age = user_data.get('age', 30)
        family_size = len(user_data.get('family_members', []))
        
        if age < 25:
            return ["Tech gadgets", "Fashion items", "Entertainment", "Education supplies", "Social activities"]
        elif age < 35:
            return ["Career items", "Home improvement", "Travel", "Investment tools", "Skill development"]
        elif age < 50:
            return ["Family items", "Health products", "Home essentials", "Children's needs", "Long-term planning"]
        else:
            return ["Comfort items", "Health supplements", "Hobby supplies", "Relaxation tools", "Wellness products"]
    
    def _contextual_predictions(self, user_data):
        weather = user_data.get('weather', 'Sunny')
        location = user_data.get('location', '')
        time_of_day = datetime.now().hour
        
        predictions = []
        
        if weather == "Rainy":
            predictions.extend(["Umbrellas", "Raincoats", "Indoor activities", "Comfort food"])
        elif weather == "Sunny":
            predictions.extend(["Sunscreen", "Outdoor gear", "Cold beverages", "Summer clothing"])
        elif weather == "Snowy":
            predictions.extend(["Winter gear", "Heating supplies", "Hot beverages", "Snow activities"])
        
        if time_of_day < 12:
            predictions.extend(["Breakfast items", "Coffee", "Morning supplements"])
        elif time_of_day < 17:
            predictions.extend(["Lunch options", "Afternoon snacks", "Energy drinks"])
        else:
            predictions.extend(["Dinner ingredients", "Evening relaxation", "Night-time products"])
        
        return predictions
    
    def _health_predictions(self, user_data):
        health_goals = user_data.get('health_goals', [])
        fitness_data = user_data.get('fitness_data', {})
        
        predictions = []
        
        if "Weight Management" in health_goals:
            predictions.extend(["Healthy snacks", "Portion control tools", "Fitness equipment"])
        if "Heart Health" in health_goals:
            predictions.extend(["Heart-healthy foods", "Omega-3 supplements", "Exercise gear"])
        
        if fitness_data.get('steps', 0) < 5000:
            predictions.append("Activity trackers and motivation tools")
        if fitness_data.get('water', 0) < 8:
            predictions.append("Water bottles and hydration reminders")
        
        return predictions
    
    def generate_predictions(self, user_data):
        all_predictions = []
        for model_name, model_func in self.prediction_models.items():
            predictions = model_func(user_data)
            all_predictions.extend(predictions)
        
        # Remove duplicates and return top 15
        unique_predictions = list(set(all_predictions))
        return unique_predictions[:15]

class SustainabilityEngine:
    def __init__(self):
        self.eco_categories = {
            'A+': {'min_score': 9, 'color': '#22c55e', 'label': 'Excellent'},
            'A': {'min_score': 8, 'color': '#3b82f6', 'label': 'Good'},
            'B+': {'min_score': 7, 'color': '#f59e0b', 'label': 'Fair'},
            'B': {'min_score': 6, 'color': '#ef4444', 'label': 'Poor'},
            'C': {'min_score': 0, 'color': '#dc2626', 'label': 'Very Poor'}
        }
    
    def calculate_carbon_footprint(self, cart_items):
        total_footprint = 0
        for item in cart_items:
            # Mock calculation based on product type
            if 'organic' in item.lower():
                total_footprint += 0.5
            elif 'electronics' in item.lower():
                total_footprint += 3.0
            elif 'clothing' in item.lower():
                total_footprint += 2.0
            elif 'meat' in item.lower():
                total_footprint += 4.0
            elif 'dairy' in item.lower():
                total_footprint += 1.5
            elif 'local' in item.lower():
                total_footprint += 0.3
            elif 'plastic' in item.lower():
                total_footprint += 2.5
            else:
                total_footprint += 1.0
        return total_footprint
    
    def get_eco_alternatives(self, product_name):
        alternatives = {
            'plastic bottle': 'Reusable stainless steel bottle',
            'paper towels': 'Reusable cloth towels',
            'regular detergent': 'Eco-friendly detergent',
            'disposable bags': 'Reusable shopping bags',
            'incandescent bulbs': 'LED bulbs',
            'plastic containers': 'Glass storage containers',
            'fast fashion': 'Sustainable clothing brands',
            'conventional produce': 'Organic produce',
            'single-use items': 'Reusable alternatives',
            'synthetic materials': 'Natural materials'
        }
        return alternatives.get(product_name.lower(), f"Eco-friendly {product_name}")
    
    def generate_sustainability_report(self, user_data):
        cart = user_data.get('cart', [])
        carbon_footprint = self.calculate_carbon_footprint(cart)
        
        if carbon_footprint < 5:
            eco_grade = 'A+'
        elif carbon_footprint < 10:
            eco_grade = 'A'
        elif carbon_footprint < 20:
            eco_grade = 'B+'
        elif carbon_footprint < 30:
            eco_grade = 'B'
        else:
            eco_grade = 'C'
        
        return {
            'carbon_footprint': carbon_footprint,
            'eco_grade': eco_grade,
            'eco_score': max(0, 100 - carbon_footprint * 2),
            'recommendations': [
                'Choose organic products when possible',
                'Use reusable bags and containers',
                'Buy local produce to reduce transport emissions',
                'Select energy-efficient appliances',
                'Reduce single-use plastic items',
                'Consider second-hand or refurbished items',
                'Support sustainable brands and certifications'
            ]
        }
    
    def calculate_waste_reduction(self, sustainable_choices):
        # Calculate potential waste reduction based on sustainable choices
        reduction_metrics = {
            'reusable_bags': 365,  # bags per year
            'water_bottle': 156,   # plastic bottles per year
            'food_containers': 200, # disposable containers per year
            'cloth_towels': 52,    # paper towel rolls per year
            'led_bulbs': 10        # incandescent bulbs per year
        }
        
        total_reduction = sum(reduction_metrics.get(choice, 0) for choice in sustainable_choices)
        return total_reduction

# Voice command processing
def process_voice_command(command):
    command = command.lower().strip()
    
    # Cart operations
    if "add" in command and "cart" in command:
        # Extract product name if possible
        if "organic" in command:
            return "I've added organic products to your cart based on your preferences."
        elif "eco" in command or "sustainable" in command:
            return "I've added eco-friendly items to your cart. These choices help reduce your carbon footprint."
        else:
            return "I've added the requested items to your cart. Is there anything else you'd like to add?"
    
    # Search and recommendations
    elif "find" in command or "search" in command:
        if "eco" in command or "sustainable" in command:
            return "Here are some eco-friendly alternatives that match your preferences and reduce environmental impact."
        elif "gift" in command:
            return "Based on your recipient's interests and your budget, here are some thoughtful gift recommendations."
        else:
            return "I found several products matching your search. Here are the top recommendations based on your aura and preferences."
    
    # Trending and community
    elif "trending" in command:
        trends = st.session_state.community_trends
        return f"In your area, the top trending items are: {', '.join(trends[:3])}. These are popular among users with similar preferences."
    
    # Delivery and scheduling
    elif "delivery" in command or "schedule" in command:
        return "I can schedule delivery for tomorrow between 9 AM - 6 PM. Would you like express delivery or standard shipping?"
    
    # Price and budget
    elif "price" in command or "under" in command or "$" in command:
        return "I found several great products within your budget. Here are the top recommendations sorted by value and rating."
    
    # Recommendations based on relationships
    elif "gift" in command or "friend" in command:
        return "Based on your friend's interests and recent activities, I recommend these thoughtful gift options that align with their hobbies."
    
    # Weather-based recommendations
    elif "weather" in command:
        weather = st.session_state.weather
        return f"Given today's {weather.lower()} weather, I recommend these items to keep you comfortable and prepared."
    
    # Health and wellness
    elif "health" in command or "wellness" in command:
        return "Based on your health goals and fitness data, here are some products that can support your wellness journey."
    
    # Sustainability queries
    elif "carbon" in command or "environment" in command:
        return "I can show you the environmental impact of your choices and suggest alternatives to reduce your carbon footprint."
    
    # General assistance
    else:
        return "I understand you're looking for assistance. Let me help you find exactly what you need based on your current aura, preferences, and context."

# Initialize AI engines
aura_engine = AuraEngine()
predictive_engine = PredictiveEngine()
sustainability_engine = SustainabilityEngine()

# Enhanced UI Components
def render_aura_indicator(aura_state, color):
    aura_class = f"aura-{aura_state.lower().replace(' ', '-')}"
    st.markdown(f'''
        <div class="aura-indicator {aura_class}" style="background: {color};">
            🌟 {aura_state} Aura
        </div>
    ''', unsafe_allow_html=True)

def render_metric_card(value, label, color="#0071ce", trend=None):
    trend_indicator = ""
    if trend:
        if trend > 0:
            trend_indicator = f'<span class="trend-indicator trend-up">↗ +{trend}%</span>'
        elif trend < 0:
            trend_indicator = f'<span class="trend-indicator trend-down">↘ {trend}%</span>'
        else:
            trend_indicator = f'<span class="trend-indicator trend-stable">→ {trend}%</span>'
    
    st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value" style="color: {color};">{value}</div>
            <div class="metric-label">{label}</div>
            {trend_indicator}
        </div>
    ''', unsafe_allow_html=True)

def render_product_card(product_name, price, eco_score, description="", in_stock=True):
    if eco_score > 8:
        eco_class = "eco-excellent"
        eco_label = "Excellent"
    elif eco_score > 6:
        eco_class = "eco-good"
        eco_label = "Good"
    elif eco_score > 4:
        eco_class = "eco-fair"
        eco_label = "Fair"
    else:
        eco_class = "eco-poor"
        eco_label = "Poor"
    
    stock_indicator = "✅ In Stock" if in_stock else "❌ Out of Stock"
    stock_color = "#22c55e" if in_stock else "#ef4444"
    
    st.markdown(f'''
        <div class="product-card">
            <h4>{product_name}</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">{description}</p>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                <strong style="color: #0071ce; font-size: 1.2rem;">${price}</strong>
                <div>
                    <span class="sustainability-badge {eco_class}">Eco: {eco_label}</span>
                    <br>
                    <small style="color: {stock_color};">{stock_indicator}</small>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

def render_social_connections(friends, family):
    st.markdown("#### 👥 Social Circle")
    
    # Friends
    friends_html = "".join([
        f'<div class="social-avatar" title="{friend}">{friend[0]}</div>'
        for friend in friends
    ])
    
    # Family
    family_html = "".join([
        f'<div class="social-avatar" title="{member}" style="background: linear-gradient(45deg, #22c55e, #16a34a);">{member[0]}</div>'
        for member in family
    ])
    
    st.markdown(f'''
        <div style="margin: 1rem 0;">
            <p><strong>Friends:</strong> {friends_html}</p>
            <p><strong>Family:</strong> {family_html}</p>
        </div>
    ''', unsafe_allow_html=True)

def render_prediction_timeline(predictions):
    st.markdown("#### 🔮 Predictive Timeline")
    
    for i, prediction in enumerate(predictions):
        days_ahead = i + 1
        confidence = max(85, 95 - i*2)  # Decreasing confidence for future predictions
        
        st.markdown(f'''
            <div class="prediction-item">
                <strong>In {days_ahead} days:</strong> {prediction}
                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                    Confidence: {confidence}% | Based on: Pattern Analysis
                </div>
            </div>
        ''', unsafe_allow_html=True)

def render_notification_center():
    notifications = [
        {"type": "recommendation", "message": "New eco-friendly products match your preferences", "time": "2 min ago"},
        {"type": "delivery", "message": "Your order will arrive tomorrow", "time": "1 hour ago"},
        {"type": "social", "message": "Alex added items to shared shopping list", "time": "3 hours ago"},
        {"type": "sustainability", "message": "You've reduced 5kg CO2 this month!", "time": "1 day ago"}
    ]
    
    st.markdown("#### 🔔 Notifications")
    for notif in notifications:
        icon = "🎯" if notif["type"] == "recommendation" else "📦" if notif["type"] == "delivery" else "👥" if notif["type"] == "social" else "🌱"
        st.markdown(f'''
            <div style="background: rgba(0, 113, 206, 0.1); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
                {icon} <strong>{notif["message"]}</strong>
                <div style="font-size: 0.8rem; color: #94a3b8;">{notif["time"]}</div>
            </div>
        ''', unsafe_allow_html=True)

# Enhanced Authentication UI
def show_enhanced_login():
    st.markdown('<div style="max-width: 500px; margin: 2rem auto; padding: 3rem; background: rgba(15, 23, 42, 0.9); border-radius: 20px; border: 1px solid rgba(0, 113, 206, 0.3);">', unsafe_allow_html=True)
    
    # Walmart logo and branding
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🛒</div>
            <div class="walmart-header" style="font-size: 2.5rem; margin-bottom: 1rem;">
                Project Nexus
            </div>
            <p style="color: #94a3b8; font-size: 1.1rem;">AI-Empathetic Retail Experience</p>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.form("enhanced_login"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
        with col2:
            register_btn = st.form_submit_button("📝 Register", use_container_width=True)
        
        if login_btn:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    st.session_state.user_role = user[4]
                    st.session_state.user_id = user[0]
                    st.success("✅ Welcome to Project Nexus!")
                    log_action(username, "login_success")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.error("❌ Please fill in all fields")
        
        if register_btn:
            st.session_state.show_register = True
            st.rerun()
    
    # Demo credentials
    st.markdown('''
        <div style="margin-top: 2rem; padding: 1rem; background: rgba(0, 113, 206, 0.1); border-radius: 10px;">
            <strong>Demo Credentials:</strong><br>
            Username: <code>admin</code><br>
            Password: <code>admin123</code>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_register_form():
    st.markdown('<div style="max-width: 500px; margin: 2rem auto; padding: 3rem; background: rgba(15, 23, 42, 0.9); border-radius: 20px; border: 1px solid rgba(0, 113, 206, 0.3);">', unsafe_allow_html=True)
    
    st.markdown('''
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📝</div>
            <div class="walmart-header" style="font-size: 2.5rem; margin-bottom: 1rem;">
                Register
            </div>
            <p style="color: #94a3b8; font-size: 1.1rem;">Create Your Account</p>
        </div>
    ''', unsafe_allow_html=True)
    
    with st.form("register_form"):
        new_username = st.text_input("👤 Username", placeholder="Choose a username")
        new_email = st.text_input("📧 Email", placeholder="Enter your email")
        new_password = st.text_input("🔒 Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        col1, col2 = st.columns(2)
        with col1:
            register_btn = st.form_submit_button("✨ Create Account", use_container_width=True)
        with col2:
            back_btn = st.form_submit_button("⬅️ Back to Login", use_container_width=True)
        
        if register_btn:
            if new_username and new_email and new_password and confirm_password:
                if new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                elif not is_valid_email(new_email):
                    st.error("❌ Invalid email address")
                else:
                    if create_user(new_username, new_password, new_email):
                        st.success("✅ Account created successfully! You can now login.")
                        log_action(new_username, "user_registered", f"Email: {new_email}")
                        st.session_state.show_register = False
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Username or email already exists")
            else:
                st.error("❌ Please fill in all fields")
        
        if back_btn:
            st.session_state.show_register = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Application
def main_nexus_app():
    # Header
    st.markdown('''
        <div style="text-align: center; margin-bottom: 3rem;">
            <div class="walmart-header">🌌 Project Nexus</div>
            <p style="font-size: 1.3rem; color: #94a3b8; margin-bottom: 2rem;">
                AI-Empathetic Retail Experience • Walmart Sparkathon 2025
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    # User info bar
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f'''
            <div style="background: rgba(0, 113, 206, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
                <strong>👤 {st.session_state.username}</strong> | 
                <span style="color: #94a3b8;">Role: {st.session_state.user_role.title()}</span> |
                <span style="color: #ffe600;">💎 {st.session_state.membership_tier} Member</span> |
                <span style="color: #22c55e;">🏆 {st.session_state.loyalty_points} Points</span>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh Aura"):
            st.session_state.aura_state = aura_engine.calculate_aura({
                'stress_level': st.session_state.stress_level,
                'energy_level': st.session_state.energy_level,
                'weather': st.session_state.weather
            })[0]
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.rerun()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Jump to Feature", [
        "🏠 Dashboard",
        "🧠 Aura Engine",
        "🛒 Predictive Shopping",
        "🌐 Context Awareness",
        "🌱 Sustainability Hub",
        "👥 Social Commerce",
        "🎯 AR/Voice Interface",
        "🚀 Live Demo",
        "🤖 Fun AI"
    ])
    
    # Current aura display
    current_aura, aura_color = aura_engine.calculate_aura({
        'stress_level': st.session_state.stress_level,
        'energy_level': st.session_state.energy_level,
        'weather': st.session_state.weather
    })
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Current Aura:** {current_aura}")
    render_aura_indicator(current_aura, aura_color)
    
    # Sidebar stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Your Stats**")
    st.sidebar.metric("Eco Score", f"{st.session_state.eco_score}/100")
    st.sidebar.metric("Cart Items", len(st.session_state.cart))
    st.sidebar.metric("Predictions", f"{st.session_state.prediction_accuracy}%")
    
    # Quick actions in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("**⚡ Quick Actions**")
    if st.sidebar.button("🛒 View Cart", use_container_width=True):
        st.session_state.show_cart = True
    if st.sidebar.button("🔔 Notifications", use_container_width=True):
        st.session_state.show_notifications = True
    if st.sidebar.button("⚙️ Settings", use_container_width=True):
        st.session_state.show_settings = True
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🧠 Aura Engine":
        show_aura_engine()
    elif page == "🛒 Predictive Shopping":
        show_predictive_engine()
    elif page == "🌐 Context Awareness":
        show_context_awareness()
    elif page == "🌱 Sustainability Hub":
        show_sustainability_hub()
    elif page == "👥 Social Commerce":
        show_social_commerce()
    elif page == "🎯 AR/Voice Interface":
        show_ar_voice_interface()
    elif page == "🚀 Live Demo":
        show_live_demo()
    elif page == "🤖 Fun AI":
        show_fun_ai()

def show_dashboard():
    st.header("🏠 Intelligent Shopping Dashboard")
    
    # Real-time metrics with trends
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("92%", "AI Accuracy", "#22c55e", trend=3)
    with col2:
        render_metric_card(f"{st.session_state.eco_score}", "Eco Score", "#3b82f6", trend=5)
    with col3:
        render_metric_card(f"{len(st.session_state.cart)}", "Cart Items", "#f59e0b")
    with col4:
        render_metric_card("$127", "Predicted Savings", "#8b5cf6", trend=12)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🎯 Personalized Recommendations")
        
        # Get recommendations based on current aura
        current_aura, _ = aura_engine.calculate_aura({
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather
        })
        
        # Dynamic product recommendations based on aura
        if current_aura == "Stressed":
            recommended_products = [
                ("Stress-Relief Tea Blend", 8.99, 8, "Herbal blend for relaxation"),
                ("Aromatherapy Diffuser", 45.99, 8, "Essential oil diffuser"),
                ("Meditation Cushion", 39.99, 8, "Comfortable meditation seat"),
                ("Calming Bath Salts", 12.99, 9, "Lavender-scented bath salts")
            ]
        elif current_aura == "Energetic":
            recommended_products = [
                ("Protein Powder", 29.99, 7, "Plant-based nutrition"),
                ("Wireless Headphones", 129.99, 4, "For workout music"),
                ("Yoga Mat", 29.99, 7, "Non-slip exercise mat"),
                ("Energy Bars", 15.99, 6, "Natural energy boost")
            ]
        else:
            recommended_products = [
                ("Organic Quinoa Bowl", 12.99, 9, "Perfect for your healthy lifestyle"),
                ("Bluetooth Speaker", 79.99, 6, "High-quality audio"),
                ("Bamboo Toothbrush", 4.99, 10, "Eco-friendly dental care"),
                ("Reusable Water Bottle", 24.99, 9, "Stay hydrated sustainably")
            ]
        
        # Display products in grid
        for i in range(0, len(recommended_products), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(recommended_products):
                    product = recommended_products[i + j]
                    with col:
                        render_product_card(*product)
                        if st.button(f"Add to Cart", key=f"add_{i}_{j}"):
                            st.session_state.cart.append(product[0])
                            st.success(f"Added {product[0]} to cart!")
                            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Predictive insights
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🔮 AI Insights")
        
        # Generate and display predictions
        user_data = {
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather,
            'calendar_events': st.session_state.calendar_events,
            'family_members': st.session_state.family_members,
            'health_goals': st.session_state.health_goals,
            'fitness_data': st.session_state.fitness_data
        }
        
        predictions = predictive_engine.generate_predictions(user_data)[:5]
        
        for prediction in predictions:
            st.markdown(f"• **{prediction}** - Based on your patterns and preferences")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🧠 AI Context")
        
        # Current context
        st.markdown(f"**🌤️ Weather:** {st.session_state.weather}")
        st.markdown(f"**📍 Location:** {st.session_state.location}")
        st.markdown(f"**🕐 Time:** {datetime.now().strftime('%I:%M %p')}")
        st.markdown(f"**🎯 Intent:** {st.session_state.current_intent}")
        
        # Biometric data with enhanced visualization
        st.markdown("**💓 Biometric Data:**")
        
        # Stress level with color coding
        stress_color = "#ef4444" if st.session_state.stress_level > 7 else "#f59e0b" if st.session_state.stress_level > 4 else "#22c55e"
        st.markdown(f'<div style="background: linear-gradient(90deg, {stress_color} {st.session_state.stress_level * 10}%, rgba(255,255,255,0.1) {st.session_state.stress_level * 10}%); height: 8px; border-radius: 4px; margin: 0.5rem 0;"></div>', unsafe_allow_html=True)
        st.caption(f"Stress Level: {st.session_state.stress_level}/10")
        
        # Energy level
        energy_color = "#22c55e" if st.session_state.energy_level > 7 else "#f59e0b" if st.session_state.energy_level > 4 else "#ef4444"
        st.markdown(f'<div style="background: linear-gradient(90deg, {energy_color} {st.session_state.energy_level * 10}%, rgba(255,255,255,0.1) {st.session_state.energy_level * 10}%); height: 8px; border-radius: 4px; margin: 0.5rem 0;"></div>', unsafe_allow_html=True)
        st.caption(f"Energy Level: {st.session_state.energy_level}/10")
        
        # Upcoming events
        st.markdown("**📅 Upcoming Events:**")
        for event in st.session_state.calendar_events[:3]:
            st.markdown(f"• {event}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Shopping cart with enhanced features
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🛒 Shopping Cart")
        
        if st.session_state.cart:
            total_items = len(st.session_state.cart)
            estimated_total = sum(random.uniform(5, 50) for _ in st.session_state.cart)
            
            st.markdown(f"**Items:** {total_items}")
            st.markdown(f"**Estimated Total:** ${estimated_total:.2f}")
            
            for i, item in enumerate(st.session_state.cart):
                col_item, col_remove = st.columns([3, 1])
                with col_item:
                    st.markdown(f"• {item}")
                with col_remove:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            
            col_checkout, col_save = st.columns(2)
            with col_checkout:
                if st.button("🚀 Checkout", use_container_width=True):
                    st.success("🎉 Order placed successfully!")
                    st.session_state.cart = []
                    st.balloons()
                    st.rerun()
            with col_save:
                if st.button("💾 Save for Later", use_container_width=True):
                    st.session_state.wishlist.extend(st.session_state.cart)
                    st.session_state.cart = []
                    st.info("Items saved to wishlist!")
                    st.rerun()
        else:
            st.info("Your cart is empty")
            st.markdown("**💝 Wishlist Items:**")
            for item in st.session_state.wishlist[:3]:
                if st.button(f"➕ {item}", key=f"wishlist_{item}"):
                    st.session_state.cart.append(item)
                    st.session_state.wishlist.remove(item)
                    st.success(f"Added {item} to cart!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Notifications center
        if st.session_state.get('show_notifications', False):
            st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
            render_notification_center()
            st.markdown('</div>', unsafe_allow_html=True)

def show_aura_engine():
    st.header("🌈 Aura Engine - Dynamic Personalization")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🎛️ Aura Controls")
        
        # Interactive controls with enhanced UI
        st.markdown("**😰 Stress Level**")
        st.session_state.stress_level = st.slider("", 1, 10, st.session_state.stress_level, key="stress_slider")
        
        st.markdown("**⚡ Energy Level**")
        st.session_state.energy_level = st.slider("", 1, 10, st.session_state.energy_level, key="energy_slider")
        
        st.markdown("**🌤️ Weather Conditions**")
        st.session_state.weather = st.selectbox("", ["Sunny", "Rainy", "Cloudy", "Snowy"], 
                                                 index=["Sunny", "Rainy", "Cloudy", "Snowy"].index(st.session_state.weather))
        
        # Intent selection
        st.markdown("**🎯 Shopping Intent**")
        intents = ["General Shopping", "Healthy Week", "Stress Relief", "Gift Shopping", "Eco-Friendly", "Fitness Focus", "Party Planning", "Work Productivity"]
        st.session_state.current_intent = st.selectbox("", intents, 
                                                       index=intents.index(st.session_state.current_intent))
        
        # Additional context
        st.markdown("**🌱 Sustainability Preference**")
        st.session_state.sustainability_preference = st.checkbox("Prioritize Eco-Friendly Products", 
                                                                st.session_state.sustainability_preference)
        
        st.markdown("**🎵 Mood Enhancement**")
        mood_music = st.checkbox("Enable mood-based ambient sounds")
        if mood_music:
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        
        # Real-time aura calculation
        current_aura, aura_color = aura_engine.calculate_aura({
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather
        })
        
        st.session_state.aura_state = current_aura
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🌟 Current Aura State")
        
        # Enhanced aura visualization
        st.markdown(f'''
            <div style="text-align: center; margin: 2rem 0;">
                <div class="progress-ring">
                    <div class="progress-text">{current_aura}</div>
                </div>
                <p style="color: {aura_color}; font-size: 1.1rem; margin-top: 1rem;">
                    Your aura is currently <strong>{current_aura}</strong>
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        # Aura recommendations
        aura_recs = aura_engine.get_aura_recommendations(current_aura)
        
        st.markdown("**🛍️ Recommended Categories:**")
        for category in aura_recs['categories']:
            st.markdown(f"• {category}")
        
        st.markdown("**🎁 Suggested Products:**")
        for product in aura_recs['products']:
            st.markdown(f"• {product}")
        
        # Aura history chart
        st.markdown("**📈 Aura History (Last 7 Days)**")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        aura_scores = [random.randint(5, 9) for _ in days]
        
        fig = px.line(x=days, y=aura_scores, title="Your Aura Patterns")
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dynamic UI demonstration
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("🎨 Dynamic UI Adaptation")
    
    # Change theme based on aura
    if current_aura == "Stressed":
        st.markdown('''
            <div style="background: linear-gradient(135deg, #ef4444, #f97316); padding: 2rem; border-radius: 15px; color: white;">
                <h3>🧘 Calm & Relaxing Interface</h3>
                <p>The interface has adapted to your stressed state with calming colors and relaxation-focused content. 
                Take a deep breath and explore stress-relief products designed to help you unwind.</p>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🫖 Herbal Teas
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🛁 Bath Products
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🧘 Meditation Tools
                    </span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    elif current_aura == "Energetic":
        st.markdown('''
            <div style="background: linear-gradient(135deg, #f59e0b, #eab308); padding: 2rem; border-radius: 15px; color: white;">
                <h3>⚡ Vibrant & Dynamic Interface</h3>
                <p>The interface is energized with bright colors and activity-focused recommendations! 
                Your high energy is perfect for fitness activities and outdoor adventures.</p>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🏃 Fitness Gear
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🎵 Audio Equipment
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🌟 Energy Supplements
                    </span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="background: linear-gradient(135deg, #0071ce, #3b82f6); padding: 2rem; border-radius: 15px; color: white;">
                <h3>🌟 Balanced Interface</h3>
                <p>The interface maintains a balanced, professional appearance for optimal shopping experience. 
                Your balanced state is perfect for making thoughtful purchasing decisions.</p>
                <div style="margin-top: 1rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🏠 Home Essentials
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        🥗 Healthy Foods
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; margin: 0.2rem;">
                        📚 Educational Items
                    </span>
                </div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_predictive_engine():
    st.header("🔮 Predictive Shopping Engine")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("🧠 AI Predictions")
        
        # Generate predictions
        user_data = {
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather,
            'calendar_events': st.session_state.calendar_events,
            'family_members': st.session_state.family_members,
            'purchase_history': st.session_state.purchase_history,
            'health_goals': st.session_state.health_goals,
            'fitness_data': st.session_state.fitness_data,
            'age': 30  # Mock age
        }
        
        predictions = predictive_engine.generate_predictions(user_data)
        
        # Display prediction timeline
        render_prediction_timeline(predictions)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("📊 Prediction Analytics")
        
        # Create prediction confidence chart
        prediction_data = pd.DataFrame({
            'Model': ['Seasonal', 'Behavioral', 'Social', 'Lifecycle', 'Contextual', 'Health'],
            'Confidence': [92, 88, 85, 90, 87, 83],
            'Accuracy': [94, 91, 87, 89, 88, 85]
        })
        
        fig = px.bar(prediction_data, x='Model', y=['Confidence', 'Accuracy'], 
                    title='Prediction Model Performance', barmode='group',
                    color_discrete_sequence=['#0071ce', '#ffe600'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Model insights
        st.markdown("**🎯 Model Insights:**")
        st.markdown("• **Seasonal patterns:** High accuracy (94%)")
        st.markdown("• **Behavioral analysis:** Strong correlation")
        st.markdown("• **Social triggers:** Moderate confidence")
        st.markdown("• **Lifecycle predictions:** Very reliable")
        st.markdown("• **Contextual factors:** Good performance")
        st.markdown("• **Health integration:** Growing accuracy")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proactive recommendations
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    st.subheader("🎯 Proactive Recommendations")
    
    # Enhanced proactive suggestions with more context
    proactive_suggestions = [
        {
            'trigger': 'Weather forecast shows rain tomorrow',
            'suggestion': 'Umbrella and waterproof jacket',
            'confidence': 95,
            'timing': 'Order today for same-day delivery',
            'reasoning': 'Based on your location weather patterns and past purchases'
        },
        {
            'trigger': 'Friend\'s birthday detected in calendar (3 days)',
            'suggestion': 'Personalized gift based on their interests',
            'confidence': 88,
            'timing': 'Order by tomorrow for on-time delivery',
            'reasoning': 'Social calendar integration and gift history analysis'
        },
        {
            'trigger': 'Stress level trending upward this week',
            'suggestion': 'Aromatherapy and relaxation products',
            'confidence': 82,
            'timing': 'Available for immediate pickup',
            'reasoning': 'Biometric data trends and wellness preferences'
        },
        {
            'trigger': 'Low protein intake detected from fitness app',
            'suggestion': 'High-quality protein supplements',
            'confidence': 79,
            'timing': 'Subscribe & Save option available',
            'reasoning': 'Health goal integration and nutrition tracking'
        },
        {
            'trigger': 'Seasonal wardrobe update needed',
            'suggestion': 'Fall fashion essentials and accessories',
            'confidence': 73,
            'timing': 'Pre-order for early access',
            'reasoning': 'Seasonal patterns and style preferences'
        }
    ]
    
    for suggestion in proactive_suggestions:
        confidence_color = "#22c55e" if suggestion['confidence'] > 85 else "#f59e0b" if suggestion['confidence'] > 75 else "#ef4444"
        
        st.markdown(f'''
            <div style="background: rgba(0, 113, 206, 0.1); padding: 1.5rem; border-radius: 12px; margin: 1rem 0; border-left: 4px solid {confidence_color};">
                <h4 style="margin: 0 0 0.5rem 0;">🔔 {suggestion['trigger']}</h4>
                <p style="margin: 0.5rem 0;"><strong>Suggestion:</strong> {suggestion['suggestion']}</p>
                <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                    <span><strong>Confidence:</strong> <span style="color: {confidence_color};">{suggestion['confidence']}%</span></span>
                    <span><strong>Timing:</strong> {suggestion['timing']}</span>
                </div>
                <p style="font-size: 0.9rem; color: #94a3b8; margin: 0.5rem 0 0 0;">
                    <em>Reasoning:</em> {suggestion['reasoning']}
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_context_awareness():
    st.header("🌍 Context Awareness System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.subheader("📍 Current Context")
        
        # Enhanced location and time display
        current_time = datetime.now()
        st.markdown(f"**📍 Location:** {st.session_state.location}")
        st.markdown(f"**🕐 Time:** {current_time.strftime('%A, %B %d, %Y - %I:%M %p')}")
        st.markdown(f"**🌤️ Weather:** {st.session_state.weather}")
        st.markdown(f"**🌡️ Temperature:** {random.randint(65, 85)}°F")
        
        # Enhanced biometric simulation
        st.markdown("**💓 Biometric Data:**")
        heart_rate = st.session_state.biometric_data['heart_rate']
        sleep_quality = st.session_state.biometric_data['sleep_quality']
        activity_level = st.session_state.biometric_data['activity_level']

def show_live_demo():
    st.header("🚀 Live Demo")
    st.write("This is a placeholder for the live demo features. Add your interactive demo here!")

def process_voice_command(command):
    # Placeholder: just echo the command
    return f"You said: {command}"

def show_sustainability_hub():
    st.header("🌱 Sustainability Hub")
    st.write("This is a placeholder for the Sustainability Hub. Add your sustainability features here!")

def show_social_commerce():
    st.header("👥 Social Commerce")
    st.write("This is a placeholder for Social Commerce. Add your social shopping features here!")

def show_ar_voice_interface():
    st.header("🎯 AR/Voice Interface")
    st.write("This is a placeholder for the AR/Voice Interface. Add your AR and voice features here!")

def show_fun_ai():
    st.header("🤖 Fun AI Features")

    # 1. AI Image Generation (Craiyon)
    st.subheader("🎨 AI Product Image Generator")
    prompt = st.text_input("Describe a product or mood for AI to draw (e.g. 'eco-friendly shopping cart')")
    if st.button("Generate AI Image"):
        if prompt:
            with st.spinner("Generating image..."):
                api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
                payload = {"inputs": prompt}
                response = requests.post(api_url, headers=headers, json=payload)
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image)
                else:
                    st.error(f"Failed to generate image. ({response.status_code}: {response.text})")

    # 2. Joke Generator
    st.subheader("😂 Shopping Joke Generator")
    if st.button("Tell me a shopping joke!"):
        joke_resp = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
        if joke_resp.status_code == 200:
            joke = joke_resp.json().get("joke", "No joke found!")
            st.info(joke)
        else:
            st.info("Why did the developer go broke? Because he used up all his cache!")

    # 3. AI Sentiment Analysis
    st.subheader("🧠 Sentiment Analysis")
    user_text = st.text_area("Type your shopping review or mood:")
    if st.button("Analyze Sentiment"):
        if user_text:
            blob = TextBlob(user_text)
            sentiment = blob.sentiment.polarity
            if sentiment > 0.2:
                st.success("Positive sentiment! 😊")
            elif sentiment < -0.2:
                st.error("Negative sentiment! 😠")
            else:
                st.info("Neutral sentiment. 😐")

    # 4. AI Chatbot (HuggingFace)
    st.subheader("💬 AI Shopping Assistant")
    chat_input = st.text_input("Ask the AI anything about shopping:")
    if st.button("Ask AI"):
        if chat_input:
            api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
            payload = {"inputs": chat_input}
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()
                # Blenderbot returns a list of dicts with 'generated_text'
                if isinstance(result, list) and "generated_text" in result[0]:
                    ai_reply = result[0]["generated_text"]
                elif isinstance(result, dict) and "generated_text" in result:
                    ai_reply = result["generated_text"]
                else:
                    ai_reply = "No reply."
                st.write("AI:", ai_reply)
            else:
                st.error(f"AI is busy. Try again later. ({response.status_code}: {response.text})")

if __name__ == "__main__":
    if not st.session_state.get('logged_in', False):
        if st.session_state.get('show_register', False):
            show_register_form()
        else:
            show_enhanced_login()
    else:
        main_nexus_app()

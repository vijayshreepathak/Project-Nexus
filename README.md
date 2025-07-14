# 🌌 Project Nexus - AI-Empathetic Retail Experience



![Project Nexus Logo](https://img.shields.io/badge/Project-Nexus-blue?style=for-the-badge&logo=walmart&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-brightgreen?style=for-the-badge)

**🚀 Reimagining Customer Experience with Emerging Technologies**

*An AI-empathetic retail ecosystem that adapts to customers' real-time context, emotions, and sustainability preferences*

[🎯 Live Demo](#) | [📖 Documentation](#documentation) | [🐛 Report Bug](#) | [💡 Request Feature](#)



## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📦 Complete Code](#-complete-code)
- [🔧 Configuration](#-configuration)
- [☁️ Deployment](#️-deployment)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🎯 Project Overview

Project Nexus is an innovative AI-empathetic retail experience platform designed for the **Walmart Sparkathon 2025**. It revolutionizes customer shopping by creating a dynamic, context-aware ecosystem that adapts to users' emotional states, environmental consciousness, and social connections.

### 🌟 Key Innovations

- **🧠 Aura Engine**: Real-time emotional state detection and UI adaptation
- **🔮 Predictive Intelligence**: 6 AI models for anticipating customer needs
- **🌱 Sustainability Hub**: Carbon footprint tracking and eco-friendly recommendations
- **👥 Social Commerce**: Community-driven shopping with family coordination
- **🎯 Context Awareness**: Weather, location, and calendar integration

## ✨ Features

### 🎨 Core Features

| Feature | Description | Technology |
|---------|-------------|------------|
| 🔐 **Authentication** | Secure login/registration with bcrypt | SQLite + bcrypt |
| 🌈 **Dynamic Aura System** | Mood-based UI adaptation | Custom AI Engine |
| 🔮 **Predictive Shopping** | AI-driven need anticipation | Multi-model ML |
| 🌱 **Sustainability Tracking** | Carbon footprint and eco-scores | Custom Algorithm |
| 👥 **Social Commerce** | Family lists and friend recommendations | Social Graph AI |
| 🎯 **AR/Voice Interface** | Next-gen shopping interactions | NLP + Computer Vision |

### 🤖 AI-Powered Entertainment

- **🎨 Product Image Generator**: Create custom visuals with HuggingFace
- **😂 Shopping Humor Bot**: Lighten the mood with retail jokes
- **💭 Sentiment Analysis**: Understand customer emotions with TextBlob
- **🤖 AI Shopping Assistant**: Conversational help with GPT-2

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Layer    │    │  AI Engine      │    │  Data Layer     │
│                 │    │                 │    │                 │
│ -  Streamlit UI  │◄──►│ -  Aura Engine   │◄──►│ -  SQLite DB     │
│ -  Dynamic Theme │    │ -  Predictive ML │    │ -  User Profiles │
│ -  Voice/AR      │    │ -  Sustainability│    │ -  Product Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 📋 Prerequisites

- Python 3.9+ (Recommended: 3.11)
- Git
- HuggingFace Account (Free)

### ⚡ Installation

```
# 1. Clone repository
git clone https://github.com/vijayshreepathak/Project-Nexus.git
cd Project-Nexus

# 2. Create virtual environment
python -m venv nexus-env
source nexus-env/bin/activate  # Windows: nexus-env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
echo "HUGGINGFACE_TOKEN=your_token_here" > .env

# 5. Run application
streamlit run app.py
```

### 🎯 Demo Credentials

| Role | Username | Password | Access |
|------|----------|----------|---------|
| Admin | `admin` | `admin123` | Full access |
| Demo | `demo` | `demo123` | Standard features |

## 📦 Complete Code

### 📄 requirements.txt

```
# Core Framework
streamlit==1.46.1

# Data Processing
pandas==2.3.0
numpy==2.0.0

# Visualization
plotly==5.24.0

# Security & Validation
bcrypt==4.3.0
validators==0.28.1

# Image Processing
Pillow==10.4.0

# AI/ML Libraries
textblob==0.17.1
requests==2.32.3

# Utilities
python-dotenv==1.0.1
```

### 🐍 app.py - Complete Application Code 
import streamlit as st
import pandas as pd
import numpy as np
import json
import sqlite3
import hashlib
import re
import random
import time
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

# Safe imports with fallbacks
try:
    from PIL import Image, ImageEnhance, ImageFilter
    import io
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

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

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Configure page
st.set_page_config(
    page_title="Project Nexus - Walmart Sparkathon",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced logging
logging.basicConfig(
    filename='nexus_audit.log', 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s'
)

def log_action(user, action, details=None):
    """Log user actions for audit trail"""
    logging.info(f"User: {user}, Action: {action}, Details: {details}")

# Utility Functions
def hash_password(password):
    """Hash password securely"""
    if HAS_BCRYPT:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """Verify password against hash"""
    if HAS_BCRYPT:
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    else:
        return hashlib.sha256(password.encode()).hexdigest() == hashed

def is_valid_email(email):
    """Validate email format"""
    if HAS_VALIDATORS:
        return validators.email(email)
    else:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

# Session State Initialization
def initialize_session_state():
    """Initialize all session state variables with defaults"""
    defaults = {
        'logged_in': False,
        'username': "",
        'user_role': "",
        'user_id': None,
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
        'eco_score': 85,
        'carbon_footprint': 20,
        'prediction_accuracy': 92,
        'loyalty_points': 1250,
        'membership_tier': "Gold",
        'health_goals': ["Weight Management", "Heart Health"],
        'fitness_data': {"steps": 8450, "calories": 2100, "water": 6},
        'voice_command': "I need something cozy for this weekend's weather",
        'show_register': False,
        'dark_mode': True,
        'tutorial_completed': False,
        'favorite_brands': ["Organic Valley", "Great Value", "Mainstays"],
        'dietary_restrictions': [],
        'allergies': [],
        'mood_tracking': {"happiness": 7, "energy": 6, "focus": 8},
        'ai_preferences': {"prediction_level": "high", "personalization": "maximum"},
        'shopping_behavior': {"impulse_buyer": False, "research_heavy": True, "price_sensitive": True},
        'environmental_commitment': {"carbon_conscious": True, "waste_reduction": True, "local_sourcing": True}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# Database Setup
def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect('nexus_sparkathon.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_comprehensive_db():
    """Initialize comprehensive database schema"""
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
    
    # Initialize admin user
    c.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if c.fetchone() == 0:
        admin_password = hash_password("admin123")
        c.execute('''INSERT INTO users (username, password, email, role, is_active) 
                     VALUES (?, ?, ?, ?, ?)''',
                  ('admin', admin_password, 'admin@walmart.com', 'admin', 1))
    
    # Initialize demo user
    c.execute("SELECT COUNT(*) FROM users WHERE username = 'demo'")
    if c.fetchone() == 0:
        demo_password = hash_password("demo123")
        c.execute('''INSERT INTO users (username, password, email, role, is_active) 
                     VALUES (?, ?, ?, ?, ?)''',
                  ('demo', demo_password, 'demo@walmart.com', 'user', 1))
    
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
        ("Plant-Based Milk", "Dairy Alternative", 4.99, 8, 0.6, "A", "Oat milk alternative", "", 180, 8.7)
    ]
    
    for product in sample_products:
        c.execute("SELECT COUNT(*) FROM products WHERE name = ?", (product,))
        if c.fetchone() == 0:
            c.execute('''INSERT INTO products (name, category, price, eco_score, carbon_footprint, 
                         sustainability_rating, description, image_url, stock_quantity, popularity_score) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', product)
    
    conn.commit()
    conn.close()

init_comprehensive_db()

# Authentication Functions
def authenticate_user(username, password):
    """Authenticate user credentials"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
    user = c.fetchone()
    if user:
        stored_password = user
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
    """Create new user account"""
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

# Enhanced CSS Styling
def load_css():
    """Load enhanced CSS for Walmart branding"""
    st.markdown('''
        
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
        .aura-calm { background: linear-gradient(45deg, #10b981, #059669); color: white; }
        
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
        
        @media (max-width: 768px) {
            .walmart-header { font-size: 2.5rem; }
            .nexus-card { padding: 1rem; margin: 0.5rem 0; }
            .metric-value { font-size: 2rem; }
        }
        
    ''', unsafe_allow_html=True)

# AI Engine Classes
class AuraEngine:
    """Advanced Aura Detection and Adaptation Engine"""
    
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
        """Calculate user's current aura state"""
        stress = user_data.get('stress_level', 5)
        energy = user_data.get('energy_level', 7)
        weather = user_data.get('weather', 'Sunny')
        hour = datetime.now().hour
        
        # Stress-based aura
        if stress > 7:
            return "Stressed", "#ef4444"
        elif stress  8:
            return "Energetic", "#f59e0b"
        elif energy  5:
            return "Cozy", "#8b5cf6"
        elif weather == "Sunny" and energy > 6:
            return "Vibrant", "#f59e0b"
        
        # Time-based influence
        if hour  22:
            return "Restful", "#6366f1"
        elif 6  0.1:
            return "Positive 😊", polarity
        elif polarity 
            🌟 {aura_state} Aura
        
    ''', unsafe_allow_html=True)

def render_metric_card(value, label, color="#0071ce", trend=None):
    """Render animated metric card"""
    trend_indicator = ""
    if trend:
        if trend > 0:
            trend_indicator = f'↗ +{trend}%'
        elif trend ↘ {trend}%'
    
    st.markdown(f'''
        
            {value}
            {label}
            {trend_indicator}
        
    ''', unsafe_allow_html=True)

def render_product_card(product_name, price, eco_score, description=""):
    """Render product card with eco rating"""
    eco_class = "eco-excellent" if eco_score > 8 else "eco-good" if eco_score > 6 else "eco-fair"
    
    st.markdown(f'''
        
            {product_name}
            {description}
            
                ${price}
                Eco: {eco_score}/10
            
        
    ''', unsafe_allow_html=True)

# Authentication UI
def show_enhanced_login():
    """Enhanced login interface"""
    st.markdown('''
        
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        
            🛒
            
                Project Nexus
            
            AI-Empathetic Retail Experience
        
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
                    st.session_state.username = user
                    st.session_state.user_role = user
                    st.session_state.user_id = user
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
    
    st.markdown('''
        
            Demo Credentials:
            Username: admin | Password: admin123
            Username: demo | Password: demo123
        
    ''', unsafe_allow_html=True)
    
    st.markdown('', unsafe_allow_html=True)

def show_register_form():
    """Registration form interface"""
    st.markdown('''
        
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        
            📝
            Register
            Create Your Account
        
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
                elif len(new_password) ', unsafe_allow_html=True)

# Main Application Pages
def main_nexus_app():
    """Main application interface"""
    load_css()
    
    # Header
    st.markdown('''
        
            🌌 Project Nexus
            
                AI-Empathetic Retail Experience -  Walmart Sparkathon 2025
            
        
    ''', unsafe_allow_html=True)
    
    # User info bar
    col1, col2, col3 = st.columns()
    with col1:
        st.markdown(f'''
            
                👤 {st.session_state.username} | 
                Role: {st.session_state.user_role.title()} |
                💎 {st.session_state.membership_tier} Member |
                🏆 {st.session_state.loyalty_points} Points
            
        ''', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Refresh Aura"):
            current_aura, _ = aura_engine.calculate_aura({
                'stress_level': st.session_state.stress_level,
                'energy_level': st.session_state.energy_level,
                'weather': st.session_state.weather
            })
            st.session_state.aura_state = current_aura
            st.rerun()
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_id = None
            st.rerun()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox("Choose Experience", [
        "🏠 Dashboard",
        "🌈 Aura Engine",
        "🔮 Predictive Shopping",
        "🌍 Context Awareness",
        "🌱 Sustainability Hub",
        "👥 Social Commerce",
        "🎯 AR/Voice Interface",
        "🎭 AI Entertainment",
        "🚀 Live Demo"
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
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "🌈 Aura Engine":
        show_aura_engine()
    elif page == "🔮 Predictive Shopping":
        show_predictive_engine()
    elif page == "🌍 Context Awareness":
        show_context_awareness()
    elif page == "🌱 Sustainability Hub":
        show_sustainability_hub()
    elif page == "👥 Social Commerce":
        show_social_commerce()
    elif page == "🎯 AR/Voice Interface":
        show_ar_voice_interface()
    elif page == "🎭 AI Entertainment":
        show_ai_entertainment()
    elif page == "🚀 Live Demo":
        show_live_demo()

def show_dashboard():
    """Main dashboard with key metrics and recommendations"""
    st.header("🏠 Intelligent Shopping Dashboard")
    
    # Real-time metrics
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
    col1, col2 = st.columns()
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🎯 Personalized Recommendations")
        
        # Get current aura
        current_aura, _ = aura_engine.calculate_aura({
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather
        })
        
        # Dynamic product recommendations
        if current_aura == "Stressed":
            products = [
                ("Stress-Relief Tea", 8.99, 8, "Herbal blend for relaxation"),
                ("Aromatherapy Diffuser", 45.99, 8, "Essential oil diffuser"),
                ("Meditation Cushion", 39.99, 8, "Comfortable meditation seat")
            ]
        elif current_aura == "Energetic":
            products = [
                ("Protein Powder", 29.99, 7, "Plant-based nutrition"),
                ("Wireless Headphones", 129.99, 4, "For workout music"),
                ("Yoga Mat", 29.99, 7, "Non-slip exercise mat")
            ]
        else:
            products = [
                ("Organic Quinoa", 12.99, 9, "Premium organic grain"),
                ("Bluetooth Speaker", 79.99, 6, "High-quality audio"),
                ("Bamboo Toothbrush", 4.99, 10, "Eco-friendly dental care")
            ]
        
        for i, product in enumerate(products):
            col_prod, col_btn = st.columns()
            with col_prod:
                render_product_card(*product)
            with col_btn:
                if st.button(f"Add to Cart", key=f"add_{i}"):
                    st.session_state.cart.append(product)
                    st.success(f"Added {product} to cart!")
                    st.rerun()
        
        st.markdown('', unsafe_allow_html=True)
        
        # AI Insights
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🔮 AI Insights")
        
        user_data = {
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather,
            'calendar_events': st.session_state.calendar_events,
            'health_goals': st.session_state.health_goals
        }
        
        predictions = predictive_engine.generate_predictions(user_data)[:5]
        
        for prediction in predictions:
            st.markdown(f"-  **{prediction}** - Based on your patterns and preferences")
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🧠 AI Context")
        
        # Current context
        st.markdown(f"**🌤️ Weather:** {st.session_state.weather}")
        st.markdown(f"**📍 Location:** {st.session_state.location}")
        st.markdown(f"**🕐 Time:** {datetime.now().strftime('%I:%M %p')}")
        st.markdown(f"**🎯 Intent:** {st.session_state.current_intent}")
        
        # Biometric data visualization
        st.markdown("**💓 Biometric Data:**")
        
        stress_color = "#ef4444" if st.session_state.stress_level > 7 else "#f59e0b" if st.session_state.stress_level > 4 else "#22c55e"
        st.markdown(f'''
            
        ''', unsafe_allow_html=True)
        st.caption(f"Stress Level: {st.session_state.stress_level}/10")
        
        energy_color = "#22c55e" if st.session_state.energy_level > 7 else "#f59e0b" if st.session_state.energy_level > 4 else "#ef4444"
        st.markdown(f'''
            
        ''', unsafe_allow_html=True)
        st.caption(f"Energy Level: {st.session_state.energy_level}/10")
        
        # Upcoming events
        st.markdown("**📅 Upcoming Events:**")
        for event in st.session_state.calendar_events[:3]:
            st.markdown(f"-  {event}")
        
        st.markdown('', unsafe_allow_html=True)
        
        # Shopping cart
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🛒 Shopping Cart")
        
        if st.session_state.cart:
            total_items = len(st.session_state.cart)
            estimated_total = sum(random.uniform(5, 50) for _ in st.session_state.cart)
            
            st.markdown(f"**Items:** {total_items}")
            st.markdown(f"**Estimated Total:** ${estimated_total:.2f}")
            
            for i, item in enumerate(st.session_state.cart):
                col_item, col_remove = st.columns()
                with col_item:
                    st.markdown(f"-  {item}")
                with col_remove:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            
            if st.button("🚀 Checkout", use_container_width=True):
                st.success("🎉 Order placed successfully!")
                st.session_state.cart = []
                st.balloons()
                st.rerun()
        else:
            st.info("Your cart is empty")
        
        st.markdown('', unsafe_allow_html=True)

def show_aura_engine():
    """Aura Engine configuration and visualization"""
    st.header("🌈 Aura Engine - Dynamic Personalization")
    
    col1, col2 = st.columns()
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🎛️ Aura Controls")
        
        # Interactive controls
        st.markdown("**😰 Stress Level**")
        st.session_state.stress_level = st.slider("", 1, 10, st.session_state.stress_level, key="stress_slider")
        
        st.markdown("**⚡ Energy Level**")
        st.session_state.energy_level = st.slider("", 1, 10, st.session_state.energy_level, key="energy_slider")
        
        st.markdown("**🌤️ Weather Conditions**")
        st.session_state.weather = st.selectbox("", ["Sunny", "Rainy", "Cloudy", "Snowy"], 
                                                 index=["Sunny", "Rainy", "Cloudy", "Snowy"].index(st.session_state.weather))
        
        # Intent selection
        st.markdown("**🎯 Shopping Intent**")
        intents = ["General Shopping", "Healthy Week", "Stress Relief", "Gift Shopping", "Eco-Friendly", "Fitness Focus"]
        st.session_state.current_intent = st.selectbox("", intents, 
                                                       index=intents.index(st.session_state.current_intent))
        
        # Sustainability preference
        st.markdown("**🌱 Sustainability Preference**")
        st.session_state.sustainability_preference = st.checkbox("Prioritize Eco-Friendly Products", 
                                                                st.session_state.sustainability_preference)
        
        current_aura, aura_color = aura_engine.calculate_aura({
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather
        })
        
        st.session_state.aura_state = current_aura
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🌟 Current Aura State")
        
        # Aura visualization
        st.markdown(f'''
            
                
                    
                        {current_aura}
                    
                
                
                    Your aura is currently {current_aura}
                
            
        ''', unsafe_allow_html=True)
        
        # Aura recommendations
        aura_recs = aura_engine.get_aura_recommendations(current_aura)
        
        st.markdown("**🛍️ Recommended Categories:**")
        for category in aura_recs['categories']:
            st.markdown(f"-  {category}")
        
        st.markdown("**🎁 Suggested Products:**")
        for product in aura_recs['products']:
            st.markdown(f"-  {product}")
        
        st.markdown('', unsafe_allow_html=True)
    
    # Dynamic UI demonstration
    st.markdown('', unsafe_allow_html=True)
    st.subheader("🎨 Dynamic UI Adaptation")
    
    if current_aura == "Stressed":
        st.markdown('''
            
                🧘 Calm & Relaxing Interface
                The interface has adapted to your stressed state with calming colors and relaxation-focused content.
            
        ''', unsafe_allow_html=True)
    elif current_aura == "Energetic":
        st.markdown('''
            
                ⚡ Vibrant & Dynamic Interface
                The interface is energized with bright colors and activity-focused recommendations!
            
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            
                🌟 Balanced Interface
                The interface maintains a balanced, professional appearance for optimal shopping experience.
            
        ''', unsafe_allow_html=True)
    
    st.markdown('', unsafe_allow_html=True)

def show_predictive_engine():
    """Predictive shopping intelligence dashboard"""
    st.header("🔮 Predictive Shopping Engine")
    
    col1, col2 = st.columns()
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🧠 AI Predictions")
        
        user_data = {
            'stress_level': st.session_state.stress_level,
            'energy_level': st.session_state.energy_level,
            'weather': st.session_state.weather,
            'calendar_events': st.session_state.calendar_events,
            'health_goals': st.session_state.health_goals
        }
        
        predictions = predictive_engine.generate_predictions(user_data)
        
        # Display prediction timeline
        st.markdown("#### 🔮 Predictive Timeline")
        
        for i, prediction in enumerate(predictions):
            days_ahead = i + 1
            confidence = max(85, 95 - i*2)
            
            st.markdown(f'''
                
                    In {days_ahead} days: {prediction}
                    
                        Confidence: {confidence}% | Based on: Pattern Analysis
                    
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("📊 Prediction Analytics")
        
        # Create prediction confidence chart
        prediction_data = pd.DataFrame({
            'Model': ['Seasonal', 'Behavioral', 'Social', 'Contextual', 'Health'],
            'Confidence': ,
            'Accuracy': 
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
        
        st.markdown("**🎯 Model Insights:**")
        st.markdown("-  **Seasonal patterns:** High accuracy (94%)")
        st.markdown("-  **Behavioral analysis:** Strong correlation")
        st.markdown("-  **Social triggers:** Moderate confidence")
        st.markdown("-  **Contextual factors:** Good performance")
        st.markdown("-  **Health integration:** Growing accuracy")
        
        st.markdown('', unsafe_allow_html=True)

def show_context_awareness():
    """Context awareness system dashboard"""
    st.header("🌍 Context Awareness System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("📍 Current Context")
        
        current_time = datetime.now()
        st.markdown(f"**📍 Location:** {st.session_state.location}")
        st.markdown(f"**🕐 Time:** {current_time.strftime('%A, %B %d, %Y - %I:%M %p')}")
        st.markdown(f"**🌤️ Weather:** {st.session_state.weather}")
        st.markdown(f"**🌡️ Temperature:** {random.randint(65, 85)}°F")
        
        # Biometric data
        st.markdown("**💓 Biometric Data:**")
        heart_rate = st.session_state.biometric_data['heart_rate']
        sleep_quality = st.session_state.biometric_data['sleep_quality']
        activity_level = st.session_state.biometric_data['activity_level']
        
        col_hr, col_sleep, col_activity = st.columns(3)
        with col_hr:
            st.metric("Heart Rate", f"{heart_rate} bpm")
        with col_sleep:
            st.metric("Sleep Quality", f"{sleep_quality}/10")
        with col_activity:
            st.metric("Activity Level", f"{activity_level}/10")
        
        # Calendar integration
        st.markdown("**📅 Upcoming Events:**")
        for event in st.session_state.calendar_events:
            st.markdown(f"-  {event}")
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🎯 Context-Aware Recommendations")
        
        current_hour = datetime.now().hour
        
        if current_hour ', unsafe_allow_html=True)

def show_sustainability_hub():
    """Sustainability tracking and optimization hub"""
    st.header("🌱 Sustainability Hub")
    
    # Generate sustainability report
    sustainability_report = sustainability_engine.generate_sustainability_report({
        'cart': st.session_state.cart,
        'purchase_history': st.session_state.purchase_history
    })
    
    # Sustainability metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(f"{sustainability_report['eco_score']}", "Eco Score", "#22c55e")
    with col2:
        render_metric_card(f"{sustainability_report['carbon_footprint']:.1f}kg", "Carbon Footprint", "#f59e0b")
    with col3:
        render_metric_card(sustainability_report['eco_grade'], "Eco Grade", "#3b82f6")
    with col4:
        render_metric_card("15%", "Waste Reduction", "#8b5cf6")
    
    col1, col2 = st.columns()
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🌍 Environmental Impact")
        
        # Carbon footprint chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        carbon_data = 
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=carbon_data, mode='lines+markers', 
                                name='Carbon Footprint', line=dict(color='#22c55e')))
        
        fig.update_layout(
            title='Carbon Footprint Reduction Over Time',
            xaxis_title='Month',
            yaxis_title='CO2 (kg)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Eco-friendly alternatives
        st.markdown("**🌿 Eco-Friendly Alternatives:**")
        
        alternatives = [
            ("Plastic water bottles", "Reusable steel bottle", "Save 156 bottles/year"),
            ("Paper towels", "Reusable cloth towels", "Reduce waste by 80%"),
            ("Incandescent bulbs", "LED bulbs", "75% less energy"),
            ("Disposable bags", "Reusable bags", "Prevent 1000+ bags/year")
        ]
        
        for original, alternative, impact in alternatives:
            st.markdown(f'''
                
                    {original} → {alternative}
                    Impact: {impact}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🎯 Sustainability Goals")
        
        # Progress rings for goals
        goals = [
            ("Carbon Neutral", 78, "#22c55e"),
            ("Zero Waste", 65, "#3b82f6"),
            ("Local Sourcing", 92, "#f59e0b"),
            ("Renewable Energy", 85, "#8b5cf6")
        ]
        
        for goal, progress, color in goals:
            st.markdown(f'''
                
                    {goal}
                    
                        
                            {progress}%
                        
                    
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
        
        # Sustainability actions
        st.markdown('', unsafe_allow_html=True)
        st.subheader("⚡ Quick Actions")
        
        if st.button("🌱 Plant a Tree", use_container_width=True):
            st.success("Tree planted! +50 eco points")
        
        if st.button("♻️ Recycle Program", use_container_width=True):
            st.success("Joined recycling program!")
        
        if st.button("🚗 Carbon Offset", use_container_width=True):
            st.success("Carbon offset purchased!")
        
        if st.button("🌟 Share Impact", use_container_width=True):
            st.success("Shared your eco achievements!")
        
        st.markdown('', unsafe_allow_html=True)

def show_social_commerce():
    """Social commerce and community features"""
    st.header("👥 Social Commerce")
    
    col1, col2 = st.columns()
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("👨‍👩‍👧‍👦 Family Shopping Coordination")
        
        # Family members management
        st.markdown("**Family Members:**")
        family_input = st.text_input("Add family member", placeholder="Enter name")
        if st.button("Add Member") and family_input:
            st.session_state.family_members.append(family_input)
            st.success(f"Added {family_input} to family!")
        
        # Display family members
        for member in st.session_state.family_members:
            col_name, col_action = st.columns()
            with col_name:
                st.markdown(f"-  {member}")
            with col_action:
                if st.button("Remove", key=f"remove_family_{member}"):
                    st.session_state.family_members.remove(member)
                    st.rerun()
        
        # Family shopping list
        st.markdown("**Shared Shopping List:**")
        shared_items = ["Milk", "Bread", "Eggs", "Apples", "Chicken"]
        for item in shared_items:
            col_item, col_assigned = st.columns()
            with col_item:
                st.markdown(f"-  {item}")
            with col_assigned:
                assigned_to = random.choice(st.session_state.family_members)
                st.caption(f"Assigned to: {assigned_to}")
        
        st.markdown('', unsafe_allow_html=True)
        
        # Community trends
        st.markdown('', unsafe_allow_html=True)
        st.subheader("📈 Community Trends")
        
        trending_products = [
            ("Plant-based milk", "↗️ +45%", "#22c55e"),
            ("Reusable bags", "↗️ +38%", "#3b82f6"),
            ("Local honey", "↗️ +32%", "#f59e0b"),
            ("Organic produce", "↗️ +28%", "#8b5cf6"),
            ("Eco-friendly cleaners", "↗️ +25%", "#06b6d4")
        ]
        
        for product, trend, color in trending_products:
            st.markdown(f'''
                
                    {product}
                    {trend}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("👫 Friends & Social")
        
        # Friends list
        st.markdown("#### 👥 Social Circle")
        
        friends_html = "".join([
            f'{friend}'
            for friend in st.session_state.friends
        ])
        
        family_html = "".join([
            f'{member}'
            for member in st.session_state.family_members
        ])
        
        st.markdown(f'''
            
                Friends: {friends_html}
                Family: {family_html}
            
        ''', unsafe_allow_html=True)
        
        # Friend recommendations
        st.markdown("**Gift Recommendations:**")
        friend_gifts = [
            ("Alex", "Bluetooth headphones", "Based on music interests"),
            ("Jamie", "Yoga mat", "Recently started yoga"),
            ("Chris", "Coffee beans", "Coffee enthusiast")
        ]
        
        for friend, gift, reason in friend_gifts:
            st.markdown(f'''
                
                    {friend}
                    {gift}
                    {reason}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)

def show_ar_voice_interface():
    """AR and Voice interface demonstration"""
    st.header("🎯 AR/Voice Interface")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🕶️ Augmented Reality Shopping")
        
        # AR simulation
        st.markdown("**Upload room image for AR product placement:**")
        uploaded_file = st.file_uploader("Choose image", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            if HAS_PIL:
                image = Image.open(uploaded_file)
                st.image(image, caption="Your Room", use_column_width=True)
                
                # Simulate AR product placement
                st.markdown("**AR Product Placement:**")
                ar_products = ["Sofa", "Coffee Table", "Lamp", "Plant", "TV"]
                selected_product = st.selectbox("Select product to place", ar_products)
                
                if st.button("Place Product"):
                    st.success(f"Placed {selected_product} in your room!")
                    st.markdown("*In a real AR system, the product would appear overlaid on your room image*")
            else:
                st.info("PIL not available. AR simulation requires image processing.")
        
        # AR features
        st.markdown("**AR Features:**")
        ar_features = [
            "🏠 Virtual furniture placement",
            "📏 Size and scale visualization",
            "🎨 Color and style matching",
            "💡 Lighting simulation",
            "🔄 360° product rotation",
            "📱 Try-before-you-buy"
        ]
        
        for feature in ar_features:
            st.markdown(f"-  {feature}")
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🎤 Voice Commerce")
        
        # Voice command simulation
        st.markdown("**Voice Assistant:**")
        
        voice_command = st.text_area("Speak or type your command:", 
                                   st.session_state.voice_command,
                                   height=100)
        
        if st.button("🎤 Process Voice Command"):
            st.session_state.voice_command = voice_command
            response = process_voice_command(voice_command)
            st.markdown(f"**Assistant:** {response}")
        
        # Voice capabilities
        st.markdown("**Voice Capabilities:**")
        voice_capabilities = [
            "🛒 Add items to cart",
            "🔍 Search products",
            "📦 Check order status",
            "💰 Compare prices",
            "📍 Find store locations",
            "⏰ Set shopping reminders",
            "🎯 Get recommendations",
            "📊 Check sustainability score"
        ]
        
        for capability in voice_capabilities:
            st.markdown(f"-  {capability}")
        
        # Sample voice commands
        st.markdown("**Sample Commands:**")
        sample_commands = [
            "Add organic milk to my cart",
            "Find eco-friendly alternatives",
            "What's trending in my area?",
            "Schedule delivery for tomorrow",
            "Show me products under $20",
            "Find gifts for my friend who loves yoga"
        ]
        
        for cmd in sample_commands:
            if st.button(f'"{cmd}"', key=f"voice_{cmd}"):
                response = process_voice_command(cmd)
                st.info(f"**Assistant:** {response}")
        
        st.markdown('', unsafe_allow_html=True)

def show_ai_entertainment():
    """AI-powered entertainment features"""
    st.header("🎭 AI Entertainment Hub")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("😂 Shopping Humor Bot")
        
        if st.button("🎪 Get a Shopping Joke", use_container_width=True):
            joke = get_joke()
            st.markdown(f'''
                
                    😂 Shopping Joke
                    {joke}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
        st.subheader("💭 Sentiment Analysis")
        
        user_text = st.text_area("Share your shopping experience:", 
                                placeholder="Tell us how you feel about your shopping today...")
        
        if st.button("Analyze Sentiment", use_container_width=True) and user_text:
            sentiment, polarity = analyze_sentiment(user_text)
            
            if "Positive" in sentiment:
                color = "#22c55e"
                icon = "😊"
            elif "Negative" in sentiment:
                color = "#ef4444"
                icon = "😔"
            else:
                color = "#94a3b8"
                icon = "😐"
            
            st.markdown(f'''
                
                    
                        {icon} Sentiment: {sentiment}
                    
                    Polarity Score: {polarity:.2f}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
    
    with col2:
        st.markdown('', unsafe_allow_html=True)
        st.subheader("🤖 AI Shopping Assistant")
        
        ai_prompt = st.text_input("Ask the AI Assistant:", 
                                placeholder="Ask about recommendations, sustainability, etc.")
        
        if st.button("Get AI Response", use_container_width=True) and ai_prompt:
            response = generate_ai_response(ai_prompt)
            st.markdown(f'''
                
                    🤖 AI Assistant
                    {response}
                
            ''', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)
        
        st.markdown('', unsafe_allow_html=True)

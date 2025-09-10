#!/usr/bin/env python3
"""
Telegram AI Bot Dashboard
A web interface to control all bot functionalities including personality, PDFs, and debugging.
"""

import os
import json
import shutil
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
import threading
import subprocess
import time
from datetime import datetime

app = Flask(__name__, template_folder='dashboard/templates', static_folder='dashboard/static')
app.secret_key = 'your-secret-key-change-this'
CORS(app)

# Configuration
UPLOAD_FOLDER = 'pdf_storage'
ALLOWED_EXTENSIONS = {'pdf'}
BOT_CONFIG_FILE = 'bot_config.json'
PERSONALITIES_FILE = 'personalities.json'

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_bot_config():
    """Load bot configuration from file"""
    default_config = {
        'reply_probability': 0.4,
        'context_msg_limit': 15,
        'max_prompt_msgs': 10,
        'max_response_tokens': 200,
        'min_response_delay': 1.0,
        'max_response_delay': 4.0,
        'typing_delay_per_word': 0.15,
        'active_personality': 'sylvia_default',
        'pdf_directory': '.',
        'debug_mode': False
    }
    
    if os.path.exists(BOT_CONFIG_FILE):
        try:
            with open(BOT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            pass
    
    return default_config

def save_bot_config(config):
    """Save bot configuration to file"""
    with open(BOT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_personalities():
    """Load personality presets"""
    default_personalities = {
        'sylvia_default': {
            'name': 'Sylvia (Default)',
            'description': 'Chaotic gamer girl from Amman - sarcastic, caring, roast queen',
            'content': open('personality.txt', 'r').read() if os.path.exists('personality.txt') else ''
        },
        'professional': {
            'name': 'Professional Assistant',
            'description': 'Formal, helpful business assistant',
            'content': '''You are a professional AI assistant. You communicate clearly and formally, providing helpful information and assistance in a business-appropriate manner. You are knowledgeable, respectful, and efficient.'''
        },
        'casual_friend': {
            'name': 'Casual Friend',
            'description': 'Relaxed, friendly, supportive companion',
            'content': '''You are a casual, friendly AI companion. You speak in a relaxed, conversational tone like talking to a good friend. You're supportive, understanding, and enjoy chatting about everyday topics.'''
        },
        'tech_expert': {
            'name': 'Tech Expert',
            'description': 'Knowledgeable programmer and tech enthusiast',
            'content': '''You are a tech-savvy AI with deep knowledge of programming, software development, and technology trends. You communicate with technical precision but remain approachable and helpful.'''
        }
    }
    
    if os.path.exists(PERSONALITIES_FILE):
        try:
            with open(PERSONALITIES_FILE, 'r') as f:
                personalities = json.load(f)
                # Merge with defaults
                for key, value in default_personalities.items():
                    if key not in personalities:
                        personalities[key] = value
                return personalities
        except:
            pass
    
    return default_personalities

def save_personalities(personalities):
    """Save personality presets to file"""
    with open(PERSONALITIES_FILE, 'w') as f:
        json.dump(personalities, f, indent=2)

def get_pdf_list():
    """Get list of available PDF files"""
    pdfs = []
    
    # Check main directory
    if os.path.exists('.'):
        for file in os.listdir('.'):
            if file.endswith('.pdf'):
                stat = os.stat(file)
                pdfs.append({
                    'name': file,
                    'path': file,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
    
    # Check upload directory
    if os.path.exists(UPLOAD_FOLDER):
        for file in os.listdir(UPLOAD_FOLDER):
            if file.endswith('.pdf'):
                path = os.path.join(UPLOAD_FOLDER, file)
                stat = os.stat(path)
                pdfs.append({
                    'name': file,
                    'path': path,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
    
    return pdfs

def get_accounts():
    """Get bot accounts configuration"""
    try:
        with open('accounts.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_accounts(accounts):
    """Save bot accounts configuration"""
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=2)

# Routes
@app.route('/')
def index():
    """Dashboard home page"""
    config = load_bot_config()
    personalities = load_personalities()
    pdfs = get_pdf_list()
    accounts = get_accounts()
    
    return render_template('dashboard.html', 
                         config=config, 
                         personalities=personalities,
                         pdfs=pdfs,
                         accounts=accounts)

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Bot configuration API"""
    if request.method == 'GET':
        return jsonify(load_bot_config())
    
    elif request.method == 'POST':
        config = request.json
        save_bot_config(config)
        return jsonify({'status': 'success'})

@app.route('/api/personalities', methods=['GET', 'POST'])
def api_personalities():
    """Personality management API"""
    if request.method == 'GET':
        return jsonify(load_personalities())
    
    elif request.method == 'POST':
        personalities = request.json
        save_personalities(personalities)
        return jsonify({'status': 'success'})

@app.route('/api/personality/<personality_id>', methods=['DELETE'])
def api_delete_personality(personality_id):
    """Delete a personality"""
    personalities = load_personalities()
    if personality_id in personalities and personality_id not in ['sylvia_default', 'professional', 'casual_friend', 'tech_expert']:
        del personalities[personality_id]
        save_personalities(personalities)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Cannot delete default personality'})

@app.route('/api/upload_pdf', methods=['POST'])
def upload_pdf():
    """Upload PDF file"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return jsonify({'status': 'success', 'filename': filename})
    
    return jsonify({'status': 'error', 'message': 'Invalid file type'})

@app.route('/api/delete_pdf', methods=['POST'])
def delete_pdf():
    """Delete PDF file"""
    data = request.json
    filepath = data.get('path')
    
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/api/pdfs')
def api_pdfs():
    """Get PDF list"""
    return jsonify(get_pdf_list())

@app.route('/api/accounts', methods=['GET', 'POST'])
def api_accounts():
    """Bot accounts management"""
    if request.method == 'GET':
        return jsonify(get_accounts())
    
    elif request.method == 'POST':
        accounts = request.json
        save_accounts(accounts)
        return jsonify({'status': 'success'})

@app.route('/api/bot/status')
def bot_status():
    """Get bot status"""
    # This would be enhanced to check actual bot processes
    return jsonify({
        'running': False,  # Placeholder
        'uptime': '0:00:00',
        'active_sessions': 0,
        'messages_today': 0
    })

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    """Start the bot"""
    # This would start the main bot process
    return jsonify({'status': 'success', 'message': 'Bot start command sent'})

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    # This would stop the main bot process
    return jsonify({'status': 'success', 'message': 'Bot stop command sent'})

@app.route('/api/logs')
def get_logs():
    """Get bot logs"""
    # This would return actual bot logs
    return jsonify({
        'logs': [
            {'timestamp': '2024-01-01 12:00:00', 'level': 'INFO', 'message': 'Bot started'},
            {'timestamp': '2024-01-01 12:01:00', 'level': 'INFO', 'message': 'Connected to Telegram'},
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Telegram AI Bot Dashboard...")
    print("📊 Dashboard will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
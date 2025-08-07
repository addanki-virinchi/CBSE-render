#!/usr/bin/env python3
"""
Main application entry point for Render.com deployment
Provides a web interface for the school scraper
"""

import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
import threading
import time
from datetime import datetime
import glob

# Import scraper components
from sequential_process_state import SequentialStateProcessor
from render_config import render_config

# Setup logging
logging.basicConfig(
    level=getattr(logging, render_config.get_config('LOG_LEVEL', 'INFO')),
    format=render_config.get_config('LOG_FORMAT', '%(asctime)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables for scraper status
scraper_status = {
    'running': False,
    'current_state': None,
    'progress': 0,
    'total_states': 0,
    'completed_states': [],
    'failed_states': [],
    'start_time': None,
    'logs': []
}

def add_log(message):
    """Add a log message to the status"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    scraper_status['logs'].append(log_entry)
    # Keep only last 100 log entries
    if len(scraper_status['logs']) > 100:
        scraper_status['logs'] = scraper_status['logs'][-100:]
    logger.info(message)

def run_scraper_task(target_states=None):
    """Run the scraper in a background thread"""
    try:
        scraper_status['running'] = True
        scraper_status['start_time'] = datetime.now()
        add_log("🚀 Starting school data scraper...")
        
        # Initialize processor
        processor = SequentialStateProcessor()
        
        if target_states:
            scraper_status['total_states'] = len(target_states)
            add_log(f"📋 Processing {len(target_states)} selected states")
        else:
            scraper_status['total_states'] = len(processor.states_list)
            add_log(f"📋 Processing all {len(processor.states_list)} states")
        
        # Process states
        for i, state_name in enumerate(target_states or processor.states_list):
            if not scraper_status['running']:  # Check if stopped
                break
                
            scraper_status['current_state'] = state_name
            scraper_status['progress'] = i
            add_log(f"🏛️ Processing state {i+1}/{scraper_status['total_states']}: {state_name}")
            
            try:
                success = processor.process_complete_state(state_name)
                if success:
                    scraper_status['completed_states'].append(state_name)
                    add_log(f"✅ Completed {state_name}")
                else:
                    scraper_status['failed_states'].append(state_name)
                    add_log(f"❌ Failed {state_name}")
            except Exception as e:
                scraper_status['failed_states'].append(state_name)
                add_log(f"❌ Error processing {state_name}: {str(e)}")
        
        # Final summary
        completed = len(scraper_status['completed_states'])
        failed = len(scraper_status['failed_states'])
        add_log(f"🎯 Scraping completed: {completed} successful, {failed} failed")
        
    except Exception as e:
        add_log(f"❌ Scraper error: {str(e)}")
    finally:
        scraper_status['running'] = False
        scraper_status['current_state'] = None

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current scraper status"""
    return jsonify(scraper_status)

@app.route('/api/start', methods=['POST'])
def start_scraper():
    """Start the scraper"""
    if scraper_status['running']:
        return jsonify({'error': 'Scraper is already running'}), 400
    
    data = request.get_json() or {}
    target_states = data.get('states', None)
    
    # Reset status
    scraper_status.update({
        'running': True,
        'current_state': None,
        'progress': 0,
        'total_states': 0,
        'completed_states': [],
        'failed_states': [],
        'logs': []
    })
    
    # Start scraper in background thread
    thread = threading.Thread(target=run_scraper_task, args=(target_states,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scraper started successfully'})

@app.route('/api/stop', methods=['POST'])
def stop_scraper():
    """Stop the scraper"""
    scraper_status['running'] = False
    add_log("🛑 Scraper stop requested")
    return jsonify({'message': 'Scraper stop requested'})

@app.route('/api/files')
def list_files():
    """List available output files"""
    try:
        files = []
        patterns = ['*.csv', '*.xlsx']
        
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                file_info = {
                    'name': os.path.basename(file_path),
                    'size': os.path.getsize(file_path),
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
                files.append(file_info)
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """Download a file"""
    try:
        # Security check - only allow CSV and Excel files
        if not (filename.endswith('.csv') or filename.endswith('.xlsx')):
            return jsonify({'error': 'Invalid file type'}), 400
        
        if not os.path.exists(filename):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/states')
def get_states():
    """Get list of available states"""
    processor = SequentialStateProcessor()
    return jsonify({'states': processor.states_list})

@app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'config': {
            'headless': render_config.get_config('HEADLESS'),
            'render_deployment': render_config.get_config('RENDER_DEPLOYMENT')
        }
    })

if __name__ == '__main__':
    # Create output directory
    output_dir = render_config.get_config('OUTPUT_DIRECTORY', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Log startup information
    add_log("🚀 School Scraper Web App starting... (v2.0 - Fixed AttributeError)")
    add_log(f"📁 Output directory: {output_dir}")
    add_log(f"🔧 Headless mode: {render_config.get_config('HEADLESS')}")
    add_log(f"🌐 Render deployment: {render_config.get_config('RENDER_DEPLOYMENT')}")
    
    # Start Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

#!/usr/bin/env python3
"""
Local development server for testing the webhook functionality
This runs a simple HTTP server that mimics Vercel's function behavior
"""

import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the webhook handler
from api.webhook import handler as WebhookHandler

class LocalWebhookHandler(BaseHTTPRequestHandler):
    """Local development wrapper for the Vercel webhook handler"""
    
    def do_GET(self):
        # Create an instance of the webhook handler and call its do_GET method
        webhook_handler = WebhookHandler()
        # Copy necessary attributes
        webhook_handler.headers = self.headers
        webhook_handler.rfile = self.rfile
        webhook_handler.wfile = self.wfile
        webhook_handler.send_response = self.send_response
        webhook_handler.send_header = self.send_header
        webhook_handler.end_headers = self.end_headers
        
        webhook_handler.do_GET()
    
    def do_POST(self):
        # Create an instance of the webhook handler and call its do_POST method
        webhook_handler = WebhookHandler()
        # Copy necessary attributes
        webhook_handler.headers = self.headers
        webhook_handler.rfile = self.rfile
        webhook_handler.wfile = self.wfile
        webhook_handler.send_response = self.send_response
        webhook_handler.send_header = self.send_header
        webhook_handler.end_headers = self.end_headers
        
        webhook_handler.do_POST()

def run_server(port=8000):
    """Run local development server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, LocalWebhookHandler)
    
    print(f"🚀 Local webhook server running on http://localhost:{port}")
    print(f"📱 Health check: http://localhost:{port}")
    print(f"🔗 Webhook endpoint: http://localhost:{port}/api/webhook")
    print("🔄 Use ngrok to expose this to the internet for Telegram webhook testing")
    print("   Example: ngrok http 8000")
    print("\n⚡ Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Local development server for Telegram webhook")
    parser.add_argument("--port", type=int, default=8000, help="Port to run server on (default: 8000)")
    
    args = parser.parse_args()
    
    # Check environment variables
    required_vars = ["OPENAI_API_KEY", "OPENAI_ORG_ID", "TELEGRAM_BOT_TOKEN"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set these in your .env file or environment for full functionality")
    
    run_server(args.port)
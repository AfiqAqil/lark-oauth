#!/usr/bin/env python3
"""
Main script to start both frontend and backend servers for Lark OAuth Integration.
This script fulfills the requirement of having only one main script to start everything.
"""

import subprocess
import sys
import time
import threading
import argparse
import signal
import os

# Import centralized logger
sys.path.append('.')
from app.core.logger import logger

# Default configurations
DEFAULT_BACKEND_PORT = 8000
DEFAULT_FRONTEND_PORT = 3000
DEFAULT_BACKEND_HOST = "localhost"

class ServerManager:
    """Manages both frontend and backend servers."""
    
    def __init__(self, backend_port=DEFAULT_BACKEND_PORT, frontend_port=DEFAULT_FRONTEND_PORT, backend_host=DEFAULT_BACKEND_HOST):
        self.backend_port = backend_port
        self.frontend_port = frontend_port
        self.backend_host = backend_host
        self.backend_process = None
        self.frontend_process = None
        self.running = False
        
    def start_backend(self):
        """Start the backend server."""
        try:
            cmd = [
                sys.executable, "-m", "uvicorn", "app.main:app",
                "--host", self.backend_host,
                "--port", str(self.backend_port),
                "--reload"
            ]
            
            logger.info(f"Starting backend server at http://{self.backend_host}:{self.backend_port}")
            self.backend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Monitor backend output
            for line in iter(self.backend_process.stdout.readline, ''):
                if self.running and line.strip():
                    logger.info(f"[BACKEND] {line.strip()}")
                    
        except Exception as e:
            logger.error(f"Failed to start backend server: {e}")
            
    def start_frontend(self):
        """Start the frontend server."""
        try:
            # Wait a bit for backend to start
            time.sleep(2)
            
            cmd = [sys.executable, "-m", "scripts.run_frontend", "--port", str(self.frontend_port)]
            
            logger.info(f"Starting frontend server at http://localhost:{self.frontend_port}")
            self.frontend_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Monitor frontend output
            for line in iter(self.frontend_process.stdout.readline, ''):
                if self.running and line.strip():
                    logger.info(f"[FRONTEND] {line.strip()}")
                    
        except Exception as e:
            logger.error(f"Failed to start frontend server: {e}")
            
    def start_servers(self):
        """Start both servers."""
        self.running = True
        
        # Check if static directory exists
        if not os.path.exists("static"):
            logger.error("❌ Static directory not found. Please ensure you're running from the project root.")
            return False
            
        # Check if .env file exists
        if not os.path.exists(".env"):
            logger.warning("⚠️  No .env file found. Please create one with your Lark app credentials.")
            logger.info("💡 See .env.example for the required format.")
            
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=self.start_backend, daemon=True)
        backend_thread.start()
        
        # Start frontend in a separate thread
        frontend_thread = threading.Thread(target=self.start_frontend, daemon=True)
        frontend_thread.start()
        
        # Print startup information with beautiful formatting
        logger.success("=" * 60)
        logger.success("🚀 Lark OAuth Integration Started Successfully!")
        logger.success("=" * 60)
        logger.info(f"📱 Frontend: http://localhost:{self.frontend_port}")
        logger.info(f"🔧 Backend:  http://{self.backend_host}:{self.backend_port}")
        logger.info(f"📚 API Docs: http://{self.backend_host}:{self.backend_port}/docs")
        logger.success("=" * 60)
        logger.warning("Press Ctrl+C to stop both servers")
        logger.success("=" * 60)
        
        return True
        
    def stop_servers(self):
        """Stop both servers."""
        self.running = False
        
        if self.backend_process:
            logger.warning("🛑 Stopping backend server...")
            self.backend_process.terminate()
            
        if self.frontend_process:
            logger.warning("🛑 Stopping frontend server...")
            self.frontend_process.terminate()
            
        logger.success("✅ Both servers stopped successfully.")

def signal_handler(signum, frame, server_manager):
    """Handle Ctrl+C gracefully."""
    logger.warning("\n⚠️  Received interrupt signal. Shutting down servers...")
    server_manager.stop_servers()
    logger.success("👋 Goodbye!")
    sys.exit(0)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Start Lark OAuth Integration (Frontend + Backend)")
    parser.add_argument("--backend-port", type=int, default=DEFAULT_BACKEND_PORT, 
                       help=f"Backend port (default: {DEFAULT_BACKEND_PORT})")
    parser.add_argument("--frontend-port", type=int, default=DEFAULT_FRONTEND_PORT, 
                       help=f"Frontend port (default: {DEFAULT_FRONTEND_PORT})")
    parser.add_argument("--backend-host", type=str, default=DEFAULT_BACKEND_HOST, 
                       help=f"Backend host (default: {DEFAULT_BACKEND_HOST})")
    
    args = parser.parse_args()
    
    # Create server manager
    server_manager = ServerManager(
        backend_port=args.backend_port,
        frontend_port=args.frontend_port,
        backend_host=args.backend_host
    )
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, server_manager))
    
    # Start servers
    if server_manager.start_servers():
        try:
            # Keep the main thread alive
            while server_manager.running:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None, server_manager)
    else:
        logger.error("Failed to start servers")
        sys.exit(1)

if __name__ == "__main__":
    main() 
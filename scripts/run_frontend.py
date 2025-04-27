import http.server
import socketserver
import os
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Default port
DEFAULT_PORT = 3000
DEFAULT_DIRECTORY = "static"

class FrontendHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DEFAULT_DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)

def run_server(port=DEFAULT_PORT):
    """Start the frontend server."""
    handler = FrontendHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        logger.info(f"Serving frontend at http://localhost:{port}")
        logger.info("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the frontend server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the server on (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    
    # Check if static directory exists
    if not os.path.exists(DEFAULT_DIRECTORY):
        logger.error(f"Directory '{DEFAULT_DIRECTORY}' not found")
        exit(1)
        
    run_server(args.port) 
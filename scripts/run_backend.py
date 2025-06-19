import subprocess
import sys
import argparse

# Import centralized logger
sys.path.append('.')
from app.core.logger import logger

# Default port
DEFAULT_PORT = 8000
DEFAULT_HOST = "localhost"

def run_backend(host=DEFAULT_HOST, port=DEFAULT_PORT, reload=True):
    """Start the backend server using uvicorn."""
    try:
        cmd = [
            sys.executable, "-m", "uvicorn", "app.main:app",
            "--host", host,
            "--port", str(port)
        ]
        
        if reload:
            cmd.append("--reload")
            
        logger.info(f"Starting backend server at http://{host}:{port}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start backend server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Backend server stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the backend server")
    parser.add_argument("--host", type=str, default=DEFAULT_HOST, help=f"Host to run the server on (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to run the server on (default: {DEFAULT_PORT})")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload on code changes")
    
    args = parser.parse_args()
    
    run_backend(args.host, args.port, not args.no_reload) 
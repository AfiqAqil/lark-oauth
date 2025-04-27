# Lark OAuth Integration

A simple FastAPI application for demonstrating Lark (Feishu) OAuth 2.0 authentication.

## Project Structure

```
lark-oauth/
├── app/                  # Backend application
│   ├── api/              # API endpoints
│   │   ├── endpoints/    # API route handlers
│   │   └── router.py     # Main API router
│   ├── core/             # Core components
│   │   ├── config.py     # Application settings
│   │   └── models.py     # Data models
│   ├── services/         # Business logic
│   │   └── lark_service.py  # Lark API integration
│   └── main.py           # FastAPI application entry point
├── static/               # Frontend static files
│   ├── scripts/          # JavaScript files
│   ├── index.html        # Main login page
│   ├── login-success.html # Login success page
│   └── styles.css        # CSS styles
├── scripts/              # Utility scripts
│   ├── run_backend.py    # Script to run the backend
│   └── run_frontend.py   # Script to run the frontend
└── requirements/         # Python dependencies
    ├── base.txt          # Production dependencies
    └── dev.txt           # Development dependencies
```

## Prerequisites

- Python 3.8 or higher
- Lark developer account with a created application
- Application credentials (App ID and App Secret) from Lark developer console

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/lark-oauth.git
cd lark-oauth
```

2. **Create and activate a virtual environment**

```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements/dev.txt
```

4. **Create a .env file**

Create a `.env` file in the root directory with the following content:

```
# Application settings
BACKEND_CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
FRONTEND_URL="http://localhost:3000"

# Lark OAuth settings
LARK_APP_ID="your_lark_app_id_here"
LARK_APP_SECRET="your_lark_app_secret_here"
LARK_BASE_URL="https://open.larksuite.com"
REDIRECT_URI="http://localhost:8000/api/auth/user/lark/callback"
```

Replace `your_lark_app_id_here` and `your_lark_app_secret_here` with your actual Lark application credentials.

5. **Configure your Lark application**

In your Lark developer console:
- Add the redirect URI: `http://localhost:8000/api/auth/user/lark/callback`
- Enable the required permissions:
  - Read basic information of the user
  - Get user email

## Running the Application

You can run the application in two different ways:

### Option 1: Single Instance (Backend + Frontend)

```bash
# Start the FastAPI server with static file mounting
python -m app.main
```

Access the application at `http://localhost:8000/static/index.html`

### Option 2: Separate Instances (Recommended)

1. **Start the Backend Server**

```bash
# Using the helper script
python -m scripts.run_backend

# Or directly with uvicorn
uvicorn app.main:app --host localhost --port 8000 --reload
```

2. **Start the Frontend Server**

```bash
# Using the helper script
python -m scripts.run_frontend

# By default, the frontend runs on port 3000
```

3. **Access the application**

Open your browser and navigate to:
```
http://localhost:3000
```

## API Endpoints

- `GET /api/auth/user/lark/login` - Redirects to Lark for authentication
- `GET /api/auth/user/lark/callback` - Handles the callback from Lark
- `POST /api/auth/user/lark/refresh` - Refreshes the access token
- `GET /api/user/{user_id}` - Gets user information by ID

## Authentication Flow

1. User clicks "Login with Lark" button
2. Backend redirects to Lark authorization page
3. User authorizes the application
4. Lark redirects back with an authorization code
5. Backend exchanges code for access token
6. Backend fetches user info and creates/updates user record
7. User is redirected to success page with user information

## Error Handling

The application handles various errors, including:
- Invalid authorization codes
- Expired tokens
- Network errors
- Missing user information

## License

MIT

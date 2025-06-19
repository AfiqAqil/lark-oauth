# Lark OAuth Integration

A simple FastAPI application for demonstrating Lark (Feishu) OAuth 2.0 authentication.

## ✨ Quick Start

**One command to start everything:**

```bash
python run.py
```

That's it! 🚀 The script will start both frontend and backend servers automatically.

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

Copy the example environment file and fill in your Lark app credentials:

```bash
cp .env.example .env
```

Then edit `.env` and replace the placeholder values:
- `LARK_APP_ID` - Your Lark App ID from the developer console
- `LARK_APP_SECRET` - Your Lark App Secret from the developer console

💡 **Tip**: The `.env.example` file contains detailed setup instructions for the Lark Developer Console.

5. **Configure your Lark application**

In your Lark developer console (detailed instructions in `.env.example`):
- Add the redirect URI: `http://localhost:8000/api/auth/user/lark/callback`
- Enable the required permissions:
  - `contact:user.id:readonly` - Get user ID
  - `contact:user.email:readonly` - Get user email
  - `contact:user.avatar:readonly` - Get user avatar

## Running the Application

### 🎯 Recommended: Single Command Start

```bash
python run.py
```

This starts both frontend and backend servers automatically:
- 📱 **Frontend**: http://localhost:3000
- 🔧 **Backend**: http://localhost:8000  
- 📚 **API Docs**: http://localhost:8000/docs

### Alternative: Manual Start (Advanced Users)

If you prefer to run servers separately:

```bash
# Terminal 1: Backend
python -m scripts.run_backend

# Terminal 2: Frontend  
python -m scripts.run_frontend
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

## 🎯 Project Goals & Features

This project demonstrates a complete Lark OAuth integration with the following features:

### ✅ **Single Command Startup**
- **Goal**: Only requires one main script to start frontend and backend
- **Solution**: `python run.py` starts both servers automatically
- **Benefits**: Simplified development workflow, no need to manage multiple terminals

### ✅ **Developer-Friendly Setup**
- **Goal**: Guide developers on how to setup Lark OAuth (including code)
- **Solution**: Comprehensive `.env.example` with step-by-step Lark console setup
- **Benefits**: Clear instructions reduce setup time and confusion

### ✅ **Clean Frontend with Guidance**
- **Goal**: Simple yet clean frontend with helpful guidance
- **Solution**: Modern UI with explanations, emojis, and clear user flow
- **Benefits**: Users understand what's happening during OAuth flow

### ✅ **Up-to-Date Documentation**
- **Goal**: README is comprehensive and current
- **Solution**: Restructured README with quick start, detailed setup, and troubleshooting
- **Benefits**: Developers can get started quickly and find help when needed

## 🚀 What You Get

- **Complete OAuth 2.0 Flow**: Authorization code flow with PKCE
- **Token Management**: Automatic refresh and secure storage
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Modern UI**: Clean, responsive interface with helpful guidance
- **Developer Experience**: One-command startup with beautiful colored logging (loguru)
- **Production Ready**: Proper error handling, file logging, and security practices

## 📚 API Endpoints

- `GET /api/auth/user/lark/login` - Redirects to Lark for authentication
- `GET /api/auth/user/lark/callback` - Handles the callback from Lark
- `POST /api/auth/user/lark/refresh` - Refreshes the access token
- `GET /api/user/{user_id}` - Gets user information by ID
- `GET /docs` - Interactive API documentation (Swagger UI)

## 🔧 Troubleshooting

**Common Issues:**

1. **"Failed to get app access token"**
   - Check your `LARK_APP_ID` and `LARK_APP_SECRET` in `.env`
   - Ensure credentials are from the correct Lark app

2. **"Redirect URI mismatch"**
   - Verify redirect URI in Lark console matches: `http://localhost:8000/api/auth/user/lark/callback`

3. **"Permission denied"**
   - Enable required permissions in Lark console (see `.env.example` for details)

4. **Frontend not loading**
   - Ensure you're running from the project root directory
   - Check that `static/` directory exists

5. **Need more debugging info?**
   - Check the `logs/lark_oauth.log` file for detailed debug information
   - Logs are automatically rotated (10MB max, 7 days retention)
   - Console output shows colored, real-time logging with loguru

## License

MIT

document.addEventListener('DOMContentLoaded', () => {
    const loginButton = document.getElementById('larkLoginBtn');
    
    // Get backend URL from environment or use default
    const backendUrl = window.BACKEND_URL || 'http://localhost:8000';
    
    // Check if already authenticated
    const authData = localStorage.getItem('larkAuthData');
    if (authData) {
        try {
            const parsedData = JSON.parse(authData);
            const expiresAt = new Date(parsedData.expires_at);
            
            // If token not expired, redirect to success page
            if (expiresAt > new Date()) {
                window.location.href = '/login-success.html';
                return;
            } else {
                // Clear expired tokens
                localStorage.removeItem('larkAuthData');
                localStorage.removeItem('larkUserData');
            }
        } catch (error) {
            console.error('Error parsing auth data:', error);
            localStorage.removeItem('larkAuthData');
            localStorage.removeItem('larkUserData');
        }
    }
    
    // Add click event to login button
    loginButton.addEventListener('click', () => {
        // Redirect to backend login endpoint
        window.location.href = `${backendUrl}/api/auth/user/lark/login`;
    });
}); 
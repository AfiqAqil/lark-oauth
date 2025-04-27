document.addEventListener('DOMContentLoaded', async () => {
    const userInfoContainer = document.getElementById('userInfo');
    const loadingMessage = document.getElementById('loadingMessage');
    const userName = document.getElementById('userName');
    const userEmail = document.getElementById('userEmail');
    const userId = document.getElementById('userId');
    const avatarContainer = document.getElementById('avatarContainer');
    const logoutBtn = document.getElementById('logoutBtn');
    
    // Get backend URL from environment or use default
    const backendUrl = window.BACKEND_URL || 'http://localhost:8000';
    
    // Function to get URL parameters
    function getUrlParameter(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }
    
    // Check if we have a user ID from URL parameters
    const userIdFromUrl = getUrlParameter('userId');
    
    if (userIdFromUrl) {
        try {
            // Fetch user data from backend
            const response = await fetch(`${backendUrl}/api/user/${userIdFromUrl}`);
            if (!response.ok) {
                throw new Error('Failed to fetch user data');
            }
            
            const userData = await response.json();
            
            // Store user data in localStorage
            localStorage.setItem('larkUserData', JSON.stringify(userData.user));
            localStorage.setItem('larkAuthData', JSON.stringify(userData.auth));
            
            // Display user information
            displayUserInfo(userData.user);
        } catch (error) {
            console.error('Error fetching user data:', error);
            loadingMessage.textContent = 'Error loading user information. Please try again.';
        }
    } else {
        // Check if we have user data in localStorage
        const storedUserData = localStorage.getItem('larkUserData');
        if (storedUserData) {
            try {
                const userData = JSON.parse(storedUserData);
                displayUserInfo(userData);
            } catch (error) {
                console.error('Error parsing user data:', error);
                loadingMessage.textContent = 'Error loading user information. Please try again.';
            }
        } else {
            loadingMessage.textContent = 'No user information found. Please log in again.';
        }
    }
    
    // Function to display user information
    function displayUserInfo(user) {
        // Hide loading message
        loadingMessage.style.display = 'none';
        
        // Set user info
        userName.textContent = user.name || 'N/A';
        userEmail.textContent = user.email || 'N/A';
        userId.textContent = user.id || 'N/A';
        
        // Set avatar if available
        if (user.avatar_url) {
            const avatar = document.createElement('img');
            avatar.src = user.avatar_url;
            avatar.alt = 'User Avatar';
            avatar.className = 'avatar';
            avatarContainer.appendChild(avatar);
        }
        
        // Show user info container
        userInfoContainer.style.display = 'block';
    }
    
    // Logout function
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('larkAuthData');
        localStorage.removeItem('larkUserData');
        window.location.href = '/index.html';
    });
    
    // Token refresh logic
    async function refreshToken() {
        try {
            const authData = localStorage.getItem('larkAuthData');
            if (!authData) return;
            
            const parsedAuthData = JSON.parse(authData);
            const expiresAt = new Date(parsedAuthData.expires_at);
            
            // Check if token is about to expire (less than 5 minutes)
            const fiveMinutesFromNow = new Date();
            fiveMinutesFromNow.setMinutes(fiveMinutesFromNow.getMinutes() + 5);
            
            if (expiresAt <= fiveMinutesFromNow) {
                console.log('Token is about to expire, refreshing...');
                
                const refreshResponse = await fetch(`${backendUrl}/api/auth/user/lark/refresh`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        refresh_token: parsedAuthData.refresh_token
                    })
                });
                
                if (!refreshResponse.ok) {
                    throw new Error('Failed to refresh token');
                }
                
                const newTokenData = await refreshResponse.json();
                
                // Update stored auth data
                localStorage.setItem('larkAuthData', JSON.stringify(newTokenData));
                console.log('Token refreshed successfully');
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
        }
    }
    
    // Check and refresh token on page load
    refreshToken();
    
    // Set up periodic token check (every 4 minutes)
    setInterval(refreshToken, 4 * 60 * 1000);
}); 
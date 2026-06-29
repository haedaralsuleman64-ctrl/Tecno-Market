function initGoogleAuth() {
    gapi.load('auth2', function() {
        gapi.auth2.init({
            client_id: 'YOUR_GOOGLE_CLIENT_ID',
            cookiepolicy: 'single_host_origin',
        });
    });
}

function googleLogin() {
    const auth2 = gapi.auth2.getAuthInstance();
    auth2.signIn().then(function(googleUser) {
        const profile = googleUser.getBasicProfile();
        const authResponse = googleUser.getAuthResponse();
        
        // إرسال البيانات إلى الخادم
        const formData = new FormData();
        formData.append('access_token', authResponse.access_token);
        formData.append('csrfmiddlewaretoken', getCSRFToken());
        
        fetch('/social-auth/google/callback/', {
            method: 'POST',
            body: formData,
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during login');
        });
    }).catch(function(error) {
        console.error('Google Sign-In Error:', error);
    });
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue;
}

// تحميل Google API
(function() {
    const script = document.createElement('script');
    script.src = 'https://apis.google.com/js/platform.js?onload=initGoogleAuth';
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
})();
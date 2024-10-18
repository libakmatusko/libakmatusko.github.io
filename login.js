document.getElementById('loginBtn').addEventListener('click', function() {
    // Get input values
    const teamName = document.getElementById('teamName').value;
    const password = document.getElementById('password').value;

    // Create login data object
    const loginData = {
        name: teamName,
        password: password
    };

    // Send login request to the server
    fetch('https://matuslibak.pythonanywhere.com/login_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: teamName, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Store the team information in localStorage
            localStorage.setItem('loggedInTeam', JSON.stringify(data.user));
            
            // Redirect to problem submission page
            window.location.href = 'problem.html';
        } else {
            // Handle error
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
    
});

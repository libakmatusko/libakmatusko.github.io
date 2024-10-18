document.getElementById('addMemberBtn').addEventListener('click', function() {
    const memberInputs = document.getElementById('memberInputs');
    
    // Create a new input field and button
    const newMemberDiv = document.createElement('div');
    newMemberDiv.classList.add('member-input');

    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.placeholder = `Člen ${memberInputs.children.length + 1}`;
    newInput.required = true;

    const removeBtn = document.createElement('button');
    removeBtn.textContent = 'Odstrániť';
    removeBtn.classList.add('removeMemberBtn');

    // Add event listener to remove button
    removeBtn.addEventListener('click', function() {
        memberInputs.removeChild(newMemberDiv);
    });

    newMemberDiv.appendChild(newInput);
    newMemberDiv.appendChild(removeBtn);
    memberInputs.appendChild(newMemberDiv);
});

document.getElementById('registerBtn').addEventListener('click', function() {
    // Get input values
    const teamName = document.getElementById('teamName').value;
    const password = document.getElementById('password').value;

    // Get member inputs
    const memberInputs = document.querySelectorAll('.member-input input');
    const members = Array.from(memberInputs).map(input => input.value).filter(member => member);

    // Create JSON object
    const userData = {
        name: teamName,
        password: password,
        members: members,
        scores: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        time: 0.0,
        wrong_answers: 0
    };

    console.log("Generated JSON:", JSON.stringify(userData)); // For debugging

    // Send data to the server or handle it accordingly
    fetch('https://matuslibak.pythonanywhere.com/add_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = "dashboard.html"; // Change as needed
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

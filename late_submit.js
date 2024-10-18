function getCompetitionDay() {
    const startDate = new Date('2024-10-10T06:00:00'); // Competition start date
    const now = new Date();
    const differenceInDays = Math.floor((now - startDate) / (1000 * 60 * 60 * 24));
    return differenceInDays + 1;
}
console.log('Submitting answer for team:', JSON.parse(localStorage.getItem('loggedInTeam')).name );
console.log('funguje')
const daySelect = document.getElementById('daySelect');
const currentDay = getCompetitionDay(); // Assuming this returns the current day of the competition

// Populate day options from 1 to today - 1
for (let day = 1; day < currentDay; day++) {
    const option = document.createElement('option');
    option.value = day;
    option.textContent = `Day ${day}`; // Use textContent instead
    daySelect.appendChild(option);
}

// Submit late answer event
document.getElementById('submitLateAnswerBtn').addEventListener('click', function() {
    const selectedDay = daySelect.value;
    const answer = document.getElementById('lateAnswer').value;

    if (!answer) {
        alert('Please enter an answer.');
        return;
    }

    // Send the late answer to the server
    fetch('https://matuslibak.pythonanywhere.com/late_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            day: selectedDay,
            answer: answer,
            name: JSON.parse(localStorage.getItem('loggedInTeam')).name // Assuming team is stored as JSON
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.isCorrect) {
            alert('Answer submitted successfully and it is correct!');
        } else {
            alert('Answer submitted successfully but it is incorrect.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to submit answer. Please try again.');
    });
});


// Download problem from the selected day
document.getElementById('downloadLateProblemBtn').addEventListener('click', function() {
    const selectedDay = daySelect.value;
    const fileName = `problem_day_${selectedDay}.pdf`; // Adjust file extension accordingly
    const filePath = `problems/${fileName}`;

    const link = document.createElement('a');
    link.href = filePath;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); // Clean up
});



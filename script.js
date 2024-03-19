// Get the filename from the URL
const url = window.location.pathname;
const filename = url.substring(url.lastIndexOf('/') + 1);

//const dotenv = require('dotenv');
//detenv.config();
//const apiKey = process.env.API_KEY;

// Get the form and attach an event listener
const questionForm = document.getElementById("question_form");
questionForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get the user's question input
    const questionInput = document.getElementById("question");

    // Check if the user input is not the default placeholder
    if (questionInput.value !== "tu napíš svoju otázku") {
        // Append topic based on the current page
        switch (filename) {
            case "pythagoras.html":
                questionInput.value = `Mám otázku ohľadom Pytagorovho trojuholníka: ${questionInput.value}`;
                break;
            case "icosahedron.html":
                questionInput.value = `Mám otázku ohľadom Ikosahedronu: ${questionInput.value}`;
                break;
            case "tetrahedron.html":
                questionInput.value = `Mám otázku ohľadom Tetrahedronu: ${questionInput.value}`;
                break;
            case "aurora.html":
                questionInput.value = `Mám otázku ohľadom polárnej žiary: ${questionInput.value}`;
                break;
            // Add more cases for other pages if needed
        }

        // Prepare the request to the OpenAI API
        const request = new Request('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            mode: 'cors',
            redirect: 'follow',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
            }),
            body: JSON.stringify({
                "model": "gpt-3.5-turbo",
                "messages": [{ "role": "user", "content": questionInput.value }],
                "temperature": 0.7,
            }),
        });

        console.log('API Request:', request);

        try {
            // Make the API request and handle the response
            const response = await fetch(request);
            console.log(response);
            const jsonResponse = await response.json();
            console.log(jsonResponse)
            const answer = jsonResponse.choices[0].message.content;

            // Log the input, output, and display the answer
            console.log(questionInput.value);
            console.log(answer);
            document.getElementById("answer").innerText = answer;
        } catch (error) {
            console.error('Error:', error);
        }
    }
});

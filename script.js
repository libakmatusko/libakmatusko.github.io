var url = window.location.pathname;
var filename = url.substring(url.lastIndexOf('/')+1);
//alert(filename);

let questionForm = document.getElementById("question_form");
questionForm.addEventListener("submit", (e) =>  {
    e.preventDefault();

    var question = document.getElementById("question");
    if (question.value != "tu napíš svoju otázku") {
        //tu sa podla stranky dopise pre otazku o akej je teme
        switch(filename) {
            case "pythagoras.html":
                question.value = "Mám otáazku ohľadom pytagorovho trojuholníka: " + question.value
                break;
            case "icosahedron.html":
                question.value = "Mám otáazku ohľadom Ikosahedronu: " + question.value
                break;
            case "tetrahedron.html":
                question.value = "Mám otáazku ohľadom Tetrahedronu: " + question.value
                break;
        }
        // tu sa bude spracovavat request s API
        const apiKey = process.env.API_KEY;
        console.log('OpenAI API Key:', apiKey);
        var request = new Request('https://api.openai.com/v1/chat/completions', {
    method: 'POST', 
    mode: 'cors', 
    redirect: 'follow',
    headers: new Headers({
        'Content-Type': 'application/json',
    "Authorization": apiKey
    }),
  body: JSON.stringify({
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": question.value}],
"temperature": 0.7
   })
});
fetch(request).then(function(response) { 
    // Convert to JSON
    return response.json();
}).then(function(j) {
    // Yay, j is a JavaScript object
    console.log(j)
    answer = j["choices"][0]["message"]["content"]
        //question je vstup
        console.log(question.value)
        //answer buder vystup.
        console.log(answer)
        document.getElementById("answer").innerText = answer;
});
    }
})
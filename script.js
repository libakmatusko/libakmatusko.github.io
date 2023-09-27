var url = window.location.pathname;
var filename = url.substring(url.lastIndexOf('/')+1);
alert(filename);

let questionForm = document.getElementById("question_form");
questionForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let question = document.getElementById("question");
    if (question.value != "tu napíš svoju otázku") {
        // tu sa bude spracovavat request s API
        switch(filename) {
            case "pythagoras.html":
                question = "Mám otáazku ohľadom pytagorvho trojuholníka: " + queastion
                break;
        }
        //question je vstup
        console.log(question.value)
        //answer buder vystup.
        let answer = "Odpoved od chat GPT"
        console.log(answer)
        document.getElementById("answer").innerText = answer;
    }
})

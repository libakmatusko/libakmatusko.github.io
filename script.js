var url = window.location.pathname;
alert(url.substring(url.lastIndexOf('/')+1));

let questionForm = document.getElementById("question_form");
questionForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let question = document.getElementById("question");
    if (question.value != "tu napíš svoju otázku") {
        // tu sa bude spracovavat request s API
        //question je vstup
        console.log(question.value)
        //answer buder vystup.
        let answer = "Odpoved od chat GPT"
        console.log(answer)
        document.getElementById("answer").innerText = answer;
    }
})

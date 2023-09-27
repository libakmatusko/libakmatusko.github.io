let questionForm = document.getElementById("question_form");
questionForm.addEventListener("submit", (e) => {
    e.preventDefault();

    let question = document.getElementById("question");
    if (question.value != "IDK") {
        // tu sa bude spracovavat request s API
        //question je vstup
        console.log(question.value)
        //answer buder vystup.
    }
});

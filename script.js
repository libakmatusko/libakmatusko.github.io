zobrazenie1 = true;
zobrazenie2 = true;
zobrazenie3 = true;
running = false;
run = false;
//pocet moznych blockov
pocetBlockov = 7
//spawn
stareCislo = 0
staronoveCislo = 0
mladeCislo = 0
noveCislo = 1
//score
score = 0
bestScore = 0
ScoreP = document.getElementById("score")
bestScoreP = document.getElementById("bestScore")
a = 0
//zrychlovanie
highSpeed = 1800
lowSpeed = 2000
function speed(highSpeed, lowSpeed){
    Speed = Math.random() * (lowSpeed - highSpeed) + highSpeed;
    console.log("speed of block: " + Speed)
    return Speed;
}
function acceleration(){

}
//veci na obrazovke
character = document.getElementById("character");
block1 = document.getElementById("block1");
block2 = document.getElementById("block2");
block3 = document.getElementById("block3");
block4 = document.getElementById("block4");
block5 = document.getElementById("block5");
block6 = document.getElementById("block6");
block7 = document.getElementById("block7");

function jump(){
    if(character.classList!= "animate"){
        character.classList.add("animate");
    }
    setTimeout(function(){
        character.classList.remove("animate")},400);
}
function restart(){
    score = 0
    a = 0
    zobrazenie1 = true;
    zobrazenie2 = true;
    zobrazenie3 = true;
    running = true;
    run = true;
    start()
}
async function start(){
    while (run==true) {
        speeed = ((Math.random() * 800) + 4000 - 300 - speed(highSpeed, lowSpeed)) / 2
        console.log("waiting: " + speeed)
        await sleep(speeed);
        noveCislo = Math.floor(Math.random()*7)+1
        while (stareCislo==noveCislo || staronoveCislo==noveCislo || mladeCislo==noveCislo){
            noveCislo = Math.floor(Math.random()*7)+1
        }
        stareCislo = staronoveCislo
        staronoveCislo = mladeCislo
        mladeCislo = noveCislo
        prekazka(noveCislo)
    }
}

function prekazka(cisloPrekazky){
    block = eval('block' + cisloPrekazky)
    if (block.hasAttribute("style")){
        block.removeAttribute("style")
    }
    block.style["animation-duration"] = speed(highSpeed, lowSpeed) + "ms";
    block.style["animation-timing-function"] = "linear";
    block.style["animation-name"] = "block";
    setTimeout(function(){
    blockStaly = eval('block' + cisloPrekazky)
    if (blockStaly.hasAttribute("style")){
        blockStaly.removeAttribute("style")
    }
    }, speed(highSpeed, lowSpeed))
}
function stop(){
    run = false
}
var checkDead  = setInterval(function(){
    
    charakterTop = parseInt(window.getComputedStyle(character).getPropertyValue("top"));
    blockLeft1 = parseInt(window.getComputedStyle(block1).getPropertyValue("left"));
    blockLeft2 = parseInt(window.getComputedStyle(block2).getPropertyValue("left"));
    blockLeft3 = parseInt(window.getComputedStyle(block3).getPropertyValue("left"));
    blockLeft4 = parseInt(window.getComputedStyle(block4).getPropertyValue("left"));
    blockLeft5 = parseInt(window.getComputedStyle(block5).getPropertyValue("left"));
    blockLeft6 = parseInt(window.getComputedStyle(block6).getPropertyValue("left"));
    blockLeft7 = parseInt(window.getComputedStyle(block7).getPropertyValue("left"));

    for (let i = 1; i<=7; i++){
        if(eval('blockLeft' + i)<40 && eval('blockLeft' + i)>0 && charakterTop>=260){
            prehra();
        }
    }
    if(running==true){
        a = a+1
        if(a==20){
            score = score+1
            ScoreP.innerText = score
            if(score % 100==0){
                highSpeed = highSpeed / 10 * 9
                lowSpeed = lowSpeed / 10 * 9
                console.log("hhhhhhhhhhhhhhhhhhhhhhhhh", highSpeed, lowSpeed)
            }
            a = 0
        }
    }
},10);

function prehra(){
    //best score
    if(score>bestScore){
        bestScore = score
        bestScoreP.innerText = bestScore
    }
    console.log("Score: " + score)
    console.log("Best score: " + bestScore)

    setTimeout(function(){
        for (let i = 1; i<=7; i++){
            if ((eval('block' + i).hasAttribute("style"))){
                (eval('block' + i).removeAttribute("style"))
            }
        }
    }, 200)
    a = 0;
    alert("you losed");
    running = false;
    stop()
}

//sleep
function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}
//pouzi va sa ako    await sleep(2000);

//download stranky
function download(fileUrl, fileName){
    A = document.createElement("A");
    A.href = fileUrl;
    A.setAttribute("download", fileName);
    A.click();
}
function Downloads(){
    download('index.html', 'index.html')
    download('platno_na_hrad.png', 'platno_na_hrad.png')
    download('script.js', 'script.js')
    download('style.css', 'style.css')
}
console.log("If you want files of this website tipe: Downloads() in console.")
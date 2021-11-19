zobrazenie1 = true;
zobrazenie2 = true;
zobrazenie3 = true;
running = false;
run = false;

pocetBlockov = 7

stareCislo = 0
staronoveCislo = 0
mladeCislo = 0
noveCislo = 1

score = 0
ScoreP = document.getElementById("score")
a = 0

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
    zobrazenie1 = true;
    zobrazenie2 = true;
    zobrazenie3 = true;
    running = true;
    run = true;
    start()
}
async function start(){
    while (run==true) {
        await sleep(1000);
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
    block.style.animation = "block 2s";
    block.style.animationTimingFunction = "linear";
    setTimeout(function(){
    blockStaly = eval('block' + cisloPrekazky)
    if (blockStaly.hasAttribute("style")){
        blockStaly.removeAttribute("style")
    }
    }, 2000)
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
        if(a==9){
            score = score+1
            ScoreP.innerText = score
            a = 0
        }
    }
},10);

function prehra(){
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
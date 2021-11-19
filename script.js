zobrazenie1 = true;
zobrazenie2 = true;
zobrazenie3 = true;

score = 0

character = document.getElementById("character");
block = document.getElementById("block");
block2 = document.getElementById("block2");
block3 = document.getElementById("block3");
function jump(){
    if(zobrazenie3==false && zobrazenie2==false && zobrazenie1==false){
        alert("You are pretty big looser!")
    }
    if(character.classList!= "animate"){
        character.classList.add("animate");
    }
    setTimeout(function(){
        character.classList.remove("animate")},500);
}
function restart(){
    zobrazenie1 = true;
    zobrazenie2 = true;
    zobrazenie3 = true;
    start()
}
function start(){
    if(zobrazenie1==true){
    prekazka1()}
    if(zobrazenie2==true){
    prekazka2()}
    if(zobrazenie3==true){
    prekazka3()}
}
function prekazka1(){
    block.style.animation = "block 2s infinite";
    block.style.animationTimingFunction = "linear";
}
function prekazka2(){
    setTimeout(function(){
    block2.style.animation = "block2 2s infinite";
    block2.style.animationTimingFunction = "linear";}, 666)
}
function prekazka3(){
    setTimeout(function(){
    block3.style.animation = "block3 2s infinite";
    block3.style.animationTimingFunction = "linear";}, 1333)
}
var checkDead  = setInterval(function(){
    charakterTop = parseInt(window.getComputedStyle(character).getPropertyValue("top"));
    blockLeft = parseInt(window.getComputedStyle(block).getPropertyValue("left"));
    blockLeft2 = parseInt(window.getComputedStyle(block2).getPropertyValue("left"));
    blockLeft3 = parseInt(window.getComputedStyle(block3).getPropertyValue("left"));
    if(blockLeft<40 && blockLeft>0 && charakterTop>=260){
        block.style.animation = "none";
        block2.style.animation = "none";
        block3.style.animation = "none";
        zobrazenie1 = false
        alert("you losed");
        start();
    }
    else if(blockLeft2<40 && blockLeft2>0 && charakterTop>=260){
        block.style.animation = "none";
        block2.style.animation = "none";
        block3.style.animation = "none";
        zobrazenie2 = false
        alert("you losed");
        start();
    }
    else if(blockLeft3<40 && blockLeft3>0 && charakterTop>=260){
        block.style.animation = "none";
        block2.style.animation = "none";
        block3.style.animation = "none";
        zobrazenie3 = false
        alert("you losed");
        start();
    }
    else {
        score = score+1
    }
},10);
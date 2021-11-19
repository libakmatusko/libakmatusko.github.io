zobrazenie1 = true
zobrazenie2 = true

character = document.getElementById("character");
block = document.getElementById("block");
block2 = document.getElementById("block2");
function jump(){
    if(character.classList!= "animate"){
        character.classList.add("animate");
    }
    setTimeout(function(){
        character.classList.remove("animate")},500);
}
function start(){
    block.style.animation = "block 2s infinite";
    block.style.animationTimingFunction = "linear";
    block2.style.animation = "block2 2s infinite";
    block2.style.animationTimingFunction = "linear";
}
var checkDead  = setInterval(function(){
    charakterTop = parseInt(window.getComputedStyle(character).getPropertyValue("top"));
    blockLeft = parseInt(window.getComputedStyle(block).getPropertyValue("left"));
    blockLeft2 = parseInt(window.getComputedStyle(block2).getPropertyValue("left"));
    if(blockLeft<20 && blockLeft>0 && charakterTop>=130){
        block.style.animation = "none";
        alert("you losed");
    }
    if(blockLeft2<20 && blockLeft2>0 && charakterTop>=130){
        block2.style.animation = "none";
        alert("you losed");
    }
},10);
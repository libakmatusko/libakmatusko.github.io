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
var checkDead  = setInterval(function(){
    charakterTop = parseInt(window.getComputedStyle(character).getPropertyValue("top"));
    blockLeft = parseInt(window.getComputedStyle(block).getPropertyValue("left"));
    blockLeft2 = parseInt(window.getComputedStyle(block2).getPropertyValue("left"));
    if(blockLeft<20 && blockLeft>0 && charakterTop>=130){
        block.style.animation = "none";
        block.style.display = "none";
        alert("you losed");
    }
    if(blockLeft2<20 && blockLeft2>0 && charakterTop>=130){
        block2.style.animation = "none";
        block2.style.display = "none";
        alert("you losed");
    }
},10);
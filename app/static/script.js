
window.onload = function(){
    display_elem("users");
}

function display_elem(element){
    let contents = document.getElementsByClassName('admin-content-internal');
    // contents.array.forEach((element) => console.log(element));

    for(let i = 0; i < contents.length; i++){
        if (contents[i].id == element){
            contents[i].style.display = "block";
            continue;
        }
        contents[i].style.display = "none";
    }

}
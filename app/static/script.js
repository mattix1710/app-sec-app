var news_paragraph = document.getElementsByClassName("news-paragraph")[0];
var text = news_paragraph.innerHTML;
news_paragraph.innerHTML = "";

var words = text.split(" ");
for(i = 0; i < 50; i++){
    news_paragraph.innerHTML += words[i] + " ";
}

news_paragraph.innerHTML += "...";
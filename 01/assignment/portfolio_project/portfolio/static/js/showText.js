// '더 읽어보기' 팝업창을 위한 js

const toggleLink = document.getElementsByClassName("toggleLink")[0];
const hiddenText = document.getElementsByClassName("hiddenText");

toggleLink.addEventListener("click", function(event) {
    event.preventDefault(); // Prevent the default behavior of the link

    for(let i = 0; i < hiddenText.length; i++) {
        const element = hiddenText[i]
        if (element.style.display === "none") {
            // If it's hidden, show it
            element.style.display = "block";
        } else {
            // If it's visible, hide it
            element.style.display = "none";
        }
    }
});
const fold = (event,element) => {element.classList.toggle('folded');event.stopPropagation();}

window.addEventListener("load", function() {
    document.querySelectorAll('main div').forEach(div => {
        div.addEventListener('click', function(event) {
            this.classList.toggle('folded');
            event.stopPropagation();
        });
    });
    document.querySelectorAll('main button').forEach(div => {
        div.addEventListener('click', function(event) {
            window.location.href=this.dataset.url;
        });
    });
});
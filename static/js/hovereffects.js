
const image = document.getElementById('image');

image.addEventListener('mouseenter', e => {
    hoverer(image);
});

image.addEventListener('mouseleave', e => {
    dehoverer(image);
})

function hoverer(img) {
    img.style.border = "thick solid #00000"
}

function dehoverer(img) {
    img.style.border = "none"
}
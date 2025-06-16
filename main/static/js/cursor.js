// основной курсор
const cursor = document.createElement("div");
cursor.classList.add("custom-cursor");
document.body.appendChild(cursor);

// позиция мышки
let mouseX = 0;
let mouseY = 0;

document.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.style.left = `${mouseX}px`;
    cursor.style.top = `${mouseY}px`;

    createTrail(mouseX, mouseY);  // создаём след
});

// хвост: создаём div с теми же стилями, но прозрачным
function createTrail(x, y) {
    const trail = document.createElement("div");
    trail.classList.add("cursor-trail");
    trail.style.left = `${x}px`;
    trail.style.top = `${y}px`;
    document.body.appendChild(trail);

    // исчезает через 500 мс
    setTimeout(() => {
        trail.remove();
    }, 500);
}

document.query

// создаём canvas и добавляем на страницу
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
canvas.classList.add('hex-grid');
document.body.appendChild(canvas);

let width, height;
let points = [];           // массив всех сот (точек-сот)
let spacing = 60;          // расстояние между центрами сот

// функция для обновления размера экрана
function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
    generateGrid();        // заново пересоздаём соты
}
window.addEventListener('resize', resize);
resize();

// создаём сетку из сот с рандомным движением
function generateGrid() {
    points = [];
    const r = spacing;
    const dx = r * Math.sqrt(3);   // горизонтальный шаг
    const dy = r * 1.5;            // вертикальный шаг

    for (let y = 0; y < height + dy; y += dy) {
        for (let x = 0; x < width + dx; x += dx) {
            let offsetX = (y / dy) % 2 === 0 ? 0 : dx / 2; // сдвиг для зигзагообразной сетки
            points.push({
                x: x + offsetX,                 // координаты соты
                y: y,
                vx: (Math.random() - 0.5) * 0.5, // случайная скорость по X
                vy: (Math.random() - 0.5) * 0.5, // случайная скорость по Y
                pulse: 0,                        // значение пульсации
                activated: false                // флаг активации
            });
        }
    }
}

// отслеживаем позицию мышки
let mouse = { x: -1000, y: -1000 };  // начальное "далеко"
document.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
});

// при клике активируем ближайшие к курсору соты
document.addEventListener('click', () => {
    points.forEach(p => {
        const dist = Math.hypot(mouse.x - p.x, mouse.y - p.y);
        if (dist < 100 && !p.activated) {
            p.pulse = 1.0;         // запускаем пульс
            p.activated = true;    // меняем цвет навсегда
        }
    });
});

// функция отрисовки шестиугольной соты
function drawHex(cx, cy, radius, pulseFactor = 1.0, color = '#7f00ff') {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
        const angle = Math.PI / 3 * i;  // угол для каждой вершины
        const x = cx + radius * pulseFactor * Math.cos(angle);
        const y = cy + radius * pulseFactor * Math.sin(angle);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.closePath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.stroke();
}

// основной цикл отрисовки
function draw() {
    ctx.clearRect(0, 0, width, height);  // чистим холст

    points.forEach((p, i) => {
        // движение
        p.x += p.vx;
        p.y += p.vy;

        // отскок от стен
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // отталкивание между сотами
        for (let j = i + 1; j < points.length; j++) {
            const p2 = points[j];
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const minDist = spacing * 0.8;

            if (dist < minDist && dist > 0) {
                const angle = Math.atan2(dy, dx);
                const force = 0.05;
                const ax = Math.cos(angle) * force;
                const ay = Math.sin(angle) * force;

                p.vx += ax;
                p.vy += ay;
                p2.vx -= ax;
                p2.vy -= ay;
            }
        }

        // анимация пульсации (временное "раздувание")
        if (p.pulse > 0) {
            p.pulse -= 0.02;
            if (p.pulse < 0) p.pulse = 0;
        }

        const pulseSize = 1 + Math.sin(p.pulse * Math.PI * 3) * 0.2;  // эффект "дыхания"
        const color = p.activated ? '#00ffff' : '#7f00ff';  // если активирован — бирюзовый

        drawHex(p.x, p.y, spacing / 2.2, pulseSize, color); // рисуем соту

        // если курсор рядом — рисуем "связь"
        const distToMouse = Math.hypot(mouse.x - p.x, mouse.y - p.y);
        if (distToMouse < 100) {
            ctx.strokeStyle = '#024702';  // цвет нити
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(mouse.x, mouse.y);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
        }
    });

    requestAnimationFrame(draw); // продолжаем анимацию
}

draw();  // запускаем

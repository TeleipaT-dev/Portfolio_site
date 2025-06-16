// создаём канвас
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
canvas.classList.add('noise-bg');
document.body.appendChild(canvas);

// обновление размера при изменении окна
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// создаём шум
function generateNoise() {
    const imageData = ctx.createImageData(canvas.width, canvas.height);
    const buffer32 = new Uint32Array(imageData.data.buffer);
    const len = buffer32.length;

    for (let i = 0; i < len; i++) {
        if (Math.random() < 0.03) {
            buffer32[i] = 0x222222ff; // мягкий тёмный шум
        }

    }

    ctx.putImageData(imageData, 0, 0);
}

// анимация
function loop() {
    generateNoise();
    requestAnimationFrame(loop);
}
loop();

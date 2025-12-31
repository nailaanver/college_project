// Simple scroll animation trigger
window.addEventListener("scroll", () => {
    document.querySelectorAll(".slide-up").forEach(el => {
        let position = el.getBoundingClientRect().top;
        let screenHeight = window.innerHeight;

        if (position < screenHeight - 100) {
            el.style.opacity = 1;
        }
    });
});

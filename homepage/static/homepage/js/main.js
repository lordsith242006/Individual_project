// Строки таблиц с атрибутом data-href работают как ссылки.
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-href]").forEach((row) => {
        row.style.cursor = "pointer";
        row.addEventListener("click", () => {
            window.location = row.dataset.href;
        });
    });
});

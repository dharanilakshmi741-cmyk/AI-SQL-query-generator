function copySQL() {
    const query = document.getElementById("sqlQuery");

    if (!query) {
        return;
    }

    navigator.clipboard.writeText(query.innerText);
}

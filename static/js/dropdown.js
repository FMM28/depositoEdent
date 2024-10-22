function toggleDropdown() {
    document.getElementById("perfilDropdown").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.perfil-btn')) {
        var dropdowns = document.getElementsByClassName("perfil-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
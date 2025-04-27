/** Alterna submenus
 * Usado para alternar a exibição de submenus no menu lateral
 * @param {HTMLElement} link - O elemento de link que foi clicado
 * @param {Event} e - O evento de clique
 * @description Este código adiciona um evento de clique a todos os links que têm submenus. 
 * Quando um link é clicado, ele alterna a classe "open" no elemento pai, mostrando ou ocultando o submenu associado.
*/
document.querySelectorAll(".has-submenu > a").forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        const parent = link.parentElement;
        const icon = link.querySelector("i:last-of-type");
        icon.className = icon.className === "bi bi-chevron-down" ? "bi bi-chevron-left" : "bi bi-chevron-down";
        
        parent.classList.toggle("open");
    });
});

/** Inicializa o Feather Icons
 * Usado para substituir os ícones do Feather no DOM
 * @description O Feather Icons é uma biblioteca de ícones SVG.
 * */ 
feather.replace();

/** Alterna o menu lateral
 * Usado para alternar a visibilidade do menu lateral
 * @description Este código adiciona um evento de clique ao botão de alternância do menu lateral.
 * Quando o botão é clicado, ele alterna a classe "closed" no menu lateral e a classe "sidebar-closed" no layout.
 * Isso permite que o menu lateral seja ocultado ou exibido.
 * */
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const layout = document.getElementById('layout');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('closed');
    layout.classList.toggle('sidebar-closed');
});

/** Alterna o tema
 * Usado para alternar entre o tema claro e escuro
 * @description Este código adiciona um evento de clique ao botão de alternância do tema.
 * Quando o botão é clicado, ele alterna a classe "dark-theme" no corpo do documento,
 * mudando assim o tema da página entre claro e escuro.
 * */
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    const isDarkMode = body.classList.toggle('dark-theme');
    const icon = themeToggle.querySelector('i');
    icon.className = isDarkMode ? 'bi bi-moon-stars' : 'bi bi-brightness-high';
});


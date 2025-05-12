// Centralizar a lógica de aplicação do tema
function applyTheme(theme) {
    const validThemes = ['light', 'dark'];
    if (!validThemes.includes(theme)) {
        console.warn(`Tema inválido: ${theme}. Aplicando tema padrão 'light'.`);
        theme = 'light';
    }

    document.body.classList.toggle('dark-theme', theme === 'dark');
    localStorage.setItem('theme', theme);
}

// Aplicar o tema salvo no localStorage imediatamente ao carregar a página
(function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);
})();

// Adicionar suporte para eventos dinâmicos
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);
});

// Fallback para navegadores sem localStorage
if (typeof localStorage === 'undefined') {
    console.warn('localStorage não está disponível. O tema não será persistido.');
}
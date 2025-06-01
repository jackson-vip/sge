// Centralizar a lógica de aplicação do tema
function applyTheme(theme) {
    const validThemes = ['light', 'dark', 'auto'];
    if (!validThemes.includes(theme)) {
        console.warn(`Tema inválido: ${theme}. Aplicando tema padrão 'light'.`);
        theme = 'light';
    }

    if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = prefersDark ? 'dark' : 'light';
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
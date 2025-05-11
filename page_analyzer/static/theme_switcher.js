const toggleButton = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const body = document.body;

// Загрузка сохраненной темы из localStorage
const savedTheme = localStorage.getItem('theme') || 'light';
body.setAttribute('data-bs-theme', savedTheme);
if (savedTheme === 'dark') {
    toggleButton.textContent = 'Светлая тема';
} else {
    toggleButton.textContent = 'Темная тема';
}

// Переключение темы
toggleButton.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    body.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    if (newTheme === 'dark') {
        toggleButton.textContent = 'Светлая тема';
    } else {
        toggleButton.textContent = 'Темная тема';
    }
});
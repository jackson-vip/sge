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
 * Persiste a preferência do tema no localStorage.
 * */
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Aplica o tema salvo no localStorage ao carregar a página
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    body.classList.add(savedTheme);
    const icon = themeToggle.querySelector('i');
    if (savedTheme === 'dark-theme') {
        icon.classList.remove('bi-brightness-high');
        icon.classList.add('bi-moon-stars');
    } else {
        icon.classList.remove('bi-moon-stars');
        icon.classList.add('bi-brightness-high');
    }
}

// Atualiza o localStorage ao alternar o tema
themeToggle.addEventListener('click', () => {
    const isDarkMode = body.classList.toggle('dark-theme');
    localStorage.setItem('theme', isDarkMode ? 'dark-theme' : '');
    const icon = themeToggle.querySelector('i');
    icon.className = isDarkMode ? 'bi bi-moon-stars' : 'bi bi-brightness-high';
});

/** Alterna o dropdown do usuário
 * Usado para abrir e fechar o menu dropdown ao clicar na imagem do usuário
 */
const userDropdown = document.getElementById('userDropdown');
const avatar = userDropdown.querySelector('img');

avatar.addEventListener('click', () => {
    userDropdown.classList.toggle('open');
});

// Fecha o dropdown ao clicar fora dele
document.addEventListener('click', (event) => {
    if (!userDropdown.contains(event.target)) {
        userDropdown.classList.remove('open');
    }
});

// Fecha o dropdown ao pressionar a tecla ESC
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        userDropdown.classList.remove('open');
    }
});

/** Bootstrap tooltips initialization
 * Usado para inicializar tooltips do Bootstrap
 * @description Este código seleciona todos os elementos com o atributo `data-bs-toggle="tooltip"` e inicializa os tooltips do Bootstrap neles.
 * Isso permite que os tooltips sejam exibidos quando o usuário passa o mouse sobre esses elementos.
 */
const tooltipTriggerList = document.querySelectorAll('[data-bs-tooltip="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// Capturar o valor do select opcao e redirecionar para a página correta
// Defina baseUrl antes de usar
const baseUrl = window.location.origin + window.location.pathname;

$(document).ready(function () {
    $('#opcoes').on("change", function () {
        let opcao = $('#opcoes').val();

        if (opcao == '12') {
            window.location.href = `${baseUrl}?opcao=${opcao}`;
        } else if (opcao == '15') {
            window.location.href = `${baseUrl}?opcao=${opcao}`;
        } else if (opcao == '18') {
            window.location.href = `${baseUrl}?opcao=${opcao}`;
        } else if (opcao == '21') {
            window.location.href = `${baseUrl}?opcao=${opcao}`;
        }
    });
});

/** Remoção dos alerts após 5 segundos
 * Usado para remover os alerts após 5 segundos
 * @description Este código seleciona todos os elementos com a classe `alert` e define um temporizador para removê-los do DOM após 5 segundos.
 * Isso é útil para limpar automaticamente os alerts da página após um período de tempo, melhorando a experiência do usuário.
 */
$(document).ready(function () {
    setTimeout(function () {
        $('div.alert').fadeOut('slow', function () {
            $(this).remove();
        });
    }, 5000);
});

/** Inicialização do Datepicker
 * Usado para inicializar o datepicker nos campos de data
 * @description Este código seleciona todos os elementos com a classe `datepicker` e inicializa o datepicker neles.
 * Isso permite que os usuários selecionem uma data de forma mais fácil e intuitiva.
 */
// Configuração do Datepicker para pt-BR
$.fn.datepicker.dates['pt-BR'] = {
    days: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
    daysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
    daysMin: ['Do', 'Se', 'Te', 'Qa', 'Qi', 'Se', 'Sa'],
    months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    today: "Hoje",
    clear: "Limpar",
    format: "dd/mm/yyyy",
    titleFormat: "MM yyyy",
    weekStart: 0                // Inicia a semana no domingo
};

$(function () {
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'pt-BR',
        autoclose: true,
        todayHighlight: true,   // Destaca a data de hoje
        clearBtn: true,
        startDate: '-100y',
        container: 'body'
    });
});

// Função para buscar o Endereço pelo CEP (ViaCEP)
$(document).ready(function () {

    function limparEndereco() {
        $('#id_endereco_logradouro').val('');
        $('#id_endereco_complemento').val('');
        $('#id_endereco_bairro').val('');
        $('#id_endereco_municipio').val('');
        $('#id_endereco_sigla').val('');
    }

    // Função para buscar o CEP
    function buscarCEP(cep) {
        $("#id_endereco_cep").on("blur", function () {
            // Remove tudo que não é número
            let cep = $(this).val().replace(/[^\d]+/g, '');

            // Verifica se o CEP possui 8 caracteres
            if (cep.length !== 8) {
                console.log('CEP inválido!');
                return false;
            }
            // Se CEP for diferente de vazio
            if (cep !== '') {

                // Faz a requisição
                $.ajax({
                    url: `https://viacep.com.br/ws/${cep}/json/`,
                    type: 'GET',
                    dataType: 'json',
                    success: function (data) {
                        // Se não houver erro
                        if (!('erro' in data)) {
                            // Preenche os campos com '...' (aguardando a requisição)
                            $('#id_endereco_logradouro').val('...');
                            $('#id_endereco_complemento').val('...');
                            $('#id_endereco_bairro').val('...');
                            // $('#id_endereco_municipio').val('...');
                            // $('#id_endereco_sigla').val('...');

                            setTimeout(() => {
                                // Carrega os campos
                                $('#id_endereco_logradouro').val(data.logradouro);
                                $('#id_endereco_complemento').val(data.complemento);
                                $('#id_endereco_bairro').val(data.bairro);
                                // $('#id_endereco_municipio').val(data.localidade);
                                // $('#id_endereco_sigla').val(data.uf);
                            }, 500);

                        } else {
                            limparEndereco();
                            // console.log('CEP não encontrado!');
                        }
                    },
                    error: function () {
                        limparEndereco();
                        // console.log('CEP não encontrado!');
                    }
                });
            }
            limparEndereco();
        });
    };
    // Chama a função buscarCEP passando o campo de CEP
    buscarCEP($('#id_endereco_cep'));
});

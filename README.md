# 📦 Sistema de Gestão Empresarial (SGE)

O **SGE** é um sistema web completo para gestão de empresas, com foco em controle de estoque, cadastro de clientes, funcionários, fornecedores, movimentações e relatórios. O sistema é responsivo, moderno e utiliza boas práticas de desenvolvimento Django.

## 🚀 Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Django 5.x](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- HTML5, CSS3 (Bootstrap 5) e JavaScript (jQuery)

## ⚙️ Funcionalidades

- Cadastro e edição de funcionários, clientes, fornecedores e produtos
- Geração automática e única de matrícula para funcionários
- Edição integrada de dados do usuário e endereço do funcionário
- Filtros avançados e busca dinâmica nas listagens
- Máscara de CPF com toggle de visualização
- Controle de estoque: entrada, saída, movimentações e alertas
- Relatórios de movimentações (em desenvolvimento)
- Interface responsiva e moderna com Bootstrap 5
- Templates e componentes reutilizáveis (search, filtros, breadcrumbs, etc)
- Autenticação de usuários e permissões
- Geração de senha aleatória e segura para novos usuários
- Customização de datas com datepicker e máscaras

## 📁 Estrutura recomendada do projeto

```bash
sge/                      # Raiz do projeto
│
├── sge_core/             # Configurações globais do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── authentication/       # Autenticação e perfis de usuário
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/authentication/
│
├── dashboard/            # Painel e gráficos
│   └── templates/dashboard/
│
├── clientes/             # Cadastro e gestão de clientes
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── templates/cliente/
│   └── static/cliente/
│
├── funcionarios/         # Cadastro e gestão de funcionários
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── templates/funcionario/
│   └── static/funcionario/
│
├── fornecedores/         # Cadastro e gestão de fornecedores
│   ├── models.py
│   ├── views.py
│   ├── templates/fornecedor/
│   └── static/fornecedor/
│
├── produtos/             # Cadastro e gestão de produtos
│   ├── models.py
│   ├── views.py
│   ├── templates/produto/
│   └── static/produto/
│
├── estoque/              # Controle de estoque
│   ├── models.py
│   ├── views.py
│   ├── templates/estoque/
│   └── static/estoque/
│
├── movimentacoes/        # Entradas e saídas de estoque
│   ├── models.py
│   ├── views.py
│   ├── templates/movimentacao/
│   └── static/movimentacao/
│
├── utils/                # Funções utilitárias e validações
│   ├── filters.py
│   ├── django_forms.py
│   └── validates_inputs.py
│
├── basic_templates/      # Templates base e parciais globais
│   └── global/
├── basic_static/         # CSS, JS e imagens globais
│   └── global/
├── media/                # Uploads de arquivos
├── Dockerfile
├── requirements.txt
├── docker-compose.yml
├── .env / .env-exemplo
└── README.md
```

[git clone git@github.com:jackson-vip/sge.git](https://github.com/jackson-vip/sge)

## 🐳 Como Executar com Docker

```bash
# 1. Clone o repositório
git clone git@github.com:jackson-vip/sge.git
cd sge

# 2. Copie o .env de exemplo
cp .env.example .env

# 3. Suba os containers
docker-compose up --build
```

O sistema estará disponível em [http://localhost:8000](http://localhost:8000)

## 👨‍💻 Execução Local (sem Docker)

1. Crie e ative um ambiente virtual Python 3.11+
2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados PostgreSQL e o arquivo `.env`
4. Execute as migrações:

   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário:

   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor:

   ```bash
   python manage.py runserver
   ```

## 📌 Observações

- O projeto utiliza Bootstrap 5 e componentes customizados para uma interface moderna.
- Os templates e filtros são altamente reutilizáveis.
- O sistema de matrícula de funcionários é automático e único.
- O CPF é mascarado e pode ser exibido/desmascarado via JS.
- O projeto já está pronto para deploy em produção via Docker.
- Para customização de temas, edite os arquivos em `basic_static/global/css/`.

---
Desenvolvido por Jackson. Para dúvidas ou sugestões, abra uma issue no repositório.

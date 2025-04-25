# 📦 Sistema de Gestão de Estoque (SGE)

O **SGE** é um sistema web desenvolvido para atender as necessidades de pequenas e médias empresas no controle e gerenciamento de seus estoques. Ele permite o cadastro, movimentação e monitoramento de produtos, fornecedores, clientes e relatórios.

## 🚀 Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Django 5.x](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [HTML5, CSS3 e JavaScript]

## ⚙️ Funcionalidades

- Cadastro de produtos com:
  - Nome, código, descrição, unidade, categoria e marca
  - Quantidade mínima e atual
  - Controle de validade e lote (opcional)
- Controle de entrada e saída de produtos
- Relatórios de movimentações por período
- Alerta de estoque baixo
- Cadastro de fornecedores e clientes
- Controle de usuários com níveis de permissão
- Interface web responsiva
- Histórico de alterações (log de ações)
- Sistema de login seguro

## 📁 Estrutura recomendada do projeto

```bash
sge/                               # Raiz do projeto
│
├── sge_core/                      # Configurações do projeto Django
│   ├── settings/                  # Configurações do Django
│   ├── urls.py                    # URLs do projeto
│   ├── wsgi.py                    # Ponto de entrada para o servidor WSGI
│   └── asgi.py                    # Ponto de entrada para o servidor ASGI
│
├── authentication/                # App: login, autenticação de usuários, perfis de usuários
│   ├── urls.py                    # URLs do app autenticacao
│   ├── views.py                   # Views do app autenticacao
│   ├── models.py                  # Aqui poderá ficar os perfis de usuários
│   ├── forms.py                   # Formulários de login e registro
│   ├── templates/authentication/  # criando name space para autenticacao
│   └── static/authentication/     # criando name space para autenticacao
│
├── dashboard/                     # App: informações e gráficos
│   ├── templates/dashboard/       # Criando name space para dashboard
│   └── static/dashboard/          # Criando name space para dashboard
│
├── produtos/                      # App: produtos (cadastro, estoque, etc.)
│   ├── templates/produtos/        # Criando name space para templates
│   └── static/produtos/           # Criando name space para arquivos estáticos
│
├── estoque/                       # App: gerenciamento de produtos e estoque
│   ├── templates/estoque/         # Criando name space para templates
│   └── static/estoque/            # Criando name space para arquivos estáticos
│
├── movimentacoes/                 # App: movimentações (entrada e saída)
│   ├── templates/movimentacoes/   # Criando name space para movimentações
│   └── static/movimentacoes/      # Criando name space para movimentações
│
├── fornecedores/                  # App: controle de fornecedores
│   ├── templates/fornecedores/    # Criando name space para fornecedores
│   └── static/fonecedores/        # Criando name space para fornecedores
│
├── relatorios/                    # App: geração de relatórios (futuro)
│   ├── templates/relatorios/      # Criando name space para relatorios
│   └── static/relatorios/         # Criando name space para relatorios
│
├── logs/                         # App: registro de logs e auditorias
│   ├── templates/logs/           # Criando name space para templates
│   └── static/logs/              # Criando name space para arquivos estáticos
│
├── basic_templates/               # Template base para os apps
├── basic_static/                  # Arquivos estáticos (CSS, JS, imagens)
├── utils/                         # Funções utilitárias (ex: validações)
│
│ Dockerfile                       # Imagem do Docker
│ requirements.txt                 # Dependências do projeto
│ docker-compose.yml               # Orquestração dos containers
│ .gitignore                       # Ignorar arquivos do Git
│ .env                             # Variáveis de ambiente
└── README.md
```

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

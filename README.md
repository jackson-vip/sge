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
sge/                        # Raiz do projeto
│
├── backend/                # Código do backend Django
│   ├── sge_core/           # Configurações do projeto Django
│   ├── produtos/           # App: produtos (cadastro, estoque, etc.)
│   ├── usuarios/           # App: usuários e permissões
│   ├── vendas/             # App: controle de vendas (futuro)
│   ├── compras/            # App: controle de compras (futuro)
│   ├── relatorios/         # App: geração de relatórios (futuro)
│   ├── static/             # Arquivos estáticos
│   └── media/              # Uploads
│
├── docker/                 # Configurações de Docker
│   ├── web/                # Dockerfile e configs do Django
│   └── db/                 # Volume do PostgreSQL
│
├── docker-compose.yml      # Orquestração dos containers
├── .env                    # Variáveis de ambiente
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

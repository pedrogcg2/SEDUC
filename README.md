# SEDUC API

Uma API Flask para gerenciamento de dados educacionais usando SQLAlchemy com padrão Repository.

> **⚠️ Nota:** Esta API é de **somente leitura e criação**. Operações de atualização (PUT) e exclusão (DELETE) foram removidas por design.

## Estrutura do Projeto

```
SEDUC/
├── api/
│   ├── __init__.py
│   ├── app.py              # Configuração principal da aplicação Flask
│   ├── config.py           # Configurações
│   ├── run.py              # Ponto de entrada da aplicação
│   ├── models/             # Camada de Modelos
│   │   ├── __init__.py
│   │   ├── aluno.py        # Modelo Aluno
│   │   ├── escola.py       # Modelo Escola
│   │   ├── disciplina.py   # Modelo Disciplina
│   │   └── matricula.py    # Modelo Matricula
│   ├── repositories/       # Camada de Repositórios
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── aluno_repository.py
│   │   ├── escola_repository.py
│   │   ├── disciplina_repository.py
│   │   └── matricula_repository.py
│   ├── services/           # Camada de Serviços
│   │   ├── __init__.py
│   │   ├── aluno_service.py
│   │   ├── escola_service.py
│   │   ├── disciplina_service.py
│   │   └── matricula_service.py
│   └── routes/             # Camada de Rotas
│       ├── __init__.py
│       ├── aluno_routes.py
│       ├── escola_routes.py
│       ├── disciplina_routes.py
│       └── matricula_routes.py
├── data/
│   ├── dados_simulados_educacao.csv
│   └── seed.py
├── sql-scripts/
│   ├── create_seduc_database.sql
│   └── create_users.sql
├── requirements.txt
├── run.py                  # Ponto de entrada principal
├── start_api.sh           # Script de inicialização
└── README.md
```

## Configuração

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

Certifique-se de que o PostgreSQL está rodando e execute os scripts SQL:

```bash
# Conectar ao PostgreSQL
psql -U postgres

# Executar os scripts
\i sql-scripts/create_seduc_database.sql
\i sql-scripts/create_users.sql
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=postgresql://master:HgAXVS5uWph3@localhost/sqldb-seduc
SECRET_KEY=sua-chave-secreta-aqui
FLASK_ENV=development
```

### 4. Executar Migrações (Opcional)

```bash
cd api
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Executar a Aplicação

```bash
python api/run.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints da API

### Health Check
- `GET /health` - Verificar status da API

### Alunos
- `GET /api/alunos/` - Listar todos os alunos
- `GET /api/alunos/?escola_id=1` - Filtrar por escola
- `GET /api/alunos/?serie=5` - Filtrar por série
- `GET /api/alunos/?turno=manhã` - Filtrar por turno
- `GET /api/alunos/?nome=João` - Buscar por nome
- `GET /api/alunos/{matricula}` - Obter aluno específico
- `POST /api/alunos/` - Criar novo aluno

### Escolas
- `GET /api/escolas/` - Listar todas as escolas
- `GET /api/escolas/?cidade=São Paulo` - Filtrar por cidade
- `GET /api/escolas/?nome=Escola` - Buscar por nome
- `GET /api/escolas/{id_escola}` - Obter escola específica
- `POST /api/escolas/` - Criar nova escola

### Disciplinas
- `GET /api/disciplinas/` - Listar todas as disciplinas
- `GET /api/disciplinas/?nome=Matemática` - Buscar por nome
- `GET /api/disciplinas/{id_disciplina}` - Obter disciplina específica
- `POST /api/disciplinas/` - Criar nova disciplina

### Matrículas
- `GET /api/matriculas/` - Listar todas as matrículas
- `GET /api/matriculas/?aluno_id=123` - Filtrar por aluno
- `GET /api/matriculas/?escola_id=1` - Filtrar por escola
- `GET /api/matriculas/?disciplina_id=1` - Filtrar por disciplina
- `GET /api/matriculas/?ano=2023` - Filtrar por ano
- `GET /api/matriculas/?serie=5` - Filtrar por série
- `GET /api/matriculas/?status=true` - Filtrar por status
- `GET /api/matriculas/{id}` - Obter matrícula específica
- `POST /api/matriculas/` - Criar nova matrícula
- `GET /api/matriculas/performance/{matricula_aluno}` - Performance do aluno

## Exemplos de Uso

### Criar um Aluno
```bash
curl -X POST http://localhost:5000/api/alunos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "data_mat": "2023-01-15",
    "turno": "manhã",
    "serie": 5,
    "id_escola": 1
  }'
```

### Criar uma Escola
```bash
curl -X POST http://localhost:5000/api/escolas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Escola Municipal São João",
    "endereco": "Rua das Flores, 123",
    "cidade": "São Paulo"
  }'
```

### Criar uma Disciplina
```bash
curl -X POST http://localhost:5000/api/disciplinas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Matemática"
  }'
```

### Criar uma Matrícula
```bash
curl -X POST http://localhost:5000/api/matriculas/ \
  -H "Content-Type: application/json" \
  -d '{
    "ano": 2023,
    "matricula_aluno": 123,
    "id_escola": 1,
    "id_disciplina": 1,
    "serie": 5,
    "nota": 8.5,
    "status": true
  }'
```

## Arquitetura

### Estrutura Modular
A API foi organizada em camadas bem definidas, com cada classe em seu próprio arquivo:

#### Camada de Modelos (`api/models/`)
- **`aluno.py`**: Modelo Aluno com relacionamentos
- **`escola.py`**: Modelo Escola com relacionamentos
- **`disciplina.py`**: Modelo Disciplina com relacionamentos
- **`matricula.py`**: Modelo Matricula com relacionamentos

#### Camada de Repositórios (`api/repositories/`)
- **`base_repository.py`**: Classe base com operações CRUD genéricas
- **`aluno_repository.py`**: Operações específicas para alunos
- **`escola_repository.py`**: Operações específicas para escolas
- **`disciplina_repository.py`**: Operações específicas para disciplinas
- **`matricula_repository.py`**: Operações específicas para matrículas

#### Camada de Serviços (`api/services/`)
- **`aluno_service.py`**: Validações e regras de negócio para alunos
- **`escola_service.py`**: Validações e regras de negócio para escolas
- **`disciplina_service.py`**: Validações e regras de negócio para disciplinas
- **`matricula_service.py`**: Validações e regras de negócio para matrículas

#### Camada de Rotas (`api/routes/`)
- **`aluno_routes.py`**: Endpoints para gerenciamento de alunos
- **`escola_routes.py`**: Endpoints para gerenciamento de escolas
- **`disciplina_routes.py`**: Endpoints para gerenciamento de disciplinas
- **`matricula_routes.py`**: Endpoints para gerenciamento de matrículas

### Repository Pattern
A API utiliza o padrão Repository para abstrair a camada de acesso a dados, com cada entidade tendo seu próprio repositório especializado.

### Service Layer
A camada de serviços implementa a lógica de negócio e validações, mantendo as rotas limpas e focadas apenas na apresentação.

### Modelos
Os modelos SQLAlchemy representam as tabelas do banco de dados com relacionamentos bem definidos.

## Validações

- Campos obrigatórios são validados na camada de serviço
- Notas devem estar entre 0 e 10
- Datas são convertidas automaticamente do formato ISO
- Relacionamentos são mantidos através de chaves estrangeiras

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- `200` - Sucesso
- `201` - Criado com sucesso
- `404` - Recurso não encontrado
- `500` - Erro interno do servidor

Respostas de erro incluem uma mensagem descritiva:

```json
{
  "error": "Aluno não encontrado"
}
``` 
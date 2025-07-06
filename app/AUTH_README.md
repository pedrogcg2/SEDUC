# SEDUC Authentication System

Este documento descreve o sistema de autenticação implementado no SEDUC API.

## Funcionalidades

### 1. Registro de Usuários
- **Endpoint**: `POST /api/auth/register`
- **Campos obrigatórios**: `username`, `password`
- **Campos opcionais**: `email`
- **Validações**:
  - Username deve ser único
  - Senha deve ter pelo menos 6 caracteres
  - Email deve ser único (se fornecido)

### 2. Login de Usuários
- **Endpoint**: `POST /api/auth/login`
- **Campos obrigatórios**: `username`, `password`
- **Retorna**: JWT token e informações do usuário

### 3. Verificação de Token
- **Endpoint**: `POST /api/auth/verify-token`
- **Campos obrigatórios**: `token`
- **Retorna**: Informações do usuário se o token for válido

### 4. Perfil do Usuário
- **Endpoint**: `GET /api/auth/profile`
- **Autenticação**: Requer token JWT
- **Retorna**: Informações do usuário logado

### 5. Alteração de Senha
- **Endpoint**: `POST /api/auth/change-password`
- **Autenticação**: Requer token JWT
- **Campos obrigatórios**: `current_password`, `new_password`

## Frontend

### Páginas Disponíveis

1. **Login** (`/login` ou `/`)
   - Formulário de login com username e senha
   - Link para página de registro
   - Redirecionamento automático após login

2. **Registro** (`/register`)
   - Formulário de registro com validações
   - Confirmação de senha
   - Redirecionamento para login após registro

3. **Dashboard** (`/dashboard`)
   - Página principal após login
   - Exibe informações do usuário
   - Menu de navegação para outras seções
   - Botão de logout

## Configuração

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL=postgresql://master:HgAXVS5uWph3@localhost/sqldb-seduc
SECRET_KEY=sua_chave_secreta_aqui
```

### 3. Inicializar Banco de Dados
```bash
cd api
python init_db.py
```

### 4. Executar a API
```bash
python run.py
```

## Uso da API

### Exemplo de Registro
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_teste",
    "password": "senha123",
    "email": "usuario@teste.com"
  }'
```

### Exemplo de Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_teste",
    "password": "senha123"
  }'
```

### Exemplo de Acesso a Endpoint Protegido
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer SEU_JWT_TOKEN_AQUI"
```

## Segurança

### JWT Tokens
- Tokens expiram em 24 horas
- Usam algoritmo HS256
- Contêm informações do usuário (ID, username)

### Senhas
- Senhas são hasheadas usando Werkzeug
- Hash utiliza PBKDF2 com SHA256
- Salt único para cada senha

### Validações
- Username único
- Email único (se fornecido)
- Senha mínima de 6 caracteres
- Verificação de conta ativa

## Usuário Padrão

Após a inicialização do banco, um usuário admin é criado automaticamente:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@seduc.com`

**⚠️ IMPORTANTE**: Em produção, altere a senha do admin imediatamente!

## Estrutura do Banco

### Tabela `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

## Decorator de Autenticação

Para proteger endpoints, use o decorator `@token_required`:

```python
from routes.auth_routes import token_required

@app.route('/protected-endpoint')
@token_required
def protected_endpoint(current_user):
    return jsonify({'message': f'Hello {current_user.username}!'})
```

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados:
- `200`: Sucesso
- `201`: Criado com sucesso
- `400`: Dados inválidos
- `401`: Não autorizado
- `500`: Erro interno do servidor

Mensagens de erro são retornadas em formato JSON:
```json
{
    "message": "Descrição do erro"
}
``` 
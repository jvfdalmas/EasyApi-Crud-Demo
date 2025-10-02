# PostgreSQL Setup Guide

## 🚨 Problema: Permission Denied for Schema Public

Este erro ocorre em versões recentes do PostgreSQL (15+) onde as permissões padrão foram alteradas por segurança.

### Erro Típico:
```
asyncpg.exceptions.InsufficientPrivilegeError: permission denied for schema public
```

## 🔧 Soluções

### **Opção 1: Script Automático (Recomendado)**

Execute o script de setup incluído:

```bash
# No servidor, navegue até o diretório backend
cd /path/to/your/backend

# Execute o script de setup
./setup_database.sh
```

O script irá:
- Criar o banco de dados `easyapi_crud`
- Criar o usuário `easyapi_user`
- Configurar um schema dedicado `easyapi`
- Definir todas as permissões necessárias

### **Opção 2: Setup Manual**

#### 1. Conectar como superusuário PostgreSQL:
```bash
sudo -u postgres psql
```

#### 2. Criar banco e usuário:
```sql
-- Criar usuário
CREATE USER easyapi_user WITH PASSWORD 'your_secure_password';

-- Criar banco
CREATE DATABASE easyapi_crud OWNER easyapi_user;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE easyapi_crud TO easyapi_user;
```

#### 3. Configurar schema e permissões:
```bash
# Conectar ao banco específico
sudo -u postgres psql easyapi_crud
```

```sql
-- Criar schema dedicado
CREATE SCHEMA IF NOT EXISTS easyapi;

-- Conceder privilégios no schema
GRANT ALL PRIVILEGES ON SCHEMA easyapi TO easyapi_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA easyapi TO easyapi_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA easyapi TO easyapi_user;

-- Privilégios padrão para objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA easyapi GRANT ALL ON TABLES TO easyapi_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA easyapi GRANT ALL ON SEQUENCES TO easyapi_user;

-- Definir search_path
ALTER USER easyapi_user SET search_path TO easyapi, public;

-- Permissões no schema public (fallback)
GRANT CREATE ON SCHEMA public TO easyapi_user;
GRANT USAGE ON SCHEMA public TO easyapi_user;
```

### **Opção 3: Usar Schema Public (Menos Seguro)**

Se você precisar usar o schema public:

```sql
-- Como superusuário postgres
GRANT CREATE ON SCHEMA public TO easyapi_user;
GRANT USAGE ON SCHEMA public TO easyapi_user;
GRANT ALL PRIVILEGES ON DATABASE easyapi_crud TO easyapi_user;
```

## ⚙️ Configuração da Aplicação

### 1. Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite com suas configurações
nano .env
```

Exemplo de `.env`:
```env
DATABASE_URL=postgresql+asyncpg://easyapi_user:your_secure_password@localhost/easyapi_crud
APP_ENV=production
ALLOWED_ORIGINS=http://your-domain.com,https://your-domain.com
```

### 2. Executar Migrações

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Criar migração inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrações
alembic upgrade head
```

## 🔍 Verificação

### Testar Conexão:
```bash
# Teste de conexão simples
python3 -c "
import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect('postgresql://easyapi_user:your_secure_password@localhost/easyapi_crud')
    result = await conn.fetchval('SELECT version()')
    print(f'PostgreSQL version: {result}')
    await conn.close()

asyncio.run(test())
"
```

### Verificar Permissões:
```sql
-- Conectar como easyapi_user
psql postgresql://easyapi_user:your_secure_password@localhost/easyapi_crud

-- Testar criação de tabela
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));
DROP TABLE test_table;
```

## 🚨 Troubleshooting

### Erro: "role does not exist"
```bash
# Verificar se o usuário existe
sudo -u postgres psql -c "\du"
```

### Erro: "database does not exist"
```bash
# Listar bancos
sudo -u postgres psql -c "\l"
```

### Erro: "connection refused"
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Iniciar se necessário
sudo systemctl start postgresql
```

### Erro: "authentication failed"
```bash
# Verificar configuração de autenticação
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Procure por linhas como:
# local   all             all                                     peer
# host    all             all             127.0.0.1/32            md5
```

## 📝 Notas de Segurança

1. **Senhas Fortes**: Use senhas complexas em produção
2. **Conexões SSL**: Configure SSL para conexões remotas
3. **Firewall**: Limite acesso ao PostgreSQL apenas aos IPs necessários
4. **Backup**: Configure backups regulares do banco
5. **Monitoramento**: Implemente logs e monitoramento de acesso

## 🔄 Migração de SQLite para PostgreSQL

Se você estava usando SQLite antes:

1. Exporte dados do SQLite (se houver)
2. Configure PostgreSQL conforme este guia
3. Execute as migrações do Alembic
4. Importe dados (se necessário)

```bash
# Backup SQLite (se existir)
cp app.db app.db.backup

# Limpar migrações antigas (se necessário)
rm -rf alembic/versions/*

# Criar nova migração
alembic revision --autogenerate -m "Initial PostgreSQL migration"
alembic upgrade head
```

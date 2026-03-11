-- ==========================================================
-- SGE | Fornecedores | Ajustes de integridade de dados
-- Execucao manual (database-first)
--
-- MOTIVO DA SEPARACAO EM TRANSACOES:
-- A tabela possui FKs com DEFERRABLE INITIALLY DEFERRED.
-- O PostgreSQL nao permite misturar DDL (ALTER TABLE) e DML
-- (UPDATE) na mesma transacao quando ha trigger events
-- pendentes dessas constraints adiadas.
-- Por isso cada bloco abaixo e uma transacao isolada.
-- ==========================================================


-- ==========================================================
-- TRANSACAO 1: Correcao de dados (DML puro)
-- ==========================================================
BEGIN;

-- 1a) Normalizar status para minusculo
UPDATE sge_fornecedor
SET status = LOWER(TRIM(status))
WHERE status IS NOT NULL AND status <> LOWER(TRIM(status));

-- 1b) Preencher status nulo/vazio com 'ativo'
UPDATE sge_fornecedor
SET status = 'ativo'
WHERE status IS NULL OR TRIM(status) = '';

-- 1c) Limpar brancos de CPF/CNPJ
UPDATE sge_fornecedor
SET
    cpf  = NULLIF(TRIM(cpf), ''),
    cnpj = NULLIF(TRIM(cnpj), '');

-- 1d) Remover CPF de fornecedor juridico
UPDATE sge_fornecedor
SET cpf = NULL
WHERE tipo_pessoa = 'juridica'
  AND cpf IS NOT NULL;

-- 1e) Remover CNPJ de fornecedor fisico
UPDATE sge_fornecedor
SET cnpj = NULL
WHERE tipo_pessoa = 'fisica'
  AND cnpj IS NOT NULL;

COMMIT;


-- ==========================================================
-- TRANSACAO 2: Ajustes estruturais na coluna status (DDL)
-- ==========================================================
BEGIN;

ALTER TABLE sge_fornecedor
    ADD COLUMN IF NOT EXISTS status VARCHAR(20) NOT NULL DEFAULT 'ativo';

ALTER TABLE sge_fornecedor
    ALTER COLUMN status SET DEFAULT 'ativo';

ALTER TABLE sge_fornecedor
    ALTER COLUMN status SET NOT NULL;

COMMIT;


-- ==========================================================
-- TRANSACAO 3: Adicionar CHECK constraints (DDL)
-- ==========================================================
BEGIN;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_sge_fornecedor_status'
          AND conrelid = 'sge_fornecedor'::regclass
    ) THEN
        ALTER TABLE sge_fornecedor
        ADD CONSTRAINT ck_sge_fornecedor_status
        CHECK (status IN ('ativo', 'inativo', 'bloqueado'));
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'ck_sge_fornecedor_doc_por_tipo'
          AND conrelid = 'sge_fornecedor'::regclass
    ) THEN
        ALTER TABLE sge_fornecedor
        ADD CONSTRAINT ck_sge_fornecedor_doc_por_tipo
        CHECK (
            (tipo_pessoa = 'juridica' AND cnpj IS NOT NULL AND cnpj <> '' AND (cpf IS NULL OR cpf = ''))
            OR
            (tipo_pessoa = 'fisica'   AND cpf  IS NOT NULL AND cpf  <> '' AND (cnpj IS NULL OR cnpj = ''))
        );
    END IF;
END $$;

COMMIT;

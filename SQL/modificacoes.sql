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


-- ==========================================================
-- TRANSACAO 4: Normalizar CPF, CNPJ, CEP e RG (remover máscaras)
-- ==========================================================
-- Aplicada a partir de MARCO/2026
-- Objetivo: Remover padrões de máscara de documentos e CEP
-- mantendo apenas dígitos, conforme novo padrão de backend.
-- ==========================================================
BEGIN;

-- 4a) Normalizar CPF em sge_fornecedor (apenas dígitos)
UPDATE sge_fornecedor
SET cpf = regexp_replace(cpf, '[^0-9]', '', 'g')
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf != regexp_replace(cpf, '[^0-9]', '', 'g');

-- 4b) Normalizar CNPJ em sge_fornecedor (apenas dígitos)
UPDATE sge_fornecedor
SET cnpj = regexp_replace(cnpj, '[^0-9]', '', 'g')
WHERE cnpj IS NOT NULL AND cnpj <> '' AND cnpj != regexp_replace(cnpj, '[^0-9]', '', 'g');

-- 4c) Normalizar CPF em sge_cliente (apenas dígitos)
UPDATE sge_cliente
SET cpf = regexp_replace(cpf, '[^0-9]', '', 'g')
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf != regexp_replace(cpf, '[^0-9]', '', 'g');

-- 4d) Normalizar RG em sge_cliente (apenas dígitos)
UPDATE sge_cliente
SET rg = regexp_replace(rg, '[^0-9]', '', 'g')
WHERE rg IS NOT NULL AND rg <> '' AND rg != regexp_replace(rg, '[^0-9]', '', 'g');

-- 4e) Normalizar CPF em sge_funcionario (apenas dígitos)
UPDATE sge_funcionario
SET cpf = regexp_replace(cpf, '[^0-9]', '', 'g')
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf != regexp_replace(cpf, '[^0-9]', '', 'g');

-- 4f) Normalizar RG em sge_funcionario (apenas dígitos)
UPDATE sge_funcionario
SET rg = regexp_replace(rg, '[^0-9]', '', 'g')
WHERE rg IS NOT NULL AND rg <> '' AND rg != regexp_replace(rg, '[^0-9]', '', 'g');

-- 4g) Normalizar CEP em sge_endereco (apenas dígitos)
UPDATE sge_endereco
SET cep = regexp_replace(cep, '[^0-9]', '', 'g')
WHERE cep IS NOT NULL AND cep <> '' AND cep != regexp_replace(cep, '[^0-9]', '', 'g');

COMMIT;


-- ==========================================================
-- TRANSACAO 5: Diagnóstico pós-normalização (DML puro)
-- ==========================================================
-- Aplicada após a normalização de março/2026
-- Objetivo: Padronizar os dados e verificar se ainda existem 
-- registros com caracteres não numéricos em campos que 
-- deveriam conter apenas dígitos, garantindo a integridade dos dados.
-- ==========================================================
BEGIN;

-- 5a) Garantir que voce esta no banco/schema corretos
SELECT current_database(), current_schema();

-- 5b) Diagnostico: quantos registros ainda tem caracteres nao numericos
SELECT COUNT(*) AS fornecedor_cpf_com_mascara
FROM sge_fornecedor
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf ~ '[^0-9]';

SELECT COUNT(*) AS fornecedor_cnpj_com_mascara
FROM sge_fornecedor
WHERE cnpj IS NOT NULL AND cnpj <> '' AND cnpj ~ '[^0-9]';

SELECT COUNT(*) AS cliente_cpf_com_mascara
FROM sge_cliente
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf ~ '[^0-9]';

SELECT COUNT(*) AS cliente_rg_com_mascara
FROM sge_cliente
WHERE rg IS NOT NULL AND rg <> '' AND rg ~ '[^0-9]';

SELECT COUNT(*) AS funcionario_cpf_com_mascara
FROM sge_funcionario
WHERE cpf IS NOT NULL AND cpf <> '' AND cpf ~ '[^0-9]';

SELECT COUNT(*) AS funcionario_rg_com_mascara
FROM sge_funcionario
WHERE rg IS NOT NULL AND rg <> '' AND rg ~ '[^0-9]';

SELECT COUNT(*) AS endereco_cep_com_mascara
FROM sge_endereco
WHERE cep IS NOT NULL AND cep <> '' AND cep ~ '[^0-9]';

-- 5c) Amostras finais (devem estar sem mascara)
SELECT cnpj FROM sge_fornecedor WHERE cnpj IS NOT NULL LIMIT 5;

COMMIT;
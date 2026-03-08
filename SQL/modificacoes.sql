
-- Adicionar a coluna STATUS em fornecedores

SELECT * FROM sge_fornecedor;
ALTER TABLE sge_fornecedor
ADD COLUMN STATUS VARCHAR(20) NOT NULL DEFAULT 'ATIVO';

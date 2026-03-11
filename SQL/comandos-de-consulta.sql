SELECT conname, pg_get_constraintdef(oid) AS definition FROM pg_constraint WHERE conrelid = 'sge_fornecedor'::regclass AND contype = 'c' ORDER BY conname;

SELECT id, tipo_pessoa, cnpj, cpf, status FROM sge_fornecedor;
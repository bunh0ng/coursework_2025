CREATE OR REPLACE FUNCTION reuse_invoice_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(invoice_id) + 1 INTO NEW.invoice_id
    FROM invoice p1
    WHERE NOT EXISTS (
        SELECT 1 FROM invoice p2 WHERE p2.invoice_id = p1.invoice_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.invoice_id IS NULL THEN
        NEW.invoice_id := nextval('invoice_invoice_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_invoice_id
BEFORE INSERT ON invoice
FOR EACH ROW
EXECUTE FUNCTION reuse_invoice_id();
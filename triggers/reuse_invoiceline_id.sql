CREATE OR REPLACE FUNCTION reuse_invoiceline_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(invoiceline_id) + 1 INTO NEW.invoiceline_id
    FROM invoiceline p1
    WHERE NOT EXISTS (
        SELECT 1 FROM invoiceline p2 WHERE p2.invoiceline_id = p1.invoiceline_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.invoiceline_id IS NULL THEN
        NEW.invoiceline_id := nextval('invoiceline_invoiceline_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_invoiceline_id
BEFORE INSERT ON invoiceline
FOR EACH ROW
EXECUTE FUNCTION reuse_invoiceline_id();
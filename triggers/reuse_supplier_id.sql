CREATE OR REPLACE FUNCTION reuse_supplier_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(supplier_id) + 1 INTO NEW.supplier_id
    FROM supplier p1
    WHERE NOT EXISTS (
        SELECT 1 FROM supplier p2 WHERE p2.supplier_id = p1.supplier_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.supplier_id IS NULL THEN
        NEW.supplier_id := nextval('supplier_supplier_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_supplier_id
BEFORE INSERT ON supplier
FOR EACH ROW
EXECUTE FUNCTION reuse_supplier_id();
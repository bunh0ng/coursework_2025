CREATE OR REPLACE FUNCTION check_supplier_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Supplier
        WHERE supplier_name = NEW.supplier_name
        AND (TG_OP = 'INSERT' OR supplier_id != NEW.supplier_id)
    ) THEN
        RAISE EXCEPTION 'Поставщик с названием "%" уже существует', NEW.supplier_name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_supplier_duplicate
BEFORE INSERT OR UPDATE ON Supplier
FOR EACH ROW
EXECUTE FUNCTION check_supplier_duplicate();
CREATE OR REPLACE FUNCTION check_supplier_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или parttype_id
    IF (((TG_OP = 'INSERT') OR (TG_OP = 'UPDATE')) AND 
        (OLD.contact_phone IS DISTINCT FROM NEW.contact_phone)) THEN
        
        IF EXISTS (
            SELECT 1 FROM supplier
            WHERE contact_phone = NEW.contact_phone
              AND supplier_id != NEW.supplier_id
        ) THEN
            RAISE EXCEPTION 'Номер телефона "%" уже занят', 
                NEW.contact_phone;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_supplier_duplicate
BEFORE INSERT ON supplier
FOR EACH ROW
EXECUTE FUNCTION check_supplier_duplicate();
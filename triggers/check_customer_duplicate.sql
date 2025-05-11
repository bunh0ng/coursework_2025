CREATE OR REPLACE FUNCTION check_customer_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или customertype_id
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND 
        (OLD.material IS DISTINCT FROM NEW.material OR 
         OLD.customertype_id IS DISTINCT FROM NEW.customertype_id)) THEN
        
        IF EXISTS (
            SELECT 1 FROM customer
            WHERE material = NEW.material
              AND customertype_id = NEW.customertype_id
              AND customer_id != NEW.customer_id
        ) THEN
            RAISE EXCEPTION 'Деталь с материалом "%" и ID типа % уже существует', 
                NEW.material, NEW.customertype_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_customer_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или customertype_id
    IF (((TG_OP = 'INSERT') OR (TG_OP = 'UPDATE')) AND 
        (OLD.customer_name IS DISTINCT FROM NEW.customer_name OR 
         OLD.city IS DISTINCT FROM NEW.city)) THEN
        
        IF EXISTS (
            SELECT 1 FROM customer
            WHERE customer_name = NEW.customer_name
              AND city = NEW.city
              AND customer_id != NEW.customer_id
        ) THEN
            RAISE EXCEPTION 'Покупатель с названием "%" из города % уже существует', 
                NEW.customer_name, NEW.city;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_customer_duplicate
BEFORE INSERT ON customer
FOR EACH ROW
EXECUTE FUNCTION check_customer_duplicate();
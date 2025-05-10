CREATE OR REPLACE FUNCTION check_customer_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Customer
        WHERE customer_name = NEW.customer_name
        AND city = NEW.city
        AND (TG_OP = 'INSERT' OR customer_id != NEW.customer_id)
    ) THEN
        RAISE EXCEPTION 'Клиент "%" из города "%" уже существует', NEW.customer_name, NEW.city;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_customer_duplicate
BEFORE INSERT OR UPDATE ON Customer
FOR EACH ROW
EXECUTE FUNCTION check_customer_duplicate();
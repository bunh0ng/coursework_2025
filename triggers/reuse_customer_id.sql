CREATE OR REPLACE FUNCTION reuse_customer_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(customer_id) + 1 INTO NEW.customer_id
    FROM customer p1
    WHERE NOT EXISTS (
        SELECT 1 FROM customer p2 WHERE p2.customer_id = p1.customer_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.customer_id IS NULL THEN
        NEW.customer_id := nextval('customer_customer_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_customer_id
BEFORE INSERT ON customer
FOR EACH ROW
EXECUTE FUNCTION reuse_customer_id();
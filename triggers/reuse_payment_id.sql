CREATE OR REPLACE FUNCTION reuse_payment_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(payment_id) + 1 INTO NEW.payment_id
    FROM payment p1
    WHERE NOT EXISTS (
        SELECT 1 FROM payment p2 WHERE p2.payment_id = p1.payment_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.payment_id IS NULL THEN
        NEW.payment_id := nextval('payment_payment_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_payment_id
BEFORE INSERT ON payment
FOR EACH ROW
EXECUTE FUNCTION reuse_payment_id();
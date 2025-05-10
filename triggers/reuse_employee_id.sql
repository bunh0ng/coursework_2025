CREATE OR REPLACE FUNCTION reuse_employee_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(employee_id) + 1 INTO NEW.employee_id
    FROM employee p1
    WHERE NOT EXISTS (
        SELECT 1 FROM employee p2 WHERE p2.employee_id = p1.employee_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.employee_id IS NULL THEN
        NEW.employee_id := nextval('employee_employee_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_employee_id
BEFORE INSERT ON employee
FOR EACH ROW
EXECUTE FUNCTION reuse_employee_id();
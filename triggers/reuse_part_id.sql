CREATE OR REPLACE FUNCTION reuse_part_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(part_id) + 1 INTO NEW.part_id
    FROM Part p1
    WHERE NOT EXISTS (
        SELECT 1 FROM Part p2 WHERE p2.part_id = p1.part_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.part_id IS NULL THEN
        NEW.part_id := nextval('part_part_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_part_id
BEFORE INSERT ON Part
FOR EACH ROW
EXECUTE FUNCTION reuse_part_id();
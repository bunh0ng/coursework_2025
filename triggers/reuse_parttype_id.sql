CREATE OR REPLACE FUNCTION reuse_parttype_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Пытаемся использовать минимальный свободный ID
    SELECT MIN(parttype_id) + 1 INTO NEW.parttype_id
    FROM parttype p1
    WHERE NOT EXISTS (
        SELECT 1 FROM parttype p2 WHERE p2.parttype_id = p1.parttype_id + 1
    );
    
    -- Если не нашли, используем стандартное поведение
    IF NEW.parttype_id IS NULL THEN
        NEW.parttype_id := nextval('parttype_parttype_id_seq');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_reuse_parttype_id
BEFORE INSERT ON parttype
FOR EACH ROW
EXECUTE FUNCTION reuse_parttype_id();
CREATE OR REPLACE FUNCTION check_parttype_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM PartType 
        WHERE type_name = NEW.type_name
        AND (TG_OP = 'INSERT' OR parttype_id != NEW.parttype_id)
    ) THEN
        RAISE EXCEPTION 'Тип детали с названием "%" уже существует', NEW.type_name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_parttype_duplicate
BEFORE INSERT OR UPDATE ON PartType
FOR EACH ROW
EXECUTE FUNCTION check_parttype_duplicate();
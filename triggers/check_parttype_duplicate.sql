CREATE OR REPLACE FUNCTION check_parttype_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или parttypetype_id
    IF (((TG_OP = 'INSERT') OR (TG_OP = 'UPDATE')) AND 
        (OLD.type_name IS DISTINCT FROM NEW.type_name)) THEN
        
        IF EXISTS (
            SELECT 1 FROM parttype
            WHERE type_name = NEW.type_name
              AND parttype_id != NEW.parttype_id
        ) THEN
            RAISE EXCEPTION 'Тип с названием "%" уже существует', 
                NEW.type_name;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_parttype_duplicate
BEFORE INSERT ON parttype
FOR EACH ROW
EXECUTE FUNCTION check_parttype_duplicate();

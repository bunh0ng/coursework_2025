CREATE OR REPLACE FUNCTION check_parttype_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или parttypetype_id
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND 
        (OLD.material IS DISTINCT FROM NEW.material OR 
         OLD.parttypetype_id IS DISTINCT FROM NEW.parttypetype_id)) THEN
        
        IF EXISTS (
            SELECT 1 FROM parttype
            WHERE material = NEW.material
              AND parttypetype_id = NEW.parttypetype_id
              AND parttype_id != NEW.parttype_id
        ) THEN
            RAISE EXCEPTION 'Деталь с материалом "%" и ID типа % уже существует', 
                NEW.material, NEW.parttypetype_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

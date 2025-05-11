CREATE OR REPLACE FUNCTION check_part_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    -- Только если изменяется material или parttype_id
    IF (TG_OP = 'INSERT') OR (TG_OP = 'UPDATE' AND 
        (OLD.material IS DISTINCT FROM NEW.material OR 
         OLD.parttype_id IS DISTINCT FROM NEW.parttype_id)) THEN
        
        IF EXISTS (
            SELECT 1 FROM Part
            WHERE material = NEW.material
              AND parttype_id = NEW.parttype_id
              AND part_id != NEW.part_id
        ) THEN
            RAISE EXCEPTION 'Деталь с материалом "%" и ID типа % уже существует', 
                NEW.material, NEW.parttype_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

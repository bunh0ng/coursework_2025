CREATE OR REPLACE FUNCTION check_part_duplicate()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Part
        WHERE material = NEW.material
        AND parttype_id = NEW.parttype_id
        AND (TG_OP = 'INSERT' OR part_id != NEW.part_id)
    ) THEN
        RAISE EXCEPTION 'Деталь с материалом "%" и типом ID % уже существует', 
            NEW.material, NEW.parttype_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_part_duplicate
BEFORE INSERT OR UPDATE ON Part
FOR EACH ROW
EXECUTE FUNCTION check_part_duplicate();
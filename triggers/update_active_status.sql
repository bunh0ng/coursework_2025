CREATE OR REPLACE FUNCTION update_part_active_status()
RETURNS TRIGGER AS $$
DECLARE 
    min_stock INT;
BEGIN
    SELECT min_stock_level INTO min_stock
    FROM Part
    WHERE part_id = NEW.part_id;

    IF NEW.quantity_in_stock < min_stock THEN
        NEW.is_active := FALSE;
    ELSE
        NEW.is_active := TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_part_active_status
BEFORE UPDATE OF quantity_in_stock ON Part
FOR EACH ROW
EXECUTE FUNCTION update_part_active_status();

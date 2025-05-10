CREATE OR REPLACE FUNCTION check_stock_level()
RETURNS TRIGGER AS $$
DECLARE
    current_stock INT;
BEGIN
    current_stock := (SELECT quantity_in_stock FROM Part WHERE part_id = NEW.part_id);
    
    IF current_stock < NEW.quantity THEN
        RAISE EXCEPTION 'Недостаточно товара на складе. Доступно: %, запрошено: %', 
              current_stock, NEW.quantity;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_invoice_line_insert
BEFORE INSERT ON InvoiceLine
FOR EACH ROW
EXECUTE FUNCTION check_stock_level();
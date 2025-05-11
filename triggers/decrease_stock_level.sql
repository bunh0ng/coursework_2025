CREATE OR REPLACE FUNCTION decrease_stock_on_invoiceline_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Part
    SET quantity_in_stock = quantity_in_stock - NEW.quantity
    WHERE part_id = NEW.part_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_decrease_stock_on_invoiceline_insert
AFTER INSERT ON InvoiceLine
FOR EACH ROW
EXECUTE FUNCTION decrease_stock_on_invoiceline_insert();

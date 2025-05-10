CREATE OR REPLACE FUNCTION update_invoice_total()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Invoice
    SET total_amount = (
        SELECT COALESCE(SUM(line_total), 0)
        FROM InvoiceLine
        WHERE invoice_id = NEW.invoice_id
    )
    WHERE invoice_id = NEW.invoice_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_invoiceline_insert
AFTER INSERT ON InvoiceLine
FOR EACH ROW
EXECUTE FUNCTION update_invoice_total();

CREATE TRIGGER trg_invoiceline_update
AFTER UPDATE ON InvoiceLine
FOR EACH ROW
EXECUTE FUNCTION update_invoice_total();

CREATE TRIGGER trg_invoiceline_delete
AFTER DELETE ON InvoiceLine
FOR EACH ROW
EXECUTE FUNCTION update_invoice_total();
CREATE OR REPLACE FUNCTION update_invoice_payment_status()
RETURNS TRIGGER AS $$
DECLARE
    total_paid DECIMAL := 0;
    total_due DECIMAL := 0;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO total_paid
    FROM Payment
    WHERE invoice_id = NEW.invoice_id;

    SELECT total_amount INTO total_due
    FROM Invoice
    WHERE invoice_id = NEW.invoice_id;

    UPDATE Invoice
    SET payment_status = CASE
        WHEN total_paid = 0 THEN 'Неоплачено'
        WHEN total_paid < total_due THEN 'Частично оплачено'
        WHEN total_paid >= total_due THEN 'Оплачено'
    END
    WHERE invoice_id = NEW.invoice_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_invoice_status
AFTER INSERT ON Payment
FOR EACH ROW
EXECUTE FUNCTION update_invoice_payment_status();

CREATE OR REPLACE FUNCTION prevent_early_payment()
RETURNS TRIGGER AS $$
DECLARE
    invoice_datee TIMESTAMP;
BEGIN
    SELECT invoice_date INTO invoice_datee
    FROM Invoice
    WHERE invoice_id = NEW.invoice_id;

    IF NEW.payment_date < invoice_datee THEN
        RAISE EXCEPTION 'Дата платежа не может быть раньше даты накладной';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_early_payment
BEFORE INSERT ON Payment
FOR EACH ROW
EXECUTE FUNCTION prevent_early_payment();

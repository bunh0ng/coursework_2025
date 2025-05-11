CREATE OR REPLACE FUNCTION prevent_payment_on_paid()
RETURNS TRIGGER AS $$
BEGIN
    IF (
        SELECT COALESCE(SUM(amount), 0)
        FROM Payment
        WHERE invoice_id = NEW.invoice_id
    ) >= (
        SELECT total_amount
        FROM Invoice
        WHERE invoice_id = NEW.invoice_id
    ) THEN
        RAISE EXCEPTION 'Накладная уже полностью оплачена';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_paymenton_paid
BEFORE INSERT ON Payment
FOR EACH ROW
EXECUTE FUNCTION prevent_payment_on_paid();

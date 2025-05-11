CREATE OR REPLACE FUNCTION prevent_overpayment()
RETURNS TRIGGER AS $$
DECLARE
    current_paid DECIMAL := 0;
    invoice_total DECIMAL := 0;
BEGIN
    -- Сумма уже внесённых платежей
    SELECT COALESCE(SUM(amount), 0)
    INTO current_paid
    FROM Payment
    WHERE invoice_id = NEW.invoice_id;

    -- Общая сумма накладной
    SELECT total_amount
    INTO invoice_total
    FROM Invoice
    WHERE invoice_id = NEW.invoice_id;

    -- Если платеж превысит допустимую сумму
    IF current_paid + NEW.amount > invoice_total THEN
        RAISE EXCEPTION 'Платёж приведет к переплате по накладной';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_overpayment
BEFORE INSERT ON Payment
FOR EACH ROW
EXECUTE FUNCTION prevent_overpayment();

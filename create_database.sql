CREATE TABLE PartType (
    parttype_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL,
    description TEXT
);
copy parttype FROM 'C:/tables/part_types.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Supplier (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(50),
    email VARCHAR(50)
);
copy supplier FROM 'C:/tables/suppliers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Part (
    part_id SERIAL PRIMARY KEY,
    material VARCHAR(50) NOT NULL,
    weight DECIMAL(10,2),
    price DECIMAL(10,2) NOT NULL,
    parttype_id SERIAL REFERENCES PartType(parttype_id),
    quantity_in_stock INT NOT NULL,
    supplier_id SERIAL REFERENCES Supplier(supplier_id),
    min_stock_level INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);
copy part FROM 'C:/tables/parts.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50),
    contact_phone VARCHAR(50),
    email VARCHAR(50)
);
copy customer FROM 'C:/tables/customers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Employee (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    second_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    hire_date DATE,
    age INT CHECK (age BETWEEN 18 AND 65)
);
copy employee FROM 'C:/tables/employees.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Invoice (
    invoice_id SERIAL PRIMARY KEY,
    invoice_date TIMESTAMP NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    customer_id SERIAL REFERENCES Customer(customer_id),
    employee_id SERIAL REFERENCES Employee(employee_id),
    payment_status VARCHAR(50) CHECK (payment_status IN ('Оплачено', 'Не оплачено', 'Частично оплачено')) DEFAULT 'Не оплачено'
);
copy invoice FROM 'C:/tables/invoices.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE InvoiceLine (
    invoiceline_id SERIAL PRIMARY KEY,
    invoice_id SERIAL REFERENCES Invoice(invoice_id),
    part_id INT REFERENCES Part(part_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL
);
copy invoiceline FROM 'C:/tables/invoice_lines.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

CREATE TABLE Payment (
    payment_id SERIAL PRIMARY KEY,
    invoice_id SERIAL REFERENCES Invoice(invoice_id),
    payment_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount > 0),
    payment_method VARCHAR(50) CHECK (payment_method IN ('Наличный расчет', 'Безналичный расчет')) DEFAULT 'Безналичный расчет'
);
COPY payment FROM 'C:/tables/payments.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

-- Индексы для ускорения
CREATE INDEX idx_part_parttype ON Part(parttype_id);
CREATE INDEX idx_part_supplier ON Part(supplier_id);
CREATE INDEX idx_invoice_customer ON Invoice(customer_id);
CREATE INDEX idx_invoice_employee ON Invoice(employee_id);
CREATE INDEX idx_invoice_date ON Invoice(invoice_date);
CREATE INDEX idx_invoiceline_part ON InvoiceLine(part_id);
CREATE INDEX idx_invoiceline_invoice ON InvoiceLine(invoice_id);
CREATE INDEX idx_payment_invoice ON Payment(invoice_id);
CREATE INDEX idx_payment_date ON Payment(payment_date);


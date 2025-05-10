CREATE OR REPLACE FUNCTION check_hire_age()
RETURNS TRIGGER AS $$
DECLARE
    hire_year INT;
    current_year INT;
    age_at_hire INT;
BEGIN
    -- Получаем текущий год и год найма
    current_year := EXTRACT(YEAR FROM CURRENT_DATE);
    hire_year := EXTRACT(YEAR FROM NEW.hire_date);
    
    -- Вычисляем примерный возраст на момент найма
    IF hire_year = current_year THEN
        age_at_hire := NEW.age;  -- Если наняли в этом году, возраст тот же
    ELSE
        age_at_hire := NEW.age - (current_year - hire_year);
    END IF;
    
    -- Проверяем, был ли сотрудник совершеннолетним на момент найма
    IF age_at_hire < 18 THEN
        RAISE EXCEPTION 
            'Сотрудник не мог быть нанят в % году в возрасте % лет (должно быть ≥18)',
            hire_year, age_at_hire;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для INSERT (добавление нового сотрудника)
CREATE TRIGGER trg_check_hire_age_insert
BEFORE INSERT ON Employee
FOR EACH ROW
EXECUTE FUNCTION check_hire_age();

-- Триггер для UPDATE (если изменили hire_date или age)
CREATE TRIGGER trg_check_hire_age_update
BEFORE UPDATE ON Employee
FOR EACH ROW
WHEN (OLD.hire_date IS DISTINCT FROM NEW.hire_date OR OLD.age IS DISTINCT FROM NEW.age)
EXECUTE FUNCTION check_hire_age();
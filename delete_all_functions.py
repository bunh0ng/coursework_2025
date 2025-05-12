import os
import psycopg2
from bot.config import database_settings

def get_connection():
    return psycopg2.connect(**database_settings)



# Подключение и выполнение
conn = get_connection()
cur = conn.cursor()
cur.execute("""
    DO $$
    DECLARE
        func_record RECORD;
    BEGIN
        FOR func_record IN 
            SELECT n.nspname AS schema_name, p.proname AS function_name,
                pg_get_function_identity_arguments(p.oid) AS args
            FROM pg_proc p
            LEFT JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
        LOOP
            EXECUTE format('DROP FUNCTION IF EXISTS %I.%I(%s) CASCADE', 
                        func_record.schema_name, 
                        func_record.function_name, 
                        func_record.args);
            RAISE NOTICE 'Dropped function: %.%(%s)', 
                        func_record.schema_name, 
                        func_record.function_name, 
                        func_record.args;
        END LOOP;
    END $$;
""")
conn.commit()
cur.close()
conn.close()


print('Все функции удалены.')

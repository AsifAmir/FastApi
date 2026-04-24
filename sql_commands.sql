select * from information_schema.tables where table_name = '#';


SELECT 
    column_name, 
    data_type, 
    character_maximum_length AS max_length,
    column_default AS default_value, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = '#';
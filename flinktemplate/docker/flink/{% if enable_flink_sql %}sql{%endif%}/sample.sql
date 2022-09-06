CREATE TABLE orders (
  order_number BIGINT,
  price        DECIMAL(32,2),
  buyer        ROW<first_name STRING, last_name STRING>,
  order_time   TIMESTAMP(3)
) WITH (
  'connector' = 'datagen'
);

CREATE TABLE print_table WITH ('connector' = 'print')
  LIKE orders;

INSERT INTO print_table SELECT * FROM orders;

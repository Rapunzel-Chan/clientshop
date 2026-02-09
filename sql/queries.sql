--Сумма товаров по каждому клиенту
SELECT
    c.name AS client_name,
    SUM(oi.quantity * oi.price_at_moment) AS total_sum
FROM client c
JOIN "order" o ON o.client_id = c.id
JOIN order_item oi ON oi.order_id = o.id
GROUP BY c.name;

--Количество дочерних элементов 1 уровня
SELECT
    parent.id,
    parent.name,
    COUNT(child.id) AS children_count
FROM category parent
LEFT JOIN category child
    ON child.parent_id = parent.id
GROUP BY parent.id, parent.name;

--VIEW: Топ-5 товаров за последний месяц
CREATE VIEW top_5_products_last_month AS
SELECT
    p.name AS product_name,
    root.name AS root_category,
    SUM(oi.quantity) AS total_quantity
FROM order_item oi
JOIN "order" o ON o.id = oi.order_id
JOIN product p ON p.id = oi.product_id
JOIN category c ON c.id = p.category_id
JOIN category root ON root.id = c.parent_id OR root.id = c.id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY p.name, root.name
ORDER BY total_quantity DESC
LIMIT 5;

--Решение по оптимизации
CREATE INDEX idx_order_created_at ON "order"(created_at);
CREATE INDEX idx_order_item_order ON order_item(order_id);
CREATE INDEX idx_order_item_product ON order_item(product_id);

ALTER TABLE product
ADD COLUMN root_category_id INT REFERENCES category(id);

CREATE MATERIALIZED VIEW top_5_products_last_month_mv AS
SELECT
    p.id AS product_id,
    SUM(oi.quantity) AS total_quantity
FROM order_item oi
JOIN "order" o ON o.id = oi.order_id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY p.id;

REFRESH MATERIALIZED VIEW top_5_products_last_month_mv;

CREATE TABLE order_2025_01 PARTITION OF "order"
FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

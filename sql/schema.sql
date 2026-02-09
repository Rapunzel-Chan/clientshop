Category (неограниченная вложенность)

| Поле      | Тип              | Описание               |
| --------- | ---------------- | ---------------------- |
| id        | PK               |                        |
| name      | varchar          | Наименование категории |
| parent_id | FK → category.id | Родительская категория |

Product (номенклатура)

| Поле        | Тип              |
| ----------- | ---------------- |
| id          | PK               |
| name        | varchar          |
| quantity    | int              |
| price       | numeric          |
| category_id | FK → category.id |

Client

| Поле    | Тип     |
| ------- | ------- |
| id      | PK      |
| name    | varchar |
| address | text    |

Order

| Поле       | Тип            |
| ---------- | -------------- |
| id         | PK             |
| client_id  | FK → client.id |
| created_at | timestamp      |

Order_item (нормализация, заказ из разного набора товаров)

| Поле            | Тип             |
| --------------- | --------------  |
| id              | PK              |
| order_id        | FK → order.id   |
| product_id      | FK → product.id |
| quantity        | int             |
| price_at_moment | numeric         |

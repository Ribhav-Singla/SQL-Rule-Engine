export interface TableColumn {
  name: string;
  type: string;
  constraint?: string;
}

export interface SchemaTable {
  name: string;
  columns: TableColumn[];
}

export const ecommerceSchema: SchemaTable[] = [
  {
    name: "customers",
    columns: [
      { name: "customer_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "first_name", type: "VARCHAR(100)" },
      { name: "last_name", type: "VARCHAR(100)" },
      { name: "email", type: "VARCHAR(255)" },
      { name: "phone", type: "VARCHAR(20)" },
      { name: "city", type: "VARCHAR(100)" },
      { name: "country", type: "VARCHAR(100)" },
      { name: "created_at", type: "DATE" },
    ],
  },
  {
    name: "categories",
    columns: [
      { name: "category_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "category_name", type: "VARCHAR(100)" },
      { name: "description", type: "TEXT" },
    ],
  },
  {
    name: "products",
    columns: [
      { name: "product_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "product_name", type: "VARCHAR(200)" },
      { name: "category_id", type: "INTEGER", constraint: "FK → categories" },
      { name: "price", type: "DECIMAL(10,2)" },
      { name: "stock_quantity", type: "INTEGER" },
      { name: "brand", type: "VARCHAR(100)" },
      { name: "rating", type: "DECIMAL(2,1)" },
    ],
  },
  {
    name: "orders",
    columns: [
      { name: "order_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "customer_id", type: "INTEGER", constraint: "FK → customers" },
      { name: "order_date", type: "DATE" },
      { name: "status", type: "VARCHAR(50)" },
      { name: "shipping_address", type: "VARCHAR(300)" },
      { name: "total_amount", type: "DECIMAL(10,2)" },
    ],
  },
  {
    name: "order_items",
    columns: [
      { name: "order_item_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "order_id", type: "INTEGER", constraint: "FK → orders" },
      { name: "product_id", type: "INTEGER", constraint: "FK → products" },
      { name: "quantity", type: "INTEGER" },
      { name: "unit_price", type: "DECIMAL(10,2)" },
    ],
  },
  {
    name: "reviews",
    columns: [
      { name: "review_id", type: "SERIAL", constraint: "PRIMARY KEY" },
      { name: "product_id", type: "INTEGER", constraint: "FK → products" },
      { name: "customer_id", type: "INTEGER", constraint: "FK → customers" },
      { name: "rating", type: "INTEGER", constraint: "CHECK 1-5" },
      { name: "comment", type: "TEXT" },
      { name: "review_date", type: "DATE" },
    ],
  },
];

use hackathon;
drop table if exists coded_products;
create table coded_products(
    productcode varchar(100) not null primary key,
    productname varchar(100)
)
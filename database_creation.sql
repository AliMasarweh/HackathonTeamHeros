-- create database hackathon;

use hackathon;
drop table if exists Stores_Products;
drop table if exists Stores;
drop table if exists Products;
drop table if exists Users;
drop table if exists coded_products;

create table Products(
    ProductID int not null auto_increment primary key,
    ProductName varchar(100)
);

create table Stores(
    StoreID int not null auto_increment primary key,
    StoreName varchar(20)
);

create table Stores_Products(
    StoreID int,
    ProductID int,
    Price float,
    Discount float default 0,
    MinQuantity int default 1,
    foreign key (StoreID) references Stores(StoreID),
    foreign key (ProductID) references Products(ProductID)
);

create table Users(
	ChatId int not null primary key,
    UserType varchar(30) default "client"
);
create table coded_products(
    productcode varchar(100) not null primary key,
    productname varchar(100)
);
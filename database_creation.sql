-- create database hackathon;

use hackathon;
drop table if exists Stores_Products;
drop table if exists Stores;
drop table if exists Products;
drop table if exists Users;

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
    foreign key (StoreID) references Stores(StoreID),
    foreign key (ProductID) references Products(ProductID)
);

create table Users(
	ChatId int,
    UserType varchar(30) default "client"
);

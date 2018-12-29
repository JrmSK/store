CREATE DATABASE store;

USE store;

CREATE TABLE category(
name VARCHAR(30) UNIQUE,
id INT AUTO_INCREMENT,
PRIMARY KEY (id)
);

CREATE TABLE product(
id_product INT AUTO_INCREMENT,
title VARCHAR(30) UNIQUE,
category_name VARCHAR(30),
description VARCHAR(500),
favorite ENUM("0","1"),
price INT,
img_url VARCHAR(100),
PRIMARY KEY (id_product)
);

DROP TABLE category;
DROP TABLE product;
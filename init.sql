use fcs;

drop table borrow;
drop table user;
drop table book;

CREATE TABLE user(
	username varchar(50) primary key,
	name varchar(100) not null,
	role varchar(20) not null,
	password varchar(500) not null,
	active int not null
);

CREATE TABLE book(
	bookname varchar(100) primary key,
	count int not null,
	price int not null,
	active int not null,
	description varchar(500) not null
);

CREATE TABLE borrow(
	username varchar(50),
	bookname varchar(100),
	issuedatetime varchar(50) not null,
	returndatetime varchar(50),
	foreign key (username) references user(username),
	foreign key (bookname) references book(bookname),
	primary key(username,bookname,issuedatetime)
);
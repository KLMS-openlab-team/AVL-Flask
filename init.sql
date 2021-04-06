use fcs;

drop table borrow;
drop table user;
drop table book;

CREATE TABLE user(
	username varchar(50) primary key,
	name varchar(100) not null,
	role varchar(20) not null,
	password varchar(500) not null,
	active int not null,
	due int not null
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


select * from book;
insert into book values('harrypotter-1',2,100,1,'good book');
insert into book values('harrypotter-2',2,100,1,'good book');
insert into book values('harrypotter-3',2,100,1,'good book');

select * from user;
insert into user values('user1','user1','user','$2b$12$TbHvUtoM1psc9LxbYDCc7OAgkAnMDioH.QXljlj9HgsIg42EnPVWS',1,0);
insert into user values('user2','user2','user','$2b$12$k1tSN8QDGUHZQPZWDL..c.Hbb8rkj3ad5YvgUtdcUbkNd3u2UAjfa',1,0);
insert into user values('admin1','admin1','admin','$2b$12$ec292NUQEH3w9Ra6gObJDOlesvGDePRlEDFhFT3HGZVKHLB.70Tzu',1,0);
insert into user values('admin2','admin2','admin','$2b$12$vK8AhPRNiwqhamoER7q4XuONR5AzBqS59Qgs4GkNXECYUTzuLbYAm',1,0);

select * from borrow;
insert into borrow values('user1','harrypotter-1','2021-04-05 13:06:20.677224','2021-04-06 13:06:20.677224');
insert into borrow values('user2','harrypotter-1','2021-04-05 13:06:20.677224',null);
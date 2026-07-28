create table message (
	id UUID primary key,
	contact UUID not null,
	account UUID not null,
	body TEXT,
	voice BYTEA,
	transcription TEXT,
	created timestamp default now()
);

create table account(
	id uuid primary key,
	name varchar(60),
	phone varchar(20),
	mail varchar(120),
	password_hash varchar(120)
);

create table contact(
	id uuid primary key,
	account uuid not null,
	name varchar(60),
	phone varchar(20),
	mail varchar(120)
);
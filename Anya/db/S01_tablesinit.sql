CREATE TABLE IF NOT EXISTS temp_messages(
	id UUID primary key,
	sender varchar(60),
	body Text,
	moment timestamp,
	account UUID
);

CREATE TABLE IF NOT EXISTS pers_messages(
	id UUID primary key,
	sender varchar(60),
	body Text,
	moment timestamp,
	account UUID
);

CREATE TABLE IF NOT EXISTS account(
	id UUID primary key,
	person varchar(60),
	email varchar(120),
	password_hash varchar(120)
);

ALTER TABLE public.temp_messages 
ALTER COLUMN moment SET DEFAULT now();

ALTER TABLE public.temp_messages 
ADD COLUMN receiver varchar(120);

ALTER TABLE public.temp_messages 
DROP COLUMN sender;

ALTER TABLE public.temp_messages 
ADD COLUMN sender varchar(120);
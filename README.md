# flask-tenis-app
Projeto em python para trabalho da faculdade

Para inicializar basta criar um banco de dados postgres com as seguintes credenciais:
database="db_loja_tenis",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
       
Em seguida: Criar as tabelas no banco de dados criado

CREATE TABLE usuarios (
	id serial PRIMARY KEY,
	nome VARCHAR (100) NOT NULL,
	email VARCHAR (50) NOT NULL,
	senha VARCHAR (255) NOT NULL
);

create table produtos (
	id serial PRIMARY KEY,
	nome VARCHAR (100) NOT NULL,
	descricao VARCHAR(200) NOT NULL,
	marcaVARCHAR(50) NOT NULL,
	imagem VARCHAR(255) NOT NULL,
	preco NUMERIC NOT NULL
);

CREATE TABLE importados (
	id serial PRIMARY KEY,
	valor VARCHAR (100) NOT NULL
);

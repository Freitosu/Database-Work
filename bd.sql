-- Banco de dados do Postgres
DROP TABLE IF EXISTS dw.fato_venda CASCADE;
DROP TABLE IF EXISTS dw.dim_jogo CASCADE;
DROP TABLE IF EXISTS dw.dim_tempo CASCADE;

CREATE TABLE dw.dim_jogo (
    jogo_id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    categoria TEXT,
    ano INTEGER,
    descricao TEXT,
    duracao INTEGER
);

CREATE TABLE dw.dim_tempo (
    tempo_id SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    ano INTEGER,
    mes INTEGER,
    dia INTEGER
);

CREATE TABLE dw.fato_venda (
    fato_id SERIAL PRIMARY KEY,
    jogo_id INTEGER REFERENCES dw.dim_jogo(jogo_id),
    tempo_id INTEGER REFERENCES dw.dim_tempo(tempo_id),
    preco NUMERIC(10,2),
    quantidade INTEGER
);

DROP TABLE IF EXISTS Usuario;

CREATE TABLE Usuario (
	UsrCodigo INTEGER NOT NULL PRIMARY KEY,
	UsrNome TEXT NOT NULL,
	UsrBarra TEXT,
	UsrProvisorio TEXT,
	UsrProvisorioValidade INTEGER,
	UsrValidacao INTEGER
);

DROP TABLE IF EXISTS Movimento;

CREATE TABLE Movimento (
	MovID INTEGER PRIMARY KEY,
	MovData INTEGER NOT NULL,
	MovBarra TEXT NOT NULL,
	MovSentido TEXT NOT NULL,
	MovBloqueado INTEGER DEFAULT 0 NOT NULL,
	MovForaHorario INTEGER DEFAULT 0 NOT NULL,
	MovProvisorio INTEGER DEFAULT 0 NOT NULL,
	UsrCodigo INTEGER,
	FOREIGN KEY(UsrCodigo) REFERENCES Usuario(UsrCodigo)
);

DROP TABLE IF EXISTS Usuario;

CREATE TABLE Usuario (
	UsrCodigo INTEGER NOT NULL PRIMARY KEY,
	UsrNome TEXT NOT NULL,
	UsrBarra TEXT,
	UsrProvisorio TEXT,
	UsrProvisorioValidade INTEGER
);

INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (5079,'Daniel', '72:8:6B:1F:E','',0);

DROP TABLE IF EXISTS Horario;

CREATE TABLE Horario (
	HorID INTEGER PRIMARY KEY,
	HorDia INTEGER NOT NULL,
	HorInicio TEXT NOT NULL,
	HorFim TEXT NOT NULL,
	HorSentido TEXT NOT NULL,
	UsrCodigo INTEGER NOT NULL,
	FOREIGN KEY(UsrCodigo) REFERENCES Usuario(UsrCodigo)
);

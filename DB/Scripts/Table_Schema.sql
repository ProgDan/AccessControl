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
	UsrProvisorioValidade INTEGER,
	UsrValidacao INTEGER
);

INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (5079,'Daniel','72:8:6B:1F:E','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (1,'Blue1','31:DF:92:EF:93','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (2,'Blue2','E7:5E:16:D3:7C','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (3,'Blue3','59:A5:8B:4C:3B','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (4,'Blue4','D9:A5:EA:4B:DD','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (5,'Blue5','E:3:16:D3:C8','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (6,'Yellow1','3:5D:2:BD:E1','',0);
INSERT INTO Usuario (UsrCodigo, UsrNome, UsrBarra, UsrProvisorio, UsrProvisorioValidade) VALUES (7,'Yellow2','E3:ED:1:BD:B2','',0);

DROP TABLE IF EXISTS Horario;

CREATE TABLE Horario (
	HorID INTEGER PRIMARY KEY,
	HorDia INTEGER NOT NULL,
	HorInicio TEXT NOT NULL,
	HorFim TEXT NOT NULL,
	HorSentido TEXT NOT NULL,
	HorValidacao INTEGER,
	UsrCodigo INTEGER NOT NULL,
	FOREIGN KEY(UsrCodigo) REFERENCES Usuario(UsrCodigo)
);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'00:00','23:59','A',0,5079);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'00:00','23:59','A',0,5079);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'00:00','23:59','A',0,5079);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'00:00','23:59','A',0,5079);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'00:00','23:59','A',0,5079);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'07:00','12:35','A',0,1);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'07:00','12:35','A',0,1);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'07:00','12:35','A',0,1);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'07:00','12:35','A',0,1);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'07:00','12:35','A',0,1);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'07:00','12:35','A',0,2);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'07:00','12:35','A',0,2);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'07:00','12:35','A',0,2);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'07:00','12:35','A',0,2);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'07:00','12:35','A',0,2);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'07:00','12:35','A',0,3);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'07:00','12:35','A',0,3);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'07:00','12:35','A',0,3);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'07:00','12:35','A',0,3);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'07:00','12:35','A',0,3);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'07:00','12:35','A',0,4);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'07:00','12:35','A',0,4);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'07:00','12:35','A',0,4);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'07:00','12:35','A',0,4);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'07:00','12:35','A',0,4);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'07:00','12:35','A',0,5);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'07:00','12:35','A',0,5);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'07:00','12:35','A',0,5);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'07:00','12:35','A',0,5);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'07:00','12:35','A',0,5);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'13:45','18:30','A',0,6);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'13:45','18:30','A',0,6);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'13:45','18:30','A',0,6);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'13:45','18:30','A',0,6);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'13:45','18:30','A',0,6);

INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (1,'13:45','18:30','A',0,7);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (2,'13:45','18:30','A',0,7);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (3,'13:45','18:30','A',0,7);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (4,'13:45','18:30','A',0,7);
INSERT INTO Horario (HorDia, HorInicio, HorFim, HorSentido, HorValidacao, UsrCodigo) VALUES (5,'13:45','18:30','A',0,7);

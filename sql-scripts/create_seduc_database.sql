
CREATE DATABASE sqldb_seduc;

CREATE TABLE aluno(
   matricula int NOT NULL,
   nome nvarchar(100) NOT NULL,
   data_mat date NOT NULL,
   turno nvarchar(10) NOT NULL,
   serie smallint NOT NULL,
   id_escola smallint NOT NULL,

   CONSTRAINT aluno_PK PRIMARY KEY (matricula),
   CONSTRAINT aluno_FK FOREIGN KEY (id_escola)
   )ON sqldb_seduc;

CREATE TABLE escola(
   id_escola int NOT NULL,
   nome nvarchar(100) NOT NULL,
   endereco nvarchar(100) NOT NULL,
   cidade nvarchar(50) NOT NULL

   CONSTRAINT escola_PK PRIMARY KEY (id_escola)
   )ON sqldb_seduc;

CREATE TABLE disciplina(
   id_disciplina int NOT NULL,
   nome nvarchar(50) NOT NULL,

   CONSTRAINT disciplina_PK PRIMARY KEY (id_disciplina)
   )ON sqldb_seduc;

CREATE TABLE matricula(
   id int NOT NULL,
   ano int NOT NULL,
   matricula_aluno int NOT NULL,
   id_escola int NOT NULL,
   id_disciplina int NOT NULL,
   serie smallint NOT NULL,
   nota float NOTNULL,
   status boolean NOT NULL,

   CONSTRAINT mat_PK PRIMARY KEY (id)
   )ON sqldb_seduc;

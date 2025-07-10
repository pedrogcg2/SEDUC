CREATE DATABASE sqldb_seduc;

CREATE TABLE escola(
   id_escola varchar(20) PRIMARY KEY,
   nome varchar(100) NOT NULL,
   endereco varchar(100) NOT NULL,
   cidade varchar(50) NOT NULL
);

CREATE TABLE aluno(
   matricula int NOT NULL,
   nome varchar(100) NOT NULL,
   data_mat date NOT NULL,
   turno varchar(10) NOT NULL,
   serie smallint NOT NULL,
   id_escola varchar(20) NOT NULL,
   CONSTRAINT aluno_PK PRIMARY KEY (matricula),
   CONSTRAINT aluno_FK FOREIGN KEY (id_escola) REFERENCES escola(id_escola)
);

CREATE TABLE disciplina(
   id_disciplina SERIAL PRIMARY KEY,
   nome varchar(50) NOT NULL
);

CREATE TABLE matricula(
   id SERIAL PRIMARY KEY,
   ano int NOT NULL,
   matricula_aluno int NOT NULL,
   id_escola varchar(20) NOT NULL,
   id_disciplina int NOT NULL,
   serie smallint NOT NULL,
   nota float NOT NULL,
   status boolean NOT NULL,
   CONSTRAINT mat_aluno_FK FOREIGN KEY (matricula_aluno) REFERENCES aluno(matricula),
   CONSTRAINT mat_escola_FK FOREIGN KEY (id_escola) REFERENCES escola(id_escola),
   CONSTRAINT mat_disciplina_FK FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina)
);

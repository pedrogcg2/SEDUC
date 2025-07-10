
CREATE DATABASE sqldb_seduc;

\c sqldb_seduc;

CREATE TABLE escola(
   id_escola SERIAL PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   endereco VARCHAR(100) NOT NULL,
   cidade VARCHAR(50) NOT NULL
);

CREATE TABLE aluno(
   matricula SERIAL PRIMARY KEY,
   nome VARCHAR(100) NOT NULL,
   data_mat DATE NOT NULL,
   turno VARCHAR(10) NOT NULL,
   serie SMALLINT NOT NULL,
   id_escola SMALLINT NOT NULL,
   CONSTRAINT aluno_FK FOREIGN KEY (id_escola) REFERENCES escola(id_escola)
);

CREATE TABLE disciplina(
   id_disciplina SERIAL PRIMARY KEY,
   nome VARCHAR(50) NOT NULL
);

CREATE TABLE matricula(
   id SERIAL PRIMARY KEY,
   ano INT NOT NULL,
   matricula_aluno INT NOT NULL,
   id_escola INT NOT NULL,
   id_disciplina INT NOT NULL,
   serie SMALLINT NOT NULL,
   nota FLOAT NOT NULL,
   status BOOLEAN NOT NULL,
   CONSTRAINT matricula_aluno_FK FOREIGN KEY (matricula_aluno) REFERENCES aluno(matricula),
   CONSTRAINT matricula_escola_FK FOREIGN KEY (id_escola) REFERENCES escola(id_escola),
   CONSTRAINT matricula_disciplina_FK FOREIGN KEY (id_disciplina) REFERENCES disciplina(id_disciplina)
);

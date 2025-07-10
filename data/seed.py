import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load CSV
df = pd.read_csv("data/dados_simulados_educacao.csv")

# Clean up and normalize data
df["Média Anual"] = df["Média Anual"].str.replace(",", ".").astype(float)
df["Aprovado"] = df["Aprovado"].map({"Sim": True, "Não": False})
df["Série"] = df["Série"].str.extract(r"(\d+)").astype(int)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="sqldb-seduc",
    user="master",
    password="HgAXVS5uWph3",
    host="postgres",
    port="5432"
)
cur = conn.cursor()

# Caches to avoid re-inserts
escola_ids = {}
disciplina_ids = {}
aluno_ids = {}
aluno_appearance_tracker = {}
for _, row in df.iterrows():
    # --- Escola ---
    escola_key = (row["Escola"], row["Cidade"])
    if escola_key not in escola_ids:
        cur.execute("""
            INSERT INTO escola (nome, endereco, cidade)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING id_escola
        """, (row["Escola"], "Endereco Exemplo", row["Cidade"]))
        result = cur.fetchone()
        if result:
            escola_id = result[0]
        else:
            cur.execute("SELECT id_escola FROM escola WHERE nome = %s AND cidade = %s", (row["Escola"], row["Cidade"]))
            escola_id = cur.fetchone()[0]
        escola_ids[escola_key] = escola_id
    else:
        escola_id = escola_ids[escola_key]

    # --- Disciplina ---
    if row["Disciplina"] not in disciplina_ids:
        cur.execute("""
            INSERT INTO disciplina (nome)
            VALUES (%s)
            ON CONFLICT DO NOTHING
            RETURNING id_disciplina
        """, (row["Disciplina"],))
        result = cur.fetchone()
        if result:
            disc_id = result[0]
        else:
            cur.execute("SELECT id_disciplina FROM disciplina WHERE nome = %s", (row["Disciplina"],))
            disc_id = cur.fetchone()[0]
        disciplina_ids[row["Disciplina"]] = disc_id
    else:
        disc_id = disciplina_ids[row["Disciplina"]]

    # --- Aluno ---
    aluno_key = (row["Aluno"], row["Turno"], escola_id)

    if aluno_key not in aluno_appearance_tracker:
        aluno_appearance_tracker[aluno_key] = 0
    else:
        aluno_appearance_tracker[aluno_key] += 1

    year = 2018 + aluno_appearance_tracker[aluno_key]
    data_mat = f"{year}-02-01"

    if row["matricula_aluno"] not in aluno_ids:
        cur.execute("""
            INSERT INTO aluno (nome, data_mat, turno, serie, id_escola)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING matricula
        """, (
            row["Aluno"],
            data_mat,
            row["Turno"],
            int(row["Série"]),
            escola_id
        ))
        result = cur.fetchone()
        if result:
            aluno_ids[row["matricula_aluno"]] = result[0]

    # --- Matricula ---
    cur.execute("""
        INSERT INTO matricula (
            ano, matricula_aluno, id_escola, id_disciplina, serie, nota, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["Ano"]),
        aluno_ids[row["matricula_aluno"]],
        escola_id,
        disc_id,
        int(row["Série"]),
        row["Média Anual"],
        row["Aprovado"]
    ))

# Commit and close
conn.commit()
cur.close()
conn.close()

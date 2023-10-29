from fastapi import FastAPI
import uvicorn
import psycopg2
from pydantic import BaseModel


class Aluno(BaseModel):
  nome: str
  idade: int
  nota_primeiro_semestre: float
  nota_segundo_semestre: float
  nome_professor: str
  numero_sala: int


app = FastAPI()

@app.get('/conectar')
def conectar():

  connection = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123456",
    database="bd_escola"
  )
  return connection

@app.post('/criar_aluno')
def criar_aluno(aluno: Aluno):

  connection = conectar()
  cursor = connection.cursor()

  # Insere o aluno no banco de dados
  sql = "INSERT INTO alunos (nome, idade, nota_primeiro_semestre, nota_segundo_semestre, nome_professor, numero_sala) VALUES (%s, %s, %s, %s, %s, %s)"
  val = (aluno.nome, aluno.idade, aluno.nota_primeiro_semestre, aluno.nota_segundo_semestre, aluno.nome_professor, aluno.numero_sala)
  cursor.execute(sql, val)

  connection.commit()
  return cursor.lastrowid

@app.get('/alunos')
def get_alunos():

  connection = conectar()
  cursor = connection.cursor()

  # Seleciona todos os alunos
  sql = "SELECT * FROM alunos"
  cursor.execute(sql)
  alunos = cursor.fetchall()

  return alunos

@app.get('/alunos/nome/<nome>')
def get_alunos_por_nome(nome: str):

  connection = conectar()
  cursor = connection.cursor()

  # Seleciona os alunos pelo nome
  sql = "SELECT * FROM alunos WHERE nome = %s"
  val = (nome,)
  cursor.execute(sql, val)
  alunos = cursor.fetchall()

  return alunos

@app.get('/alunos/nota/<nota>')
def get_alunos_por_nota(nota: float):

  connection = conectar()
  cursor = connection.cursor()

  # Seleciona os alunos pela nota
  sql = "SELECT * FROM alunos WHERE nota_primeiro_semestre >= %s"
  val = (nota,)
  cursor.execute(sql, val)
  alunos = cursor.fetchall()

  return alunos

if __name__ == '__main__':
  uvicorn.run(app, host='00.00.00.00', port=8000)

from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
import uvicorn


class Aluno(BaseModel):
  nome: str
  idade: int
  nota_primeiro_semestre: float
  nota_segundo_semestre: float
  nome_professor: str
  numero_sala: int


app = FastAPI(debug=True)

@app.get('/conectar')
def conectar():

  connection = psycopg2.connect(
    host="dpg-ckushv3amefc73cek860-a.oregon-postgres.render.com",
    port=5432,
    user="root",
    password="tOqBSmsaLEie6ZSM2GPcewVCZ1DScvL7",
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

@app.post('/atualizar_aluno/<id>')
def atualizar_aluno(id: int, aluno: Aluno):

  connection = conectar()
  cursor = connection.cursor()

  # Atualiza o aluno no banco de dados
  sql = "UPDATE alunos SET nome = %s, idade = %s, nota_primeiro_semestre = %s, nota_segundo_semestre = %s, nome_professor = %s, numero_sala = %s WHERE id = %s"
  val = (aluno.nome, aluno.idade, aluno.nota_primeiro_semestre, aluno.nota_segundo_semestre, aluno.nome_professor, aluno.numero_sala, id)
  cursor.execute(sql, val)

  connection.commit()
  return aluno

@app.delete('/deletar_aluno/<id>')
def deletar_aluno(id: int):

  connection = conectar()
  cursor = connection.cursor()

  # Exclui o aluno do banco de dados
  sql = "DELETE FROM alunos WHERE id = %s"
  val = (id,)
  cursor.execute(sql, val)

  connection.commit()
  return id

if __name__ == '__main__':

  # Atualiza o código para passar o parâmetro send à função principal do aplicativo

  from gunicorn import gunicorn

  def main():
    app

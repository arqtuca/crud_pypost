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



app = FastAPI(debug=True)

@app.get("/")
def home():
    return "Este é um projeto de exemplo que inclui uma aplicação CRUD desenvolvida em Python com o framework FastAPI. A aplicação é destinada a realizar operações de Create, Read, Update e Delete (CRUD) em um banco de dados MySQL. O objetivo principal deste projeto é demonstrar como criar uma aplicação CRUD simples e como implantá-la em uma plataforma de hospedagem, no caso, o Render."

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



@app.put('/atualizar_aluno/<id>')
def atualizar_aluno(id: int, aluno: Aluno):

  connection = conectar()
  cursor = connection.cursor()

  # Valida os dados do aluno
  aluno.validate()

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

import os

port = int(os.environ.get("PORT", 10000))  # Use a porta padrão 8080 se a variável de ambiente não estiver definida

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=port)

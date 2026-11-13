
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



class BancoDados:
    def conectar(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="gestao_esportiva"
        )



class Modalidade:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao


class Treinador:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone


class Equipe:
    def __init__(self, nome, categoria, id_modalidade, id_treinador):
        self.nome = nome
        self.categoria = categoria
        self.id_modalidade = id_modalidade
        self.id_treinador = id_treinador



class DAO:
    def __init__(self):
        self.banco = BancoDados()

    def consultar(self, tabela):
        conexao = self.banco.conectar()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(f"SELECT * FROM {tabela}")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    def cadastrar(self, sql, valores):
        conexao = self.banco.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Error:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()



class ModalidadeDAO(DAO):
    def listar(self):
        return self.consultar("modalidade")

    def inserir(self, modalidade):
        sql = """
            INSERT INTO modalidade (nome, descricao)
            VALUES (%s, %s)
        """
        return self.cadastrar(
            sql,
            (modalidade.nome, modalidade.descricao)
        )



class TreinadorDAO(DAO):
    def listar(self):
        return self.consultar("treinador")

    def inserir(self, treinador):
        sql = """
            INSERT INTO treinador (nome, telefone)
            VALUES (%s, %s)
        """
        return self.cadastrar(
            sql,
            (treinador.nome, treinador.telefone)
        )



class EquipeDAO(DAO):
    def listar(self):
        return self.consultar("equipe")

    def inserir(self, equipe):
        sql = """
            INSERT INTO equipe
            (nome, categoria, id_modalidade, id_treinador)
            VALUES (%s, %s, %s, %s)
        """
        return self.cadastrar(
            sql,
            (
                equipe.nome,
                equipe.categoria,
                equipe.id_modalidade,
                equipe.id_treinador
            )
        )



@app.errorhandler(Error)
def erro_banco(erro):
    return jsonify({
        "erro": "Erro ao acessar o banco de dados",
        "detalhes": str(erro)
    }), 500


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensagem": "Sistema de Gestão Esportiva funcionando!",
        "tecnologias": ["Python", "Flask", "MySQL", "POO"]
    })



@app.route("/modalidades", methods=["GET"])
def listar_modalidades():
    dao = ModalidadeDAO()
    return jsonify(dao.listar())


@app.route("/modalidades", methods=["POST"])
def cadastrar_modalidade():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome obrigatório"}), 400

    descricao = dados.get("descricao")
    modalidade = Modalidade(nome.strip(), descricao)

    dao = ModalidadeDAO()
    novo_id = dao.inserir(modalidade)

    return jsonify({
        "mensagem": "Modalidade cadastrada!",
        "id_modalidade": novo_id
    }), 201



@app.route("/treinadores", methods=["GET"])
def listar_treinadores():
    dao = TreinadorDAO()
    return jsonify(dao.listar())


@app.route("/treinadores", methods=["POST"])
def cadastrar_treinador():
    dados = request.get_json(silent=True) or {}

    nome = dados.get("nome")
    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome obrigatório"}), 400

    treinador = Treinador(
        nome.strip(),
        dados.get("telefone")
    )

    dao = TreinadorDAO()
    novo_id = dao.inserir(treinador)

    return jsonify({
        "mensagem": "Treinador cadastrado!",
        "id_treinador": novo_id
    }), 201


# ROTAS DE EQUIPES
@app.route("/equipes", methods=["GET"])
def listar_equipes():
    dao = EquipeDAO()
    return jsonify(dao.listar())


@app.route("/equipes", methods=["POST"])
def cadastrar_equipe():
    dados = request.get_json(silent=True) or {}

    campos = ["nome", "id_modalidade", "id_treinador"]

    if any(dados.get(campo) is None for campo in campos):
        return jsonify({
            "erro": "Nome, modalidade e treinador são obrigatórios"
        }), 400

    try:
        id_modalidade = int(dados["id_modalidade"])
        id_treinador = int(dados["id_treinador"])
    except (ValueError, TypeError):
        return jsonify({"erro": "IDs devem ser números"}), 400

    nome = dados["nome"]
    if not isinstance(nome, str) or not nome.strip():
        return jsonify({"erro": "Nome inválido"}), 400

    equipe = Equipe(
        nome.strip(),
        dados.get("categoria"),
        id_modalidade,
        id_treinador
    )

    dao = EquipeDAO()

    try:
        novo_id = dao.inserir(equipe)
    except mysql.connector.IntegrityError:
        return jsonify({
            "erro": "Modalidade ou treinador não encontrado"
        }), 400

    return jsonify({
        "mensagem": "Equipe cadastrada!",
        "id_equipe": novo_id
    }), 201


if __name__ == "__main__":
    app.run(debug=True)

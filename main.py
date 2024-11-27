from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import logging
import oracledb
from walletcredentials import uname, pwd, dsn, cdir, wltloc, wltpwd

app = Flask(__name__, static_folder="static")
app.secret_key = "your_secret_key"  #importante para a sessão

#configurando o logging corretamente
logging.basicConfig(level=logging.INFO)

#função para conexão ao banco e execução de SQL
def execute_sql(sql, params=None, fetch=False):
    try:
        with oracledb.connect(user=uname, password=pwd, dsn=dsn, config_dir=cdir, wallet_location=wltloc, wallet_password=wltpwd) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, params or {})
                if fetch:
                    return cursor.fetchone()
                connection.commit()
    except Exception as e:
        logging.error(f"Erro ao executar SQL: {e}")
        raise

#rota para renderizar a página inicial
@app.route("/")
def login():
    return render_template("index.html")

# Rota de registro de usuário
@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    emailUsuario = request.form.get('email')
    senha = request.form.get('password')

    codigo = request.form.get('codigo') #matricula/id
    
    matricula = request.form.get('matricula')
    cpf = request.form.get('cpf')
    campus = request.form.get('campus')


    if not nome or not emailUsuario or not senha or not codigo or not campus:
        return jsonify({"error": "Os campos nome, email, senha codigo e campus são obrigatórios"}), 400

    try:
        #ESTÁ SEM o CÓDIGO/ID DE USUARIO POR ENQUNATO
        sql = "INSERT INTO USUARIO (nome, email, senha,matricula,cpf,campus) VALUES (:nome, :email, :password, :matricula, :cpf)"
        execute_sql(sql, {"campus": campus,"nome": nome, "email": emailUsuario, "password": senha, "matricula": matricula ,"cpf": cpf})

        sql = 'SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL = emailUsuario'
        idUsuario = execute_sql(sql, {'emailUsuario': emailUsuario}, fetch=True)

        sql = 'SELECT tipo_usuario FROM USUARIO WHERE id_usario = :idUsuario'
        tipoUsuario = execute_sql(sql, {"idUsuario": idUsuario}, fetch=True)

        session['emailLogado'] = emailUsuario
        session['idLogado'] = idUsuario
        session['tipoLogado'] = tipoUsuario

        return redirect(url_for('home'))
    except oracledb.IntegrityError:
        return jsonify({"error": "Email já registrado"}), 400
    except Exception as e:
        logging.error(f"Erro no registro do usuário: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500


# Rota de login de usuário
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    try:
        query = "SELECT senha FROM USUARIO WHERE EMAIL = :email"
        result = execute_sql(query, {"email": email}, fetch=True)

        if result and result[0] == senha:
            sql = 'SELECT id_usuario FROM USUARIO WHERE EMAIL = :email'
            idUsuario = execute_sql(sql, {"email": email}, fetch=True)

            #pegar tipo de usuario
            sql = 'SELECT tipo_usuario FROM USUARIO WHERE id_usario = :idUsuario'
            tipoUsuario = execute_sql(sql, {"idUsuario": idUsuario}, fetch=True)
            
            session['emailLogado'] = email
            session['idLogado'] = idUsuario
            session['tipoLogado'] = tipoUsuario

            return redirect(url_for('home'))
        else:
            return jsonify({"error": "Credenciais inválidas"}), 401
    except Exception as e:
        logging.error(f"Erro no login: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500


#rota para página do usuário
@app.route('/usuario')
def home():
    emailUsuario = session.get('emailLogado')
    if not emailUsuario:
        return redirect(url_for('login'))
    
    #pegar o id do usuario
    sql = "SELECT nome, id_usuario, tipo_usuario FROM USUARIO WHERE USER_EMAIL = :email"
    nomeUsuario, idUsuario, tipoUsuario = execute_sql(sql, {"email": emailUsuario}, fetch=True)

    if not nomeUsuario:
        return jsonify({"error": "Usuário não encontrado"}), 400

    session['idLogado'] = idUsuario
    session['tipoLogado'] = tipoUsuario

    #ADICIONAR VARIAVEL COM CODIGO PARA ACHAR RESERVAS DO USUARIO E BLA BLA BLA

    if tipoUsuario == 'aluno':
        return render_template('indexAluno.html', user_name=nomeUsuario, user_id = idUsuario, user_tipo = tipoUsuario)
    
    if tipoUsuario == 'servidor':
        return render_template('indexServidor.html', user_name=nomeUsuario, user_id = idUsuario, user_tipo = tipoUsuario)
    
    if tipoUsuario == 'administrador':
        return render_template('indexAdministrador.html', user_name=nomeUsuario, user_id = idUsuario, user_tipo = tipoUsuario)


    return render_template('index.html', user_name=nomeUsuario, user_id = idUsuario, user_tipo = tipoUsuario)

#rota da solicitação
@app.route('/solicitação')
def solicitacao(laboratorio,dataReserva,horaInicio,horaFim):
    emailUsuario = session.get('emailLogado')
    if not emailUsuario:
        return redirect(url_for('login'))
    
    tipoUsuario = session.get('tipoLogado') 
    if tipoUsuario == 'aluno':
        #COLOCAR UM ALERT NO HTML  
        #mensagem = 'Solicitação não disponível para alunos.'
        return redirect(url_for('home'))

    sql = 'SELECT ID_USUARIO FROM USUARIOS WHERE EMAIL = emailUsuario'
    idUsuario = execute_sql(sql, {'emailUsuario': emailUsuario})

    sql = '''INSERT INTO RESERVAS (ID_LABORATORIO, ID_USUARIO, DATA_RESERVA, HORA_INICIO, HORA_FIM, STATUS_RESERVA)
             VALUES(:laboratorio, :idUsuario, :dataReserva, :horaInicio, :horaFim, :statusReserva)'''
    execute_sql(sql, {'laboratorio': laboratorio, 'idUsuario': idUsuario, 'dataReserva': dataReserva, 'horaInicio': horaInicio, 'horaFim': horaFim, 'statusReserva': 'em andamento'})

#rota da agenda do usuario
@app.route('/agendaSemanal')
def agenda():
    emailUsuario = session.get('emailLogado')
    if not emailUsuario:
        return redirect(url_for('login'))
    
    tipoUsuario = session.get('tipoLogado') 







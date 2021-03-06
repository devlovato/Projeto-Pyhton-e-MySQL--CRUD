from Database.conexao import conexao
from PyQt5 import uic,QtGui,QtWidgets
from PyQt5.QtWidgets import QMessageBox 
from pyfiglet import figlet_format
from termcolor import colored

texto = figlet_format("PyQt5 e MySQL ",width=200)
texto = colored(texto,"cyan")
print(texto)


def Login(): 

    global Email, Password
    Email = login.lineEdit.text()
    Password = login.lineEdit_2.text()
    
    if Email =="" and Password =="":
       login.label_4.setText("Digite um Email e Senha!")
    else:
        try:    
            cursor = conexao.cursor()
            cursor.execute("SELECT tb_user_pass, tb_user_email,tb_user_permission FROM tb_user WHERE tb_user_email='{}' AND tb_user_pass='{}'".format(Email,Password))
            dados = cursor.fetchall()
            if dados == []:
                login.label_4.setText("E-mail ou senha Incorretos")
            else:
                passwd = dados[0][0]
                mail = dados[0][1]
                nivel_permissao = dados[0][2]
                # print(nivel_permissao)
                if Email == mail and Password == passwd and nivel_permissao == 1:
                    dash.label_2.show()
                    ListarAdm()
                elif Email == mail and Password == passwd:
                    login.lineEdit.text()
                    login.lineEdit.setText("")  
                    login.lineEdit_2.text()
                    login.lineEdit_2.setText("")
                    Listar(Email,Password)
                else:
                    login.label_4.setText("E-mail ou senha Incorretos")

        except ValueError:
            login.label_4.setText("Digite um Email e Senha!", ValueError)
            # print("OCORREU UM ERRO NA VALIDAÇAO DO FORMULARIO",ValueError)
    return conexao

def Cadastro():
    cadastro.show()
    Nome = cadastro.lineEdit_3.text()
    Email = cadastro.lineEdit.text()
    Password = cadastro.lineEdit_2.text()
    sexo = ""
    if cadastro.radioButton.isChecked():
        sexo = "M"
    elif cadastro.radioButton_2.isChecked():
        sexo = "F"
    
    if  Nome=="" or Email =="" or Password =="" or sexo=="":
        cadastro.label_6.setText("PREENCHA TODOS OS CAMPOS!")
    else:
        try:
            cursor = conexao.cursor()
            Insert = f'INSERT INTO tb_user(tb_user.tb_user_nome,tb_user.tb_user_email,tb_user_pass,tb_user_sexo,tb_user_permission) VALUES("{Nome}","{Email}", "{Password}","{sexo}","0")'
            cursor.execute(Insert)
            conexao.commit()
            cadastro.label_6.text()
            cadastro.label_6.setText("CADASTRADO COM SUCESSO!")
            cadastro.lineEdit.setText("")
            cadastro.lineEdit_2.setText("")
            cadastro.lineEdit_3.setText("")
            Chamalog()
        except ValueError:
            cadastro.label_6.setText("OCORREU UM ERRO ",ValueError)
    return conexao

def Listar(Email,Password):

    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT tb_user_id FROM tb_user WHERE tb_user_email="{}" and tb_user_pass="{}"'.format(Email,Password))
        id = cursor.fetchall()
        cursor.execute('SELECT tb_user_nome FROM tb_user WHERE tb_user_email="{}" and tb_user_pass="{}"'.format(Email,Password))
        nome = cursor.fetchall()
        cursor.execute('SELECT tb_user_sexo FROM tb_user WHERE tb_user_email="{}" and tb_user_pass="{}"'.format(Email,Password))
        info = cursor.fetchall()

        # print(info[0][0])
        sexo = ""
        if info[0][0] =='':
            print('sem sexo')

        elif info[0][0]=="M":
           dash.rdb_masc.setChecked(True)
           sexo = "M"

        elif info[0][0]=="F":
           dash.rdb_femi.setChecked(True)
           sexo = "F"

        # print(sexo)
        dash.label_3.hide()
        dash.tableWidget.hide()   
        dash.cad_btn.hide()
        dash.btn_upt_user.show()
        dash.dell_btn.hide()
        dash.resize(400, 480)
        dash.label_4.hide()
        dash.comboBox.hide()
        dash.groupBox.hide()
        dash.pushButton_2.move(280,18)
        dash.label_2.show()
        # HERE 
        dash.label_5.move(100,315)
        dash.rdb_masc.move(100,340)
        dash.rdb_femi.move(190,340)

        dash.label.move(100,70)
        dash.id.move(100,120)
        dash.nome.move(100,170)
        dash.email.move(100,220)
        dash.senha.move(100,270)
        dash.btn_upt_user.move(100,380)
        dash.btn_upt_user.resize(201,41)
        dash.upt_btn.hide()

        login.close()
        dash.show()
        dash.label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Bold))
        dash.label.setText("Bem Vindo, Usuário")

        dash.id.setText(str(id[0][0]))
        dash.nome.setText(nome[0][0])
        dash.email.setText(Email)
        dash.senha.setText(Password)

    except ValueError:
        print("OCORREU UM ERRO ",ValueError)
    return conexao

def Deletar():

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Deseja apagar esse registro?")
        msgBox.setWindowTitle("Message")
        msgBox.setStandardButtons(QMessageBox.Yes  | QMessageBox.No)
        # msgBox.buttonClicked.connect(msgButtonClick)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes :
            linha = dash.tableWidget.currentRow()
            # if dash.tableWidget.rowCount()>0:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT tb_user_id FROM tb_user")
                dados_id = cursor.fetchall()
                if dados_id ==[]:
                    dash.label_2.setStyleSheet ('color: red')
                    dash.label_2.setText("NÃO HÁ REGISTRO !")
                    dash.close()
                else:
                    dados_limpo = dados_id[linha][0]
                    cursor.execute("DELETE FROM tb_user WHERE tb_user_id="+str(dados_limpo))
                    dash.tableWidget.removeRow(linha)
                    conexao.commit()
                    dash.id.setText("")
                    dash.nome.setText("")
                    dash.email.setText("")
                    dash.senha.setText("")
                    dash.label_2.text()
                    dash.label_2.setStyleSheet ('color: Green')
                    dash.label_2.setText("DELETADO!")
            except ValueError:
                print("OCORREU UM ERRO",ValueError)
        return conexao

def ListarAdm():
    dash.label_2.setText("")
    dash.label_3.show()
    dash.comboBox.setCurrentIndex(0) 
    dash.dell_btn.hide()
    dash.pushButton_2.move(830,30)
    dash.resize(945,541)
    dash.upt_btn.resize(161,51)
    dash.upt_btn.move(460,390)

    dash.label_2.setText("")
    dash.label.move(30,30)
    dash.id.move(50,110)
    dash.nome.move(50,160)
    dash.email.move(50,210)
    dash.senha.move(50,260)
    dash.label.setFont(QtGui.QFont("Arial", 28, QtGui.QFont.Bold))
    dash.label_2.move(160,470)
    dash.show()
    login.close()
    dash.tableWidget.show()   
    dash.upt_btn.show()
    dash.cad_btn.show()


    dash.label_5.move(60,310)
    dash.rdb_masc.move(60,340)
    dash.rdb_femi.move(150,340)
    dash.comboBox.show()
    dash.id.setText("")
    dash.nome.setText("")
    dash.email.setText("")
    dash.senha.setText("")
    dash.btn_upt_user.hide()
    try:
        cursor = conexao.cursor()
        dash.label.text()
        dash.label.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        dash.label.setText("Bem Vindo, Administrador")
        
        cursor.execute("SELECT*FROM tb_user")
        dados_lidos = cursor.fetchall()
        dash.tableWidget.setRowCount(len(dados_lidos))
        dash.tableWidget.setColumnCount(6)
        for i in range(0, len(dados_lidos)):
            for j in range(0,6):
                dash.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    except ValueError:
        print('ERRO',ValueError)
    return conexao

def PegaDados():
    try:
        linha = dash.tableWidget.currentRow()
        cursor = conexao.cursor()
        cursor.execute("SELECT tb_user_id FROM tb_user")
        dados_id = cursor.fetchall()
        if dados_id ==[]:
            dash.label_2.setText("NAO HÁ REGISTROS!")
        else:
            id = dados_id[linha][0]
            cursor.execute("SELECT*FROM tb_user WHERE tb_user_id="+str(id))       
            usuario = cursor.fetchall()
    
            global valor_do_id
            valor_do_id = id
    
            dash.id.setText(str(usuario[0][0]))
            dash.nome.setText(str(usuario[0][1]))
            dash.email.setText(str(usuario[0][2]))
            dash.senha.setText(str(usuario[0][3]))
            global sexo
            sexo = ""


            if usuario[0][4]=="M":
                sexo ="M"
                dash.rdb_masc.setChecked(True)
            elif usuario[0][4]=="F":
                sexo = "F"
                dash.rdb_femi.setChecked(True)
            # else:
            #     print('EXO VAZIO')
    
    
            if int(usuario[0][5]) == 0:
                permissao = dash.comboBox.setCurrentText(str(usuario[0][5]))
            else:
                permissao = dash.comboBox.setCurrentText(str(usuario[0][5]))
    
    except ValueError:
        print('OCORREU UM ERRO',ValueError)

def AlteraDados():
    nome =  dash.nome.text()
    email=  dash.email.text()
    senha=  dash.senha.text()
    sexo =""
    if dash.rdb_masc.isChecked():
        sexo = "M"
    elif dash.rdb_femi.isChecked():
        sexo ="F"
    else:
        dash.rdb_masc.setChecked(False)
        dash.rdb_femi.setChecked(False)
    permissao = dash.comboBox.currentText()
    try:
        cursor = conexao.cursor()
        if nome=="" and email =="" and senha=="":
            dash.label_2.setText("PREENCHA OS CAMPOS!")
            dash.label_2.setStyleSheet ('color: red')
        else:
            cursor.execute("UPDATE tb_user SET tb_user_nome = '{}', tb_user_email ='{}',tb_user_pass='{}', tb_user_sexo='{}',tb_user_permission='{}' WHERE tb_user_id = {}".format(nome,email,senha,sexo,permissao,valor_do_id))     
            conexao.commit()
            dash.label_2.setStyleSheet ('color: green')
            dash.label_2.setText("ALTERADO!")
            dash.id.setText("")
            dash.nome.setText("")
            dash.email.setText("")
            dash.senha.setText("")
    except ValueError:
        print('ERRO',ValueError)
    return conexao

def AlteraDadosUsuario():
    id = dash.id.text()
    nome =  dash.nome.text()
    email=  dash.email.text()
    senha=  dash.senha.text()
    dash.label_2.move(150,430)
    sexo = ""
    if dash.rdb_femi.isChecked():
        sexo = "F"
    elif dash.rdb_masc.isChecked():
        sexo = "M"
    try:
        cursor = conexao.cursor()
        if nome=="" and email =="" and senha=="":
            dash.label_2.setText("Os campos vazios!")  
        else:
            cursor.execute("UPDATE tb_user SET tb_user_nome = '{}', tb_user_email ='{}',tb_user_pass='{}',tb_user_sexo ='{}' WHERE tb_user_id = {}".format(nome,email,senha,sexo,id))     
            conexao.commit()
            dash.label_2.setStyleSheet ('color: Green')
            dash.label_2.setText("ALTERADO!")

    except ValueError:
        print('ERRO',ValueError)
    return conexao

def CadastrarDadosUsuario():
    Nome = dash.nome.text()
    Email = dash.email.text()
    Password = dash.senha.text()
    sexo = ""
    permissao = dash.comboBox.currentText()
    if dash.rdb_masc.isChecked():
        sexo = "M"
    elif dash.rdb_femi.isChecked():
        sexo = "F"
    
    if  Nome=="" or Email =="" or Password =="" or sexo=="":
        dash.label_2.setText("PREENCHA TODOS OS CAMPOS!")
    else:
        try:
            cursor = conexao.cursor()
            Insert = f'INSERT INTO tb_user(tb_user.tb_user_nome,tb_user.tb_user_email,tb_user_pass,tb_user_sexo,tb_user_permission) VALUES("{Nome}","{Email}", "{Password}","{sexo}","{permissao}")'
            cursor.execute(Insert)
            conexao.commit()
            dash.label_2.text()
            dash.label_2.setText("CADASTRADO!")
            dash.nome.setText("")
            dash.email.setText("")
            dash.senha.setText("")
        except ValueError:
            cadastro.label_6.setText("OCORREU UM ERRO ",ValueError)
    return conexao  

def ChamaCad():
    login.label_4.setText("")
    cadastro.show()
    login.close()

def Chamalog():
    dash.label_2.show()
    cadastro.label_6.setText("")
    login.show()
    cadastro.close()

def closeDash():
    dash.label_2.setText("")
    dash.label_2.hide()
    login.label_4.setText("")
    login.lineEdit.text()
    login.lineEdit.setText("")  
    login.lineEdit_2.text()
    login.lineEdit_2.setText("")
    dash.close()
    login.show()


app = QtWidgets.QApplication([])
cadastro = uic.loadUi('Projeto-PyQt5---CRUD-/Ui/cadastro.ui')
login = uic.loadUi("Projeto-PyQt5---CRUD-/Ui/login.ui")
dash  = uic.loadUi('Projeto-PyQt5---CRUD-/Ui/dashboard.ui')


dash.tableWidget.doubleClicked.connect(Deletar)
dash.tableWidget.doubleClicked.connect(PegaDados)
dash.btn_upt_user.clicked.connect(AlteraDadosUsuario)
dash.upt_btn.clicked.connect(AlteraDados)
dash.pushButton_2.clicked.connect(closeDash)
dash.cad_btn.clicked.connect(CadastrarDadosUsuario)

cadastro.pushButton.clicked.connect(Cadastro)
cadastro.pushButton_2.clicked.connect(Chamalog)

login.pushButton.clicked.connect(Login)
login.pushButton_2.clicked.connect(ChamaCad)

login.show()
app.exec()












#coding: utf-8

from appJar import gui
import MySQLdb

app = gui("Tela de Login", "400x200")

def usando(btn):
	pass
	#app.infoBox("Mensagem de aviso!", "Você me usou. Vou-lhe usar!")

#def name(btn):
	#cod = app.textBox("Seus dados", "Digite seu nome:", parent=None)
	#print cod

def pesquisar_cidade(btn):
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		cursor.execute("SELECT c.id, c.NomeCidade, e.NomeEstado FROM Cidade c"+
			" INNER JOIN Estado e ON e.id = c.idEstado " +
			" WHERE c.NomeCidade LIKE '%" + termo + "%'")
		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", "{} - {} - {}".format(x[0], x[1], x[2]))

def pesquisar_estado(btn):
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		cursor.execute("SELECT e.id, e.NomeEstado, p.NomePais FROM Estado e"+
			" INNER JOIN Pais p ON e.idPais = p.id " +
			" WHERE e.NomeEstado LIKE '%" + termo + "%'")
		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", "{} - {} - {}".format(x[0], x[1], x[2]))

def pesquisar_pais(btn):
	termo = app.getEntry("txtBusca")
	if termo == '':
		app.errorBox("Erro", 'Informe um termo para pesquisar!')
	else:
		cursor.execute("SELECT id, NomePais FROM Pais WHERE NomePais LIKE '%" + termo + "%'")
		rs = cursor.fetchall()

		app.clearListBox("lBusca")

		for x in rs:
			app.addListItem("lBusca", "{} - {}".format(x[0], x[1]))

def excluir_cidade(btn):
	termo = app.getEntry("txt_cidade")
	cursor.execute("DELETE FROM Cidade WHERE id = '{}'".format(termo))
	conexao.commit()
	app.hideSubWindow('janela_excluir')

def exibir_cidade(btn):
	app.showSubWindow('janela_excluir')


def inserir_cidade(btn):
	cidade = app.getEntry('txtcidade')
	idestado = app.getEntry('txtestado')
	cursor.execute("INSERT INTO Cidade (NomeCidade, idEstado) VALUES ('{}',{})".format(cidade, idestado))
	#cursor.execute("INSERT INTO Cidade (NomeCidade, Estado_idEstado) VALUES('%s',%s)" % (cidade,idestado))
	conexao.commit()
	app.hideSubWindow('janela_inserir')

def exibir_cidade1(btn):
	app.showSubWindow('janela_inserir')

def atualizar_cidade(btn):
	termo = app.getEntry("id-cidade")
	entrada = app.getEntry("id-estado")
	cursor.execute("UPDATE Cidade SET idEstado = {} WHERE id = {}".format(entrada, termo))
	conexao.commit()
	app.hideSubWindow('janela_atualizar')

def exibir_cidade2(btn):
	app.showSubWindow('janela_atualizar')

def login_banco(btn):
	global conexao
	global cursor
	try:
		usuario = app.getEntry("usuario")
		senha = app.getEntry("senha")		
		conexao = MySQLdb.connect("192.168.56.101", usuario, senha, "mundo")
		cursor = conexao.cursor()
		app.showSubWindow('programa_janela')
		return conexao

	except:
		app.errorBox("Erro", 'Usuario e/ou senha incorreto(s)')



app.addEntry('usuario', 0,1)
app.setEntryDefault("usuario", "Digite o Usuario")

app.addEntry('senha', 1,1)
app.setEntryDefault("senha", "Digite a senha")

app.addButton("OK", login_banco, 2,1)

# this is a pop-up
app.startSubWindow("janela_inserir", modal=True)
app.addLabel("l1", "Inserindo dados...")
app.addEntry('txtestado')
app.addEntry('txtcidade')
app.addButton("Salvar cidade", inserir_cidade)
app.setEntryDefault("txtestado", "ID do Estado")
app.setEntryDefault("txtcidade", "Nome da cidade")
app.stopSubWindow()

app.startSubWindow("janela_excluir", modal=True)
app.addLabel("l2", "Excluindo dados...")
app.addEntry('txt_cidade')
app.addButton("Apagar cidade", excluir_cidade)
app.setEntryDefault("txt_cidade", "Id da cidade")
app.stopSubWindow()

app.startSubWindow("janela_atualizar", modal=True)
app.addLabel("l3", "Atualizando dados...")
app.addEntry('id-cidade')
app.addEntry('id-estado')
app.addButton("Atualizar registro", atualizar_cidade)
app.setEntryDefault("id-cidade", "Id da cidade")
app.setEntryDefault("id-estado", "Id do novo estado")
app.stopSubWindow()

app.startSubWindow("programa_janela", modal=True)
app.addLabel("lUser", "Banco Mundo")
app.addButton("Pesquisar cidade", pesquisar_cidade, 1,0)
app.addButton("Pesquisar pais", pesquisar_pais, 1,1)
app.addButton("Pesquisar estado", pesquisar_estado, 1,2)
app.addButton("Excluir cidade", exibir_cidade, 2,0)
app.addButton("Inserir cidade", exibir_cidade1, 2,2)
app.addButton("Atualizar estado", exibir_cidade2, 2,1)
app.addEntry("txtBusca", 3,1)
app.setEntryDefault("txtBusca", "Digite o termo da busca...")
app.addListBox("lBusca", [], 5,1)
app.setListBoxRows("lBusca", 5)
app.stopSubWindow()

app.go()
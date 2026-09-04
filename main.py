# main.py
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QMessageBox, QGroupBox, QFormLayout, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from validacoes import (
    validar_cpf, validar_cnpj, validar_email,
    validar_celular, validar_cep, consulta_cep
)
import database
import re

app = QApplication([])

window = QWidget()
window.setWindowTitle("Cadastro de Pessoa")
window.resize(800, 700)

window.setStyleSheet("""
    QWidget {
        background-color: #222;
        color: white;
    }

    QGroupBox {
        border: 1px solid #555;
        border-radius: 8px;
        margin-top: 12px;
        padding: 15px;
        font-weight: bold;
        font-size: 14px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 6px;
        background-color: #222;
    }

    QLabel {
        font-size: 13px;
    }

    QLineEdit, QComboBox {
        background-color: white;
        color: black;
        border: 1px solid #aaa;
        border-radius: 4px;
        padding: 6px;
        min-height: 18px;
    }

    QPushButton {
        padding: 7px 12px;
        border-radius: 4px;
        font-weight: bold;
    }

    QPushButton:hover {
        border: 1px solid white;
    }
""")

# ============================================================
# TÍTULO
# ============================================================
fonte_titulo = QFont()
fonte_titulo.setBold(True)
fonte_titulo.setPointSize(18)

label_titulo = QLabel("Cadastro de Pessoa")
label_titulo.setAlignment(Qt.AlignCenter)
label_titulo.setFont(fonte_titulo)

# ============================================================
# CAMPOS - PESSOA
# ============================================================
nome = QLineEdit()
nome.setPlaceholderText("Digite o nome completo")

tipo = QComboBox()
tipo.addItems(["CPF", "CNPJ"])

documento = QLineEdit()
documento.setPlaceholderText("Digite o CPF ou CNPJ")

email = QLineEdit()
email.setPlaceholderText("exemplo@email.com")

celular = QLineEdit()
celular.setPlaceholderText("(35) 99999-9999")

# ============================================================
# CAMPOS - ENDEREÇO
# ============================================================
cep = QLineEdit()
cep.setPlaceholderText("Ex: 37500-000")

botao_cep = QPushButton("Consultar CEP")

logradouro = QLineEdit()
logradouro.setPlaceholderText("Rua, avenida, etc.")

numero = QLineEdit()
numero.setPlaceholderText("Ex: 123")

complemento = QLineEdit()
complemento.setPlaceholderText("Apto, bloco, casa...")

bairro = QLineEdit()
bairro.setPlaceholderText("Digite o bairro")

cidade = QLineEdit()
cidade.setPlaceholderText("Digite a cidade")

estado = QComboBox()
estado.addItems([
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
])

# ============================================================
# BLOCO 1 - CADASTRO DA PESSOA
# ============================================================
bloco_pessoa = QGroupBox("Cadastro da Pessoa")
form_pessoa = QFormLayout()
form_pessoa.setSpacing(10)
form_pessoa.setLabelAlignment(Qt.AlignRight)

form_pessoa.addRow("Nome completo:", nome)
form_pessoa.addRow("Tipo de documento:", tipo)
form_pessoa.addRow("CPF/CNPJ:", documento)
form_pessoa.addRow("E-mail:", email)
form_pessoa.addRow("Celular:", celular)

bloco_pessoa.setLayout(form_pessoa)

# ============================================================
# BLOCO 2 - CADASTRO DO ENDEREÇO
# ============================================================
bloco_endereco = QGroupBox("Cadastro do Endereço")
form_endereco = QFormLayout()
form_endereco.setSpacing(10)
form_endereco.setLabelAlignment(Qt.AlignRight)

# Linha especial do CEP: campo + botão
linha_cep = QHBoxLayout()
linha_cep.setSpacing(8)
linha_cep.addWidget(cep)
linha_cep.addWidget(botao_cep)

form_endereco.addRow("CEP:", linha_cep)
form_endereco.addRow("Logradouro:", logradouro)
form_endereco.addRow("Número:", numero)
form_endereco.addRow("Complemento:", complemento)
form_endereco.addRow("Bairro:", bairro)
form_endereco.addRow("Cidade:", cidade)
form_endereco.addRow("Estado:", estado)

bloco_endereco.setLayout(form_endereco)

# ============================================================
# BOTÕES
# ============================================================
botao_limpar = QPushButton("Limpar")
botao_limpar.setStyleSheet(
    "background-color:#990000;color:white;font-weight:bold;"
)

botao_salvar = QPushButton("Salvar Cadastro")
botao_salvar.setStyleSheet(
    "background-color:#004400;color:white;font-weight:bold;"
)

botao_excluir = QPushButton("Excluir Cadastro")
botao_excluir.setStyleSheet(
    "background-color:#990000;color:white;font-weight:bold;"
)

botoes = QHBoxLayout()
botoes.setSpacing(10)
botoes.addWidget(botao_limpar)
botoes.addWidget(botao_salvar)
botoes.addWidget(botao_excluir)

tabela = QTableWidget()
tabela.setColumnCount(5)
tabela.setHorizontalHeaderLabels([ "Nome", "Documento", "E-mail", "Celular", "Cidade" ])
tabela.setEditTriggers(QTableWidget.NoEditTriggers)
tabela.setSelectionBehavior(QTableWidget.SelectRows)
tabela.setSelectionMode(QTableWidget.SingleSelection)
tabela.horizontalHeader().setStretchLastSection(True)

campo_pesquisa = QLineEdit()
campo_pesquisa.setPlaceholderText("Pesquisar por nome...")

botao_pesquisar = QPushButton("Pesquisar")
botao_todos = QPushButton("Mostrar todos")

linha_pesquisa = QHBoxLayout()
linha_pesquisa.addWidget(campo_pesquisa)
linha_pesquisa.addWidget(botao_pesquisar)
linha_pesquisa.addWidget(botao_todos)

def pesquisar():
    texto = campo_pesquisa.text().strip()
    if texto == "":
        atualizar_tabela() 
        return
    pessoas = database.pesquisar_pessoas(texto)
    tabela.setRowCount(len(pessoas))
    
    for linha, pessoa in enumerate(pessoas):
        tabela.setItem(linha, 0, QTableWidgetItem(str(pessoa["id"])))
        tabela.setItem(linha, 1, QTableWidgetItem(pessoa["nome"]))
        tabela.setItem(linha, 2, QTableWidgetItem(pessoa["documento"]))
        tabela.setItem(linha, 3, QTableWidgetItem(pessoa["email"]))
        tabela.setItem(linha, 4, QTableWidgetItem(pessoa["celular"]))
        tabela.setItem(linha, 5, QTableWidgetItem(pessoa["cidade"]))

def excluir():
    linha = tabela.currentRow()

    if linha < 0:
        QMessageBox.warning(
            window,
            "Nenhum cadastro selecionado",
            "Selecione um cadastro na tabela."
        )
        return

    id_pessoa = tabela.item(linha, 0).text()

    resposta = QMessageBox.question(
        window,
        "Confirmar exclusão",
        "Deseja realmente excluir este cadastro?",
        QMessageBox.Yes | QMessageBox.No
    )

    if resposta != QMessageBox.Yes:
        return

    if database.excluir_pessoa(id_pessoa):
        QMessageBox.information(
            window,
            "Sucesso",
            "Cadastro excluído com sucesso."
        )

        atualizar_tabela()

    else:
        QMessageBox.critical(
            window,
            "Erro",
            "Não foi possível excluir o cadastro."
        )

# ============================================================
# LAYOUT PRINCIPAL
# ============================================================
layout = QVBoxLayout()
layout.setSpacing(10)
layout.setContentsMargins(20, 15, 20, 20)

layout.addWidget(label_titulo)
layout.addSpacing(5)
layout.addWidget(bloco_pessoa)
layout.addWidget(bloco_endereco)
layout.addSpacing(5)
layout.addLayout(botoes)
layout.addLayout(linha_pesquisa)
layout.addWidget(tabela)

window.setLayout(layout)

# ============================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================
def re_digits(s: str) -> str:
    return re.sub(r'\D', '', s or "")

def limpar_campos():
    nome.clear()
    documento.clear()
    email.clear()
    celular.clear()
    cep.clear()
    logradouro.clear()
    numero.clear()
    complemento.clear()
    bairro.clear()
    cidade.clear()
    estado.setCurrentIndex(0)
    tipo.setCurrentIndex(0)
    nome.setFocus()

def validar_tudo() -> bool:
    # --------------------------------------------------------
    # Pessoa
    # --------------------------------------------------------
    if nome.text().strip() == "":
        QMessageBox.warning(
            window,
            "Campo obrigatório",
            "O campo 'Nome completo' não foi preenchido."
        )
        nome.setFocus()
        return False

    # Documento
    doc = re_digits(documento.text())

    if doc == "":
        QMessageBox.warning(
            window,
            "Documento obrigatório",
            "Informe um CPF ou CNPJ."
        )
        documento.setFocus()
        return False

    if tipo.currentText() == "CPF":
        if not validar_cpf(doc):
            QMessageBox.warning(
                window,
                "CPF inválido",
                "O CPF informado não é válido."
            )
            documento.setFocus()
            return False
    else:
        if not validar_cnpj(doc):
            QMessageBox.warning(
                window,
                "CNPJ inválido",
                "O CNPJ informado não é válido."
            )
            documento.setFocus()
            return False

    # E-mail
    if not validar_email(email.text().strip()):
        QMessageBox.warning(
            window,
            "E-mail inválido",
            "O e-mail informado não possui um formato válido."
        )
        email.setFocus()
        return False

    # Celular
    if not validar_celular(celular.text().strip()):
        QMessageBox.warning(
            window,
            "Celular inválido",
            "O celular deve possuir 11 números."
        )
        celular.setFocus()
        return False

    # --------------------------------------------------------
    # Endereço
    # --------------------------------------------------------
    if not validar_cep(cep.text().strip()):
        QMessageBox.warning(
            window,
            "CEP inválido",
            "O CEP deve possuir 8 números."
        )
        cep.setFocus()
        return False

    if logradouro.text().strip() == "":
        QMessageBox.warning(
            window,
            "Logradouro obrigatório",
            "Informe o logradouro."
        )
        logradouro.setFocus()
        return False

    if numero.text().strip() == "":
        QMessageBox.warning(
            window,
            "Número obrigatório",
            "Informe o número do endereço."
        )
        numero.setFocus()
        return False

    if bairro.text().strip() == "":
        QMessageBox.warning(
            window,
            "Bairro obrigatório",
            "Informe o bairro."
        )
        bairro.setFocus()
        return False

    if cidade.text().strip() == "":
        QMessageBox.warning(
            window,
            "Cidade obrigatória",
            "Informe a cidade."
        )
        cidade.setFocus()
        return False

    return True

# ============================================================
# CONSULTA DE CEP
# ============================================================
def on_consultar_cep():
    cep_val = cep.text().strip()

    if not validar_cep(cep_val):
        QMessageBox.warning(
            window,
            "CEP inválido",
            "Informe um CEP com 8 dígitos."
        )
        cep.setFocus()
        return

    resultado = consulta_cep(cep_val)

    if resultado is None:
        QMessageBox.information(
            window,
            "CEP não encontrado / erro",
            "Não foi possível obter o endereço para o CEP informado. "
            "Verifique a conexão ou o CEP."
        )
        return

    # Preenche automaticamente os campos retornados pelo ViaCEP
    logradouro.setText(resultado.get("logradouro", ""))
    bairro.setText(resultado.get("bairro", ""))
    cidade.setText(resultado.get("cidade", ""))

    uf = resultado.get("estado", "")
    idx = estado.findText(uf)

    if idx != -1:
        estado.setCurrentIndex(idx)

    # O usuário continua podendo alterar os dados preenchidos.
    numero.setFocus()

# ============================================================
# SALVAR
# ============================================================
def on_salvar():
    if not validar_tudo():
        return

    dados = {
        "nome": nome.text().strip(),
        "tipo": tipo.currentText(),
        "documento": re_digits(documento.text()),
        "email": email.text().strip(),
        "celular": re_digits(celular.text()),
        "cep": re_digits(cep.text()),
        "logradouro": logradouro.text().strip(),
        "numero": numero.text().strip(),
        "complemento": complemento.text().strip(),
        "bairro": bairro.text().strip(),
        "cidade": cidade.text().strip(),
        "estado": estado.currentText()
    }

    ok = database.salvar_pessoa(dados)

    if ok:
        QMessageBox.information(
            window,
            "Sucesso",
            "Cadastro salvo com sucesso."
        )
        limpar_campos()
        atualizar_tabela()
    else:
        QMessageBox.critical(
            window,
            "Erro",
            "Ocorreu um erro ao salvar o cadastro."
        )

# ============================================================
# LIMPAR
# ============================================================
def on_limpar():
    limpar_campos()

def atualizar_tabela():
    pessoas = database.listar_pessoas()

    tabela.setRowCount(len(pessoas))

    for linha, pessoa in enumerate(pessoas):
        tabela.setItem(linha, 0, QTableWidgetItem(pessoa["nome"]))
        tabela.setItem(linha, 1, QTableWidgetItem(pessoa["documento"]))
        tabela.setItem(linha, 2, QTableWidgetItem(pessoa["email"]))
        tabela.setItem(linha, 3, QTableWidgetItem(pessoa["celular"]))
        tabela.setItem(linha, 4, QTableWidgetItem(pessoa["cidade"]) )

# ============================================================
# CONECTAR SINAIS
# ============================================================
botao_cep.clicked.connect(on_consultar_cep)
botao_salvar.clicked.connect(on_salvar)
botao_limpar.clicked.connect(on_limpar)
botao_pesquisar.clicked.connect(pesquisar)
botao_todos.clicked.connect(atualizar_tabela)
botao_excluir.clicked.connect(excluir)

# ============================================================
# INICIALIZAR BANCO E MOSTRAR JANELA
# ============================================================
database.criar_tabela()
atualizar_tabela()
window.show()
app.exec()
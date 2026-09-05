# validacoes.py
import re
import requests

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def calc(digs):
        s = sum(int(a) * b for a, b in zip(digs, range(len(digs)+1, 1, -1)))
        r = 11 - (s % 11)
        return '0' if r >= 10 else str(r)
    v1 = calc(cpf[:9])
    v2 = calc(cpf[:9] + v1)
    return cpf[-2:] == v1 + v2

def validar_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    def calc(digs, pesos):
        s = sum(int(d)*p for d,p in zip(digs, pesos))
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos2 = [6] + pesos1
    v1 = calc(cnpj[:12], pesos1)
    v2 = calc(cnpj[:12] + v1, pesos2)
    return cnpj[-2:] == v1 + v2

def validar_email(email: str) -> bool:
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validar_celular(cel: str) -> bool:
    cel_limpo = re.sub(r'\D', '', cel)
    return len(cel_limpo) == 11

def validar_cep(cep: str) -> bool:
    cep_limpo = re.sub(r'\D', '', cep)
    return len(cep_limpo) == 8

def consulta_cep(cep: str, timeout: float = 5.0) -> dict | None:
    """
    Consulta ViaCEP e retorna dicionário com logradouro, bairro, localidade, uf.
    Retorna None em caso de erro de conexão ou CEP não encontrado.
    """
    cep_limpo = re.sub(r'\D', '', cep)
    if len(cep_limpo) != 8:
        return None
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        resp = requests.get(url, timeout=timeout)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if data.get("erro"):
            return None
        return {
            "logradouro": data.get("logradouro", ""),
            "bairro": data.get("bairro", ""),
            "cidade": data.get("localidade", ""),
            "estado": data.get("uf", "")
        }
    except requests.RequestException:
        return None
def validar_nome(nome):
    nome = nome.strip()


    partes = nome.split()

    if len(partes) < 2:
        return False


    if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ ]+", nome):
        return False

    return True

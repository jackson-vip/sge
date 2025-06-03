import re

# Validar CPF
def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf)) # Apenas números
    if not cpf:
        return False
    cpf = re.sub(r'[^0-9]', '', cpf) # Apenas números
    if len(cpf) != 11:
        return False
    # CPFs com todos os dígitos iguais são inválidos
    if cpf in (c * 11 for c in '1234567890'):
        return False
    calc = lambda t: int(t[1]) * (t[0] + 2)
    d1 = ((sum(map(calc, enumerate(reversed(cpf[:-2])))) * 10) % 11) % 10
    d2 = ((sum(map(calc, enumerate(reversed(cpf[:-1])))) * 10) % 11) % 10
    return str(d1) == cpf[-2] and str(d2) == cpf[-1]

# Validar CNPJ
def validate_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj)) # Apenas números
    if not cnpj:
        return False
    cnpj = re.sub(r'[^0-9]', '', cnpj) # Apenas números
    if len(cnpj) != 14:
        return False
    calc = lambda t: int(t[1]) * t[0]
    d1 = (sum(map(calc, enumerate(reversed(cnpj[:-2])), 2) * 10) % 11) % 10
    d2 = (sum(map(calc, enumerate(reversed(cnpj[:-1])), 2) * 10) % 11) % 10
    return str(d1) == cnpj[-2] and str(d2) == cnpj[-1]

# Validar CPF ou CNPJ
def validate_cpf_cnpj(value):
    if not value:
        return False
    if len(value) == 11:
        return validate_cpf(value)
    elif len(value) == 14:
        return validate_cnpj(value)
    return False

# Validar telefone
def validate_phone(phone):
    # phone = ''.join(filter(str.isdigit, phone)) # Apenas números
    if not phone:
        return False
    phone = re.sub(r'[^0-9]', '', phone) # Apenas números
    if len(phone) < 10 or len(phone) > 11:
        return False
    return True

# Validar CEP
def validate_cep(cep):
    if not cep:
        return False
    cep = re.sub(r'[^0-9]', '', cep) # Apenas números 
    if len(cep) != 8:
        return False
    return True

# Validar e-mail
def validate_email(email):
    if not email:
        return False
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

# Validar sigla de UF acitar apenas as siglas de Unidades Federativas do Brasil
def validate_sigla(sigla):
    if not sigla:
        return False
    siglas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    return sigla.upper() in siglas

def validate_rg(rg):
    if not rg or not rg.strip():
        return True  # Campo não obrigatório, vazio é válido
    rg = re.sub(r'[^0-9]', '', rg)  # Apenas números
    if len(rg) < 7 or len(rg) > 12:  # Comprimento típico do RG no Brasil
        return False
    return True
from datetime import datetime

# Função para formatação monetária
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(",", "temp").replace(".", ",").replace("temp", ".")

# Funções de operações bancárias
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: {formatar_valor(valor)}")
        return saldo, extrato
    print("Erro: Valor deve ser positivo!")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saques = numero_saques >= limite_saques
    excedeu_limite = valor > limite

    if excedeu_saques:
        print("Erro: Limite diário de saques atingido.")
    elif excedeu_limite:
        print(f"Erro: Valor máximo por saque: {formatar_valor(limite)}")
    elif valor > saldo:
        print("Erro: Saldo insuficiente.")
    elif valor <= 0:
        print("Erro: Valor inválido.")
    else:
        saldo -= valor
        extrato.append(f"Saque: {formatar_valor(valor)}")
        numero_saques += 1
        print("Saque realizado!")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n======== EXTRATO ========")
    print("Nenhuma movimentação." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: {formatar_valor(saldo)}")
    print("========================")

# Funções para gestão de clientes e contas
def criar_usuario(usuarios):
    cpf = input("CPF (apenas números): ").strip()
    
    if any(u['cpf'] == cpf for u in usuarios):
        print("Erro: CPF já cadastrado!")
        return
    
    nome = input("Nome completo: ").strip()
    data_nasc = input("Data nasc. (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ").strip()
    
    usuarios.append({
        'cpf': cpf,
        'nome': nome,
        'data_nascimento': data_nasc,
        'endereco': endereco
    })
    print("Usuário cadastrado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("CPF do titular: ").strip()
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    
    if not usuario:
        print("Erro: Usuário não encontrado!")
        return None
    
    return {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'usuario': usuario
    }

def listar_contas(contas):
    print("\n======== CONTAS ========")
    if not contas:
        print("Nenhuma conta cadastrada")
        return
    
    for conta in contas:
        titular = conta['usuario']
        print(
            f"Agência: {conta['agencia']}\n"
            f"C/C: {conta['numero_conta']:04d}\n"
            f"Titular: {titular['nome']}\n"
            f"CPF: {titular['cpf']}\n"
            "------------------------"
        )
    print("========================")

# Configurações iniciais
saldo = 0.0
extrato = []
numero_saques = 0
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500.0
usuarios = []
contas = []
AGENCIA = "0001"

# Sistema de menu
menu = """
======== SISTEMA BANCÁRIO ========
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo usuário
[c] Nova conta
[l] Listar contas
[q] Sair
==================================
"""

# Loop principal
while True:
    print(menu)
    opcao = input("Operação: ").strip().lower()
    
    if opcao == 'd':
        try:
            valor = float(input("Valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        except ValueError:
            print("Erro: Valor inválido!")
    
    elif opcao == 's':
        try:
            valor = float(input("Valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=LIMITE_VALOR_SAQUE,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )
        except ValueError:
            print("Erro: Valor inválido!")
    
    elif opcao == 'e':
        exibir_extrato(saldo, extrato=extrato)
    
    elif opcao == 'u':
        criar_usuario(usuarios)
    
    elif opcao == 'c':
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)
            print(f"Conta {numero_conta} criada!")
    
    elif opcao == 'l':
        listar_contas(contas)
    
    elif opcao == 'q':
        print("Encerrando sistema...")
        break
    
    else:
        print("Operação inválida!")
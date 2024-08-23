"""
Programa feito no curso da DIO "NTT DATA - Engenharia de Dados com Python"
(https://web.dio.me/track/engenharia-dados-python)

Este programa simula um sistema bancário simples de apenas um usuário e sem
persistencia das operações que permite ao usuário realizar operações básicas
como depósitos, saques, e visualização de extratos. O saldo e o extrato são
mantidos apensa enquanto o programa executa e atualizados conforme as operações
são realizadas.

Funções principais:

- exibir_extrato(extrato, saldo): Exibe o extrato das transações realizadas e o saldo atual.
- realizar_deposito(saldo, extrato): Permite ao usuário realizar um depósito, atualizando o saldo
e registrando a transação.
- realizar_saque(saldo, extrato, limite, numero_saques, limite_saques): Permite ao usuário realizar
um saque, respeitando o saldo disponível, limite diário, e o número máximo de saques permitidos.
- main(): Função principal que controla o fluxo do programa, apresentando o MENU e chamando as
funções apropriadas com base na escolha do usuário.

Variáveis:

- saldo: Armazena o saldo atual da conta do usuário.
- limite: Define o limite máximo para saques.
- extrato: Lista que armazena o histórico de transações (depósitos e saques).
- numero_saques: Contador que registra quantos saques foram realizados no dia.
- limite_saques: Limite diário de saques permitidos.

Como usar:

1. Execute o programa.
2. Selecione uma opção do MENU ([d] Depositar, [s] Sacar, [e] Extrato, [q] Sair).
3. Siga as instruções para realizar a operação escolhida.
4. O programa continuará a executar até que a opção `q` (Sair) seja selecionada.
"""

import datetime
import textwrap

from prettytable import PrettyTable


def menu():
    """
    Apresenta o menu principal do sistema bancário, permitindo ao usuário
        escolher entre as opções disponíveis:
    * Depositar
    * Sacar
    * Extrato
    * Nova conta
    * Listar contas
    * Novo usuário
    * Sair

    Retorna:
        str: A opção escolhida pelo usuário.
    """
    MENU = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(MENU))


def obter_valor_positivo(mensagem: str) -> float:
    """
    Solicita ao usuário que insira um valor numérico positivo e retorna esse valor.

    A função exibe uma mensagem de solicitação ao usuário e tenta converter a
    entrada para um número de ponto flutuante. 
    Se o usuário inserir um valor que não seja um número válido ou se o número
    for menor ou igual a zero, a função 
    continuará solicitando a entrada até que um valor positivo seja inserido.

    Parâmetros:
    mensagem (str): A mensagem a ser exibida ao usuário para solicitar a entrada.

    Retorna:
    float: O valor numérico positivo inserido pelo usuário.
    """
    while True:
        try:
            valor = float(input(mensagem))
            if valor > 0:
                return valor
            print("O valor deve ser positivo e maior que zero.")
        except ValueError:
            print("Entrada inválida! Por favor, insira um número válido.")


def exibir_extrato(extrato: list[str], saldo: float) -> None:
    """
    Exibe o extrato das transações realizadas e o saldo atual.

    Parâmetros:
    - extrato (list): Lista de strings que contém o histórico das transações (depósitos e saques).
    - saldo (float): O saldo atual da conta do usuário.

    Retorna:
    - None: A função apenas imprime o extrato e o saldo na tela.
    """
    # print("\n================ EXTRATO ================")
    # print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
    # print(f"\nSaldo: R$ {saldo:.2f}")
    # print("==========================================")
    tabela = PrettyTable(["Data", "Descrição", "Valor"])
    for transacao in extrato:
        data = transacao['data'].strftime('%d/%m/%Y')
        descricao = transacao['descricao']
        valor = f"R$ {transacao['valor']:.2f}"
        tabela.add_row([data, descricao, valor])
    tabela.add_row([datetime.datetime.now().strftime('%d/%m/%Y'), "Saldo", f"R$ {saldo:.2f}"])
    print(tabela)


def realizar_deposito(saldo: float, extrato: list[str]) -> tuple[float, list[str]]:
    """
    Realiza um depósito na conta do usuário, atualizando o saldo e registrando a transação.

    Parâmetros:
    - saldo (float): O saldo atual da conta do usuário.
    - extrato (list[str]): Lista de strings que contém o histórico das transações.

    Retorna:
    - tuple[float, list[str]]: Uma tupla contendo o saldo atualizado e a lista
        de extrato atualizada.
    """
    valor = obter_valor_positivo("Informe o valor do depósito: ")
    if valor > 0:
        saldo += valor
        extrato.append({'data': datetime.datetime.now(),
                       'descricao': 'Depósito', 'valor': valor})
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def realizar_saque(
    saldo: float, extrato: list[str], limite: float, numero_saques: int, limite_saques: int
) -> tuple[float, list[str], int]:
    """
    Realiza um saque da conta do usuário, respeitando o saldo disponível, o
        limite diário, e o número máximo de saques permitidos.

    Parâmetros:
    - saldo (float): O saldo atual da conta do usuário.
    - extrato (list[str]): Lista de strings que contém o histórico das transações.
    - limite (float): O valor máximo permitido para um saque.
    - numero_saques (int): O número atual de saques realizados.
    - limite_saques (int): O número máximo de saques permitidos por dia.

    Retorna:
    - tuple[float, list[str], int]: Uma tupla contendo o saldo atualizado, a
        lista de extrato atualizada, e o número de saques atualizados.
    """
    valor = obter_valor_positivo("Informe o valor do saque: ")
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append({'data': datetime.datetime.now(),
                       'descricao': 'Saque', 'valor': valor})
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def validar_cpf(cpf: str) -> bool:
    """Valida um número de CPF utilizando o algoritmo de validação padrão.

    Parâmetros:
        cpf (str): O número de CPF a ser validado.

    Retorna:
        bool: True se o CPF for válido, False caso contrário.
    """

    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        digito1 = 0
    else:
        digito1 = resto

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = 11 - (soma % 11)
    if resto == 10 or resto == 11:
        digito2 = 0
    else:
        digito2 = resto

    # Verifica se os dígitos verificadores calculados correspondem aos dígitos do CPF
    if digito1 != int(cpf[9]) or digito2 != int(cpf[10]):
        return False

    return True


def criar_usuario(usuarios: list) -> None:
    """
    Cria um novo usuário no sistema. Solicita as informações do usuário, valida
        o CPF e adiciona o usuário à lista de usuários.

    Parâmetros:
        usuarios (list): Lista de dicionários, onde cada dicionário representa um usuário.

    Retorna:
        None
    """
    cpf = input("Informe o CPF (somente números): ")
    while not validar_cpf(cpf):
        print("CPF inválido. Por favor, informe um CPF válido.")
        cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    try:
        data_nascimento = datetime.datetime.strptime(
            data_nascimento, "%d-%m-%Y")
    except ValueError:
        print("Data de nascimento inválida. Use o formato dd-mm-aaaa.")
        return
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                    "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf: str, usuarios: list) -> dict:
    """
    Filtra a lista de usuários buscando um usuário com o CPF informado.

    Parâmetros:
        cpf (str): O CPF do usuário a ser buscado.
        usuarios (list): Lista de dicionários, onde cada dicionário representa um usuário.

    Retorna:
        dict: O dicionário do usuário encontrado, caso exista. Caso contrário, retorna None.
    """
    usuarios_filtrados = [
        usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia: str, numero_conta: int, usuarios: list) -> dict:
    """
    Cria uma nova conta bancária para um usuário existente.

    Parâmetros:
        agencia (str): O número da agência.
        numero_conta (int): O número da conta.
        usuarios (list): Lista de dicionários, onde cada dicionário representa
            um usuário.

    Retorna:
        dict: Um dicionário representando a nova conta, caso o usuário seja
            encontrado. Caso contrário, retorna None.
    """
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas: list) -> None:
    """
    Lista todas as contas cadastradas no sistema, exibindo a agência, número da
        conta e o nome do titular.

    Parâmetros:
        contas (list): Lista de dicionários, onde cada dicionário representa uma conta.

    Retorna:
        None
    """
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main() -> None:
    """
    Função principal que controla o fluxo do programa, apresentando o menu e
        chamando as funções apropriadas com base na escolha do usuário.

    Parâmetros:
    - Nenhum

    Retorna:
    - None: A função não retorna nenhum valor, apenas controla o fluxo do programa.
    """
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    limite_saques = 3
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            saldo, extrato = realizar_deposito(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = realizar_saque(
                saldo, extrato, limite, numero_saques, limite_saques)
        elif opcao == "e":
            exibir_extrato(extrato, saldo)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()

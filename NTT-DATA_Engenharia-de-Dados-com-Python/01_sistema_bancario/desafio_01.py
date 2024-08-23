"""
Programa feito no curso da DIO "NTT DATA - Engenharia de Dados com Python"
(https://web.dio.me/track/engenharia-dados-python)

Este programa simula um sistema bancário simples de apenas um usuário e sem persistencia das operações
que permite ao usuário realizar operações básicas como depósitos, saques, e visualização de extratos. O saldo e
o extrato são mantidos apensa enquanto o programa executa e atualizados conforme as operações são realizadas.

Funções principais:

- exibir_extrato(extrato, saldo): Exibe o extrato das transações realizadas e o saldo atual.
- realizar_deposito(saldo, extrato): Permite ao usuário realizar um depósito, atualizando o saldo e registrando a transação.
- realizar_saque(saldo, extrato, limite, numero_saques, limite_saques): Permite ao usuário realizar um saque, respeitando o saldo disponível, limite diário, e o número máximo de saques permitidos.
- main(): Função principal que controla o fluxo do programa, apresentando o MENU e chamando as funções apropriadas com base na escolha do usuário.

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


MENU = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


def obter_valor_positivo(mensagem: str) -> float:
    """
    Solicita ao usuário que insira um valor numérico positivo e retorna esse valor.

    A função exibe uma mensagem de solicitação ao usuário e tenta converter a entrada para um número de ponto flutuante. 
    Se o usuário inserir um valor que não seja um número válido ou se o número for menor ou igual a zero, a função 
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
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else "\n".join(extrato))
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def realizar_deposito(saldo: float, extrato: list[str]) -> tuple[float, list[str]]:
    """
    Realiza um depósito na conta do usuário, atualizando o saldo e registrando a transação.

    Parâmetros:
    - saldo (float): O saldo atual da conta do usuário.
    - extrato (list[str]): Lista de strings que contém o histórico das transações.

    Retorna:
    - tuple[float, list[str]]: Uma tupla contendo o saldo atualizado e a lista de extrato atualizada.
    """
    valor = obter_valor_positivo("Informe o valor do depósito: ")
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def realizar_saque(
    saldo: float, extrato: list[str], limite: float, numero_saques: int, limite_saques: int
) -> tuple[float, list[str], int]:
    """
    Realiza um saque da conta do usuário, respeitando o saldo disponível, o limite diário, e o número máximo de saques permitidos.

    Parâmetros:
    - saldo (float): O saldo atual da conta do usuário.
    - extrato (list[str]): Lista de strings que contém o histórico das transações.
    - limite (float): O valor máximo permitido para um saque.
    - numero_saques (int): O número atual de saques realizados.
    - limite_saques (int): O número máximo de saques permitidos por dia.

    Retorna:
    - tuple[float, list[str], int]: Uma tupla contendo o saldo atualizado, a lista de extrato atualizada, e o número de saques atualizados.
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
        extrato.append(f"Saque: R$ {valor:.2f}")
        numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques


def main() -> None:
    """
    Função principal que controla o fluxo do programa, apresentando o menu e chamando as funções apropriadas com base na escolha do usuário.

    Parâmetros:
    - Nenhum

    Retorna:
    - None: A função não retorna nenhum valor, apenas controla o fluxo do programa.
    """
    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    limite_saques = 3

    while True:
        opcao = input(MENU)

        if opcao == "d":
            saldo, extrato = realizar_deposito(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = realizar_saque(
                saldo, extrato, limite, numero_saques, limite_saques)
        elif opcao == "e":
            exibir_extrato(extrato, saldo)
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()

# ⚒️Desenvolvimento: Sistema Bancário

**Objetivo:** O sistema simula o menu de um caixa eletrônico bancário, permitindo que o usuário realize as seguintes operações:

- **Depósito:** Permite depositar valores na conta.
- **Saque:** Permite sacar dinheiro da conta, com algumas restrições:
  - Valor do saque não pode ser superior ao saldo disponível.
  - Valor máximo por saque é de R$ 500,00.
  - Quantidade máxima de saques por dia é 3.
- **Extrato:** Mostra o histórico de movimentações da conta, incluindo depósitos, saques e transferências.
- **Transferência:** Permite transferir valores para outras contas.
- **Sair:** Encerra o programa.

### Funcionamento:
- O programa apresenta um menu com as opções disponíveis.
- O usuário digita o número da opção desejada.
- O programa valida a opção e executa a operação correspondente.
- O programa informa o resultado da operação e retorna ao menu principal.

### Mensagens de Erro:

- **Saldo Insuficiente:** Aparece quando o valor do saque ou da transferência é superior ao saldo disponível na conta.
- **Valor Inválido:** Aparece quando o valor digitado for negativo ou não for um número.
- **Opção Inválida:** Aparece quando o usuário digitar um número que não corresponde a nenhuma opção do menu.

### Exemplo de Uso:

Todas as transações testadas estão no arquivo exemplo_de_uso.txt na pasta inputs

*Resultado final*

================ EXTRATO BANCÁRIO ================

Depósito: R$ 5000.00

Saque: R$ 150.00

Saque: R$ 350.00

Transferência para conta 1234: R$ 850.00

Depósito: R$ 650.00

Saque: R$ 499.00

Transferência para conta 1235: R$ 963.00


Saldo: R$ 2838.00

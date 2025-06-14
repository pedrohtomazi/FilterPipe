# 📘 Resumo Final – Aula Xiscatti


## 🧠 Portas Lógicas


### 📌 Resumo_02 - ✅ Útil técnico

**Resumo:**

Aula sobre operações lógicas XOR e XNOR com uma entrada negada e sua aplicação em um circuito eletrônico.

- A saída de um XOR é negada quando todas as entradas são iguais, mas ao utilizar um XNOR, se uma das entradas for negada, o resultado seria diferente.
- Quando uma entrada possui um trêsseis em cima, significa que a variável atual está sendo negada. Se houver dois trêsseis em cima, isso indica que ambas as entradas estão negadas e a saída seria invertida.
- É possível ter duas entradas negadas em um XNOR.
- Aplicação prática: exemplo de um carrinho controlado por Arduino seguindo uma linha preta, onde o carrinho tem 100 sujes e precisa se movimentar ao longo da linha seguindo uma sinalização. Além disso, foram mencionados sumôbots (robôs) que utilizam serra laser em batalhas entre si e brincadeiras com robôs controlados remotos na internet.
- Ao longo do curso, o aluno deve aprender sobre a encadeamento de componentes eletrônicos e o processo de projeto de circuito para uma compreensão mais profunda da funcionamento das saídas baseadas em sensores. O foco será retornar ao assunto de portas lógicas.
- A primeira tabelinha apresentada ilustra o funcionamento do XNOR com entrada IBC sem negação de variáveis, onde a saída depende da premissa que duas variáveis iguais dão na saída.

——————————————————————————————————————————————————


### 📌 Resumo_03 - ✅ Útil técnico

Resumo da Aula:

Objetivo: Apresentar o funcionamento da porta lógica XNOR (porta de coincidência) e como seria possível realizar circuito equivalente com outras entradas.

1. Descrição da Porta XNOR:
   - A porta XNOR compara duas entradas e produz saídas 0 (verdadeiro) caso as entradas sejam iguais ou diferentes (o complemento lógico um).
   - Se a entrada padrão é false, não importa o valor das outras entradas.
   - A tabela de verdade para a porta XNOR é:
     | Entrada A | Entrada B | Saída XNOR |
     |-----------|-----------|------------|
     | 0         | 0         | 1          |
     | 0         | 1         | 1          |
     | 1         | 0         | 1          |
     | 1         | 1         | 0          |

2. Porta XNOR vs. Porta de Coincidência:
   - Ambas as portas são usadas para detectar coincidências ou incoerências em duas entradas.
   - No entanto, a porta de coincidência é mais comumente utilizada e também conhecida como porta XNOR.

3. Circuito equivalente:
   - Apresentou um exemplo de circuito equivalente para uma entrada XNOR usando as entradas A e B negadas (A' e B') seguidas por uma operação AND e um NOT na saída.
   - A entrada verdadeira para a porta XNOR seria obtida através da inversão de A e B, seguido da operação AND e em seguida inversão de novo (not).

4. Rectas Equivalentes:
   - Foi introduzido o conceito de rectas equivalentes como um método para simplificar circuitos complexos, que mostra que certos circuitos podem ser substituídos por outros sem alterar seu funcionamento geral.
   - Foi sugerido que a combinação A e B negados poderia ser visto como uma recta equivalente para a porta XNOR.

——————————————————————————————————————————————————


## 🧠 Sensores e Sinalização


### 📌 Resumo_05 - ✅ Útil técnico

Titulo: Operações de sensores em um sistema automatizado de estacionamento

   Resumo: Neste tópico, foi abordado como ativar e controlar os sensores de um sistema automatizado de estacionamento. Ocorre que a potência A é ligada quando os sensores estão funcionando em 0 (barco 100% ou overclock), e a potência 0 é utilizada quando os sensores estão em 50 graus.

   Os seguintes passos são necessários para ativar as luzes conforme o status dos sensores:
      - Se o sensor A está ativado e o sensor B não está, ligar a luz vermelha
      - Se o sensor B está ativado e o sensor A não está, ligar a luz azul
      - Se os sensores estão ativos, ligar a luz vermelha
      - Caso ambos os sensores estejam ativos, a luz verde será acionada

   Para identificar a operação que se deseja realizar, é necessário considerar o status dos dois sensores. Por exemplo:
      - Se o sensor A e o sensor B estiverem ativados, a operação de um sensor A será a primeira executada, seguida da operação de um sensor B

   Considerações adicionais:
      - Se o estacionamento for cheio, a cancela de entrada não precisa ser ligada
      - Se o estacionamento não estiver totalmente cheio, a cancela de entrada precisará ser habilitada
      - Se um cabo estiver dentro da cancela, ela ficará desabilitada
      - Para uma operação automatizada, é necessário considerar mais questões
      - Não se pode desabilitar a cancela de entrada e sair; caso contrário, o carro continuará a entrar
      - Os sensores de entrada e saída também estão disponíveis

   Além disso, foi apresentado um exemplo da primeira entrada no sistema automatizado de estacionamento.

——————————————————————————————————————————————————


### 📌 Resumo_06 - ✅ Útil técnico

Resumo estruturado da aula:

Título: Uso de sensores em um sistema de portões elétricos

Resumo:
- Pode usar os sensores se A e B estiverem em zero.
- A e B devem estar em um para ligar a plaquinha, mas podemos imaginar outras maneiras de fazer isso.
- Quando a saída está habilitada, ela é um (1). Quando está desabilitada, ela é zero (0).
- Se a entrada estiver desabilitada, significa que o estacionamento está cheio.
- A cancela da entrada é habilitada quando a saída está desabilitada.
- A tabelinha usa dois sensores de posição do carro e pode ser construída no Lógica de Luz, tornando-se mais visualizável.
- Nenhuma prova vai ter a, b, entrada, saída, retorno. A tabelinha lógica léve apenas A e B.
- Deverá ser construído no Lógica de Luz e observado para entender o que está acontecendo.

Conclusão:
- O uso dos sensores em um sistema de portões elétricos é fundamental para a funcionalidade do sistema.
- A compreensão da lógica do sistema pode ser facilitada construindo tabelas e observando suas reações no Lógica de Luz.

——————————————————————————————————————————————————


### 📌 Resumo_07 - ✅ Útil técnico

Aula de Sinalização em Circuito Integrado

   Neste exemplo, estamos analisando um circuito que utiliza os sinais: Verde (G), Amarelo (Y) e Vermelho (R).

   - Inicie pelo verde 1 e vermelho 2.
   - Um no sinal negativo estará com o verde, enquanto outro estaria com o vermelho.
   - Em seguida, mude do verde para amarelo.
   - Enquanto isso, o vermelho continua ligado.
   - A mudança acontece entre amarelo e vermelho, se passando do primeiro para o segundo.
   - Caso esteja dentro de um botão, não entrar no caso. Estamos pensando na sequência do ciclo das luzes.
   - Será utilizado um servidor temporizador. Os sinais permanecerão ligados por um determinado tempo.
   - O ciclo verde e o vermelho demora mais do que o amarelo, pois este último serve para indicar que vai fechar.
   - Em Curitiba, o amarelo significa a mesma coisa que acelera. É importante sempre considerar as coisas que pioram a situação, como dirigir sob influência de aparelhos móveis.

——————————————————————————————————————————————————


### 📌 Resumo_10 - ✅ Útil técnico

Transcrição reorganizada e resumida:

O tema discutido foi o circuito de sinais usando como exemplo um sinalizador de trÁnsito. A partir de 2008, o custo da hora vendida do carro usado Wanda Fit (que possui um Honda Accord com 95 milhas) é irrelevante para a discussão.

Neste circuito, há duas sequências de assinareiros: o primeiro ciclo com os sinais vermelho e verde e o segundo ciclo com os sinais amarelo e vermelho. A sequência do assinareiro 2 é simultaneamente ligada com o 1 para mostrar quem está no primeiro ciclo e depois quem está no segundo ciclo.

A partir de uma programação em um arduino, este circuito pode ser controlado e alterado, permitindo que o tempo seja temporizado. As equações matemáticas para calcular a saída são complexas e podem gerar dúvidas. No entanto, as tabelas criadas facilitam a comprensão do funcionamento do circuito de sinais.

A sequência 2x0, 2x1, 2x2, 2x4, etc é muito importante no contexto de circuitos lógicos. A discussão sobre portas lógicas foi encerrada neste momento.

——————————————————————————————————————————————————


## 🧠 Hardware e Prova


### 📌 Resumo_13 - ✅ Útil técnico

Aula sobre Processamento Digital:

1. Pontuação: 1 menos 0 (se for necessário imprimir um ponto, é preciso imprestar um ponto negativo)
2. Uma vez que você tenha impresso 1, você terá 1 menos 1. Neste caso, não será necessário mais imprimir pontos.
3. A prova consistirá em três partes: parte binária, parte relacionada com portas lógicas e mais a parte de números romanos.
4. Por isso, você terá que estudar os seguintes tópicos: processador, memória, descorrida, interface, periférico, fonte, cabinet, monitor e builds.
5. Você precisa saber o funcionamento do joguinho (processador), mas não é necessário que você saiba como construí-lo.
6. O processador executa a fonte de energia, enquanto que a memória armazena dados e realiza o banalamento. A interface permite a comunicação entre o usuário e o computador.
7. Nesta prova, você será perguntado sobre PCI Express, pois este é o barramento mais recente e oferece melhor controle do sistema.
8. Os principais pontos a serem estudados são os de processador e memória.
9. No final, revise os tópicos principais da prova, não precisa decorar, já que você acabou de receber uma descrição detalhada sobre ela. Não haverá questões ativas na prova do Blackboard.

——————————————————————————————————————————————————


### 📌 Resumo_14 - ✅ Útil técnico

Processador em questão:

   - É responsável pela execução de microcódigos no LAN (Redes Locais de Área), marque como verdadeiro ou falso.
   - Também é o processador responsável pelo envio e recebimento dos elementos em uma rede Zouk (Zoning).

   Observe-se que, mesmo o trabalhador não lendo exatamente o que o processador faz, ele precisa ter conhecimentos básicos para saber onde posicionar os olhos e acompanhar as tarefas principais.

   Algumas etapas importantes ao se trabalhar com processadores são:
   - Estudar o material de forma detalhada;
   - Aprender o funcionamento básico do processador em redes locais e zoning;
   - Identificar os principais pontos a serem observados durante o trabalho.

——————————————————————————————————————————————————

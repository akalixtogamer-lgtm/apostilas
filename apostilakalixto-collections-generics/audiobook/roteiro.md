# Collections e Generics em Java — roteiro para ouvir

Roteiro em texto corrido da apostila "Collections e Generics em Java", do dev-Kalixto, escrito para ser ouvido. Em vez de ler o código linha por linha, ele explica as ideias, as analogias, os erros comuns e onde tudo isso aparece em projetos reais. Os exemplos completos, com código e saída, estão na apostila publicada.

## Abertura

Olá! Aqui começa o estudo de Collections e Generics em Java, do dev-Kalixto.

Este é um assunto que separa quem escreve programas pequenos de quem escreve sistemas de verdade. Quase todo software trabalha com grupos de coisas: os alunos de uma turma, os produtos de um carrinho, os e-mails já cadastrados, os pedidos esperando na cozinha, o estoque de cada item de uma loja. Para guardar e consultar esses grupos, o Java oferece um conjunto de estruturas prontas, chamado Java Collections Framework. E para que essas estruturas sejam seguras, ou seja, para que uma lista de nomes nunca receba um número por engano, o Java usa um recurso chamado Generics.

Nos próximos capítulos, vamos passar por cinco ideias grandes. Primeiro, por que coleções existem e como a família está organizada. Segundo, as quatro personalidades principais: List, Set, Map e Queue. Terceiro, como ordenar objetos. Quarto, Generics: classes e métodos que recebem o tipo como parâmetro, os coringas e o que acontece com os tipos depois da compilação. E quinto, como escolher a estrutura certa, onde tudo isso aparece no mercado e um projeto completo de um studio de dança para amarrar tudo.

Uma dica antes de começar: ouça um capítulo por vez, e depois abra a apostila para rodar os exemplos daquele capítulo. Ouvir constrói a intuição; rodar o código transforma a intuição em habilidade.

## Capítulo 1 — Por que coleções existem

Vamos começar pelo problema. Antes de conhecer coleções, todo estudante de Java aprende o array, o vetor. O array é ótimo, mas tem um defeito de nascença: o tamanho é fixo. Quando você escreve que quer um array de inteiros com quatro posições, ele terá quatro posições para sempre. Chegou a quinta nota de um aluno? Não cabe. Você precisa criar outro array, maior, e copiar tudo à mão. Se tentar escrever na quinta posição, o Java lança um erro de índice fora dos limites.

Além do tamanho, cada problema do mundo real pede um comportamento diferente. Às vezes você quer manter a ordem em que as coisas chegaram. Às vezes você quer proibir repetidos, como num cadastro de e-mails. Às vezes você quer achar algo rapidamente por uma chave, como o preço de um produto pelo nome. E às vezes você quer atender por ordem de chegada, como numa fila. Escrever cada uma dessas estruturas do zero, em cada projeto, seria caro e cheio de bugs.

Um pouco de história ajuda a entender o desenho atual. Na primeira versão do Java, em mil novecentos e noventa e seis, existiam só algumas classes soltas, como Vector e Hashtable, sem uma organização comum. Em mil novecentos e noventa e oito, no JDK um ponto dois, nasceu o Java Collections Framework, projetado por Joshua Bloch. Ele trouxe interfaces que definem o contrato de cada tipo de coleção, implementações prontas e algoritmos como ordenação. Em dois mil e quatro, no Java cinco, chegaram os Generics, o for melhorado e o autoboxing. Depois vieram melhorias de conforto: o operador diamante no Java sete, os lambdas e métodos como forEach e removeIf no Java oito, as fábricas de coleções imutáveis no Java nove e, no Java vinte e um, as Sequenced Collections, que padronizaram como pegar o primeiro e o último elemento.

Guarde esta frase, porque ela resume a apostila inteira: Collections dão as estruturas prontas; Generics garantem, já na compilação, que só entra nelas o tipo certo.

Uma ArrayList, a coleção mais usada do Java, também usa um array por dentro. A diferença é que ela cuida do trabalho chato por você: quando o array interno enche, ela cria um maior e copia os elementos sozinha. Você só pede para adicionar, e ela cresce.

E aqui vai o primeiro hábito profissional: programe para a interface. Quando você declara uma lista, o tipo da variável deve ser a interface List, e só na hora de criar o objeto você escolhe a implementação, por exemplo ArrayList. Assim, se um dia precisar trocar a implementação, você muda uma palavra e o resto do código continua igual.

## Capítulo 2 — A família das coleções

Pense na família das coleções como uma árvore genealógica. No topo está Iterable, que significa simplesmente "algo que pode ser percorrido". Logo abaixo vem Collection, a mãe das coleções. E de Collection nascem três filhas principais: List, Set e Queue.

Cada uma tem uma personalidade. Vamos usar analogias do dia a dia para fixar.

List é a chamada da turma. A ordem importa, cada aluno tem uma posição numerada, começando do zero, e dois alunos podem ter o mesmo nome. A implementação padrão é ArrayList.

Set é a lista de convidados de uma festa. Cada pessoa aparece uma vez só. Se você tentar colocar alguém que já está na lista, nada muda. As implementações mais comuns são HashSet, LinkedHashSet e TreeSet.

Queue é a fila do caixa do supermercado. Quem chega primeiro é atendido primeiro. E existe uma versão com duas pontas, chamada Deque, que também serve como pilha de pratos: o último prato colocado é o primeiro a sair.

E existe um quarto membro importante que, curiosamente, não é filho de Collection: o Map. O Map é um dicionário. Você procura pela palavra, que é a chave, e encontra o significado, que é o valor. As palavras não se repetem, mas dois significados podem ser iguais. As implementações mais comuns são HashMap, LinkedHashMap e TreeMap.

Por que o Map fica de fora da família Collection? Porque ele não guarda elementos soltos, guarda pares de chave e valor. Por isso ele não tem o método add, e sim o método put. E por isso você não percorre um Map diretamente: você percorre uma das visões dele, que são o conjunto de chaves, a coleção de valores ou o conjunto de pares, chamado entrySet. Essa é uma pegadinha clássica de prova e de entrevista: Map não é uma Collection.

Uma última observação sobre a árvore: algumas classes herdam umas das outras. O LinkedHashSet é filho do HashSet, e o LinkedHashMap é filho do HashMap. E a LinkedList é uma classe curiosa, porque é ao mesmo tempo uma List e uma Deque.

## Capítulo 3 — List e ArrayList

Vamos para a prática com a List. Uma List mantém a ordem de inserção, aceita repetidos e dá acesso por posição.

As operações básicas são intuitivas. Add adiciona no final. Get lê uma posição. Set substitui o que está numa posição. Remove tira um elemento. Contains pergunta se um elemento está na lista. E size diz quantos elementos existem.

Imagine o seguinte exemplo, que está na apostila. Você cria uma lista de alunos e adiciona Ana, Bruno e Ana de novo. A lista aceita, e fica Ana, Bruno, Ana. Depois você troca a posição um por Carla. Lembre que a contagem começa do zero, então a posição um é o Bruno, e a lista vira Ana, Carla, Ana. Quando você pede para remover Ana, só a primeira Ana sai, e a lista termina como Carla, Ana.

Aqui mora uma armadilha famosa. Numa lista de números inteiros, se você pede para remover o número um, o Java entende que você quer remover a posição um, e não o valor um. Para remover o valor, você precisa deixar claro que está passando um objeto inteiro, e não uma posição.

Existem quatro jeitos de percorrer uma lista. O for melhorado, que é o mais legível quando você só precisa de cada elemento. O forEach, que é o estilo moderno com lambda ou referência de método. O for com índice, que você usa quando a posição importa. E o Iterator, que é o que o for melhorado usa por baixo dos panos e que dá controle total.

E agora a armadilha mais comum de todas: remover elementos de uma lista enquanto você a percorre com o for melhorado. Isso quebra o iterador escondido, e o Java lança uma exceção chamada ConcurrentModificationException, que quer dizer exceção de modificação concorrente. A solução moderna é usar o método removeIf, passando a condição. Por exemplo, remover todos os números pares de uma lista se escreve numa linha só, e sem risco.

Outro cuidado: o Java tem um jeito rápido de criar listas prontas, o List ponto of. Só que essas listas são imutáveis. Se você tentar adicionar ou remover algo nelas, recebe uma exceção de operação não suportada. Quando precisar editar, crie uma ArrayList nova a partir dela.

Por fim, ArrayList versus LinkedList. A ArrayList guarda tudo num bloco contínuo de memória, então ler qualquer posição é instantâneo, mas inserir no meio obriga a empurrar os vizinhos. A LinkedList é uma corrente de elos, então inserir nas pontas é barato, mas achar a posição número mil exige caminhar elo por elo. Na prática, a ArrayList vence quase sempre. Para filas e pilhas, prefira ArrayDeque.

## Capítulo 4 — Set: elementos únicos

Agora o Set, a lista de convidados. Um Set não admite duplicatas. Mas o que exatamente é uma duplicata? Quem decide são dois métodos que todo objeto Java tem: equals e hashCode.

Um detalhe útil: quando você adiciona algo num Set, o método add responde verdadeiro se o elemento entrou e falso se ele já existia. Isso é ótimo para validar cadastros. Se o add respondeu falso, o e-mail já estava registrado.

Por que o HashSet é tão rápido para dizer se algo existe? Imagine um armário com muitas gavetas numeradas. Quando você quer guardar um objeto, calcula um número a partir dele, que é o hashCode. Esse número diz em qual gaveta o objeto vai. Para procurar depois, você calcula o mesmo número e vai direto na gaveta certa, sem abrir todas as outras. Dentro da gaveta podem existir alguns objetos, e aí o equals confirma qual é o mesmo. Por isso, em média, procurar num HashSet leva o mesmo tempo, com dez elementos ou com dez milhões.

Daqui nasce uma regra de ouro, chamada contrato entre equals e hashCode: se dois objetos são iguais pelo equals, eles precisam ter o mesmo hashCode. Se você quebrar essa regra, objetos iguais caem em gavetas diferentes, e o Set passa a aceitar duplicatas que você nem vê.

Isso acontece muito com classes criadas por você. Com String e Integer funciona sozinho, porque essas classes já implementam equals e hashCode. Mas imagine uma classe Aluno com CPF. Se você não implementar os dois métodos, dois alunos com o mesmo CPF são considerados diferentes, porque o Java compara apenas se são o mesmo objeto na memória. No exemplo da apostila, o Set sem equals fica com dois alunos iguais; o Set com equals fica com um só.

A forma moderna de resolver isso é usar record, disponível desde o Java dezesseis. Um record é uma classe de dados em que o compilador gera automaticamente equals, hashCode e toString a partir dos campos. Para dados que entram em Set ou que servem de chave em Map, o record é a escolha mais segura.

E qual Set escolher? O HashSet é o mais rápido, mas não garante nenhuma ordem. O LinkedHashSet mantém a ordem em que você inseriu, ótimo para um histórico sem repetição. E o TreeSet mantém tudo sempre ordenado, em ordem alfabética para textos e crescente para números. O preço do TreeSet é ser um pouco mais lento, mas ainda muito rápido.

## Capítulo 5 — Map: chave e valor

Vamos ao dicionário, o Map. Um Map associa cada chave única a um valor. Pense num controle de estoque: a chave é o nome do produto e o valor é a quantidade.

Quando você coloca Mouse com dez unidades, e depois coloca Mouse de novo com doze, o Map não cria uma segunda entrada. Ele substitui o valor, porque a chave é única. Agora Mouse vale doze.

Quando você pede o valor de uma chave que não existe, o Map devolve nulo, que em Java é null. E isso causa um erro clássico: se você tenta guardar esse nulo numa variável de número inteiro primitivo, o programa quebra com NullPointerException. Para evitar, use o método getOrDefault, que devolve um valor padrão, como zero, quando a chave não existe.

Para percorrer um Map, você escolhe uma das três visões. A visão de chaves, quando só precisa dos nomes. A visão de valores, quando só precisa das quantidades, por exemplo para somar o estoque total. E a visão de pares, o entrySet, quando precisa de chave e valor juntos. Essa última é a mais eficiente, porque você não precisa buscar cada chave de novo.

O Java oito trouxe métodos que economizam muitas linhas. O primeiro é o merge, perfeito para contar coisas. Imagine contar quantas vezes aparece cada estilo de dança numa lista: samba, forró, samba, jazz, samba, forró. Para cada palavra, você chama merge com o valor um e a regra de somar. Se a palavra ainda não existe, ela entra com um; se já existe, soma um. No final você tem forró dois, jazz um, samba três.

O segundo é o computeIfAbsent, perfeito para agrupar. Imagine agrupar nomes pela letra inicial. Para cada nome, você pede ao Map a lista daquela letra, e se ela ainda não existir, ele cria uma lista vazia na hora. Depois é só adicionar o nome. Resultado: letra A com Ana e Alice, letra B com Bruno e Beatriz, letra C com Carla.

E a escolha da implementação segue a mesma lógica do Set. Aliás, por dentro, o HashSet usa um HashMap. O HashMap é o mais rápido e não garante ordem. O LinkedHashMap mantém a ordem de inserção. E o TreeMap mantém as chaves ordenadas e ainda oferece consultas como "qual é a primeira chave" ou "quais chaves vêm antes desta", ótimas para relatórios e rankings.

## Capítulo 6 — Filas, pilhas e prioridade

Quando a pergunta do seu programa é "quem é o próximo?", você precisa de uma fila.

A Queue segue a regra FIFO, sigla em inglês para primeiro a entrar, primeiro a sair. Pense na fila do caixa: chegaram o cliente A, o cliente B e o cliente C. O primeiro atendido é o A.

As operações da fila vêm em pares. Para inserir, existe o add, que lança exceção se falhar, e o offer, que só devolve falso. Para remover o primeiro da fila, existe o remove, que lança exceção se a fila estiver vazia, e o poll, que devolve nulo. Para apenas espiar quem é o próximo, sem tirar da fila, existe o element e o peek. No dia a dia, offer, poll e peek são os mais usados, porque não explodem quando a fila está vazia.

A Deque, que se lê "déqui", é uma fila de duas pontas. Ela pode funcionar como pilha, seguindo a regra LIFO: último a entrar, primeiro a sair. Pense numa pilha de pratos, ou no Control Z do editor de texto: a última ação feita é a primeira a ser desfeita. O botão voltar do navegador funciona do mesmo jeito. Para pilhas, use ArrayDeque. A antiga classe Stack ainda existe, mas é considerada legada.

E existe a PriorityQueue, a fila de prioridade. Nela, não sai quem chegou primeiro, e sim quem tem maior prioridade. Por padrão, sai sempre o menor elemento. Se você colocar cinco, um e três, sai o um, depois o três, depois o cinco. Com um comparador, você define a prioridade que quiser, como atender primeiro os casos mais urgentes de um pronto-socorro, ou os alunos do plano premium de uma academia.

## Capítulo 7 — Ordenação e coleções modernas

Ordenar objetos é uma das tarefas mais comuns. O Java oferece dois caminhos.

O primeiro é o Comparable, que define a ordem natural de uma classe. A própria classe ensina como se comparar, através do método compareTo. Textos têm ordem natural alfabética, números têm ordem crescente. Cada classe tem uma única ordem natural.

O segundo é o Comparator, que é uma regra de ordenação entregue de fora. Você pode ter quantos quiser: por nome, por nota, por idade, invertido. E desde o Java oito, montar comparadores ficou muito expressivo. Por exemplo, para ordenar uma turma pela maior nota, e em caso de empate pelo nome, você compara pela nota, inverte a ordem para a maior vir primeiro e, em seguida, desempata pelo nome. Lendo o código em voz alta, ele soa quase como a frase em português.

Agora, coleções imutáveis. Uma coleção imutável é aquela que não pode ser alterada depois de criada. Isso parece uma limitação, mas evita uma família inteira de bugs do tipo "quem mexeu nessa lista?". Existem três formas principais. As fábricas List ponto of, Set ponto of e Map ponto of criam coleções imutáveis novas, que não aceitam nulos nem repetidos. O copyOf cria uma cópia imutável de outra coleção. E o unmodifiableList cria uma vista somente leitura: se a lista original mudar, a vista mostra a mudança. Essa diferença entre cópia e vista é pergunta comum de entrevista.

Por fim, as Sequenced Collections, do Java vinte e um. Antes delas, pegar o último elemento era diferente em cada tipo de coleção. Agora as coleções que têm ordem definida, como listas, LinkedHashSet e LinkedHashMap, ganharam métodos uniformes: getFirst para o primeiro, getLast para o último e reversed para ver tudo de trás para frente.

## Capítulo 8 — Generics: tipos como parâmetros

Chegamos à segunda metade do assunto: Generics.

Antes do Java cinco, uma lista guardava qualquer objeto. Você podia colocar um número e, logo depois, um texto, e ninguém impedia. O problema aparecia na hora de ler: você precisava converter o elemento para o tipo esperado, e se alguém tivesse colocado o tipo errado, o programa quebrava em execução, na frente do usuário, com um erro de conversão de classe.

Com Generics, você diz o tipo da lista na declaração: uma lista de inteiros. A partir daí, o compilador barra qualquer tentativa de adicionar um texto, e na leitura você não precisa converter nada. O erro sai da execução e vai para a compilação, que é o melhor lugar possível para um erro aparecer: na sua máquina, e não na do cliente.

Três regras práticas. Primeira: Generics só aceitam tipos de referência. Não existe lista de int; existe lista de Integer. O Java converte automaticamente entre o número primitivo e o objeto, num processo chamado autoboxing. Segunda: use o operador diamante, aqueles sinais de menor e maior vazios, para o compilador deduzir o tipo sem você repetir. Terceira: nunca use o tipo cru, ou seja, uma List sem tipo. Ele só existe para compatibilidade com código antigo.

Você também pode criar suas próprias classes genéricas. O exemplo clássico é uma Caixa de T. Esse T é um parâmetro de tipo, um espaço reservado que será preenchido na hora de criar o objeto. Uma única classe Caixa serve de molde para uma caixa de textos, que guarda "Olá", e para uma caixa de inteiros, que guarda quarenta e dois. Se você tentar guardar um texto na caixa de inteiros, o código nem compila. E quando você lê o número da caixa, pode multiplicar por dois direto, sem conversão.

Existe uma convenção de nomes para esses parâmetros. T para tipo genérico. E para elemento de coleção. K e V para chave e valor, como no Map. R para resultado de uma função.

Métodos também podem ser genéricos. Um método pode declarar o seu próprio T, mesmo dentro de uma classe que não é genérica. Por exemplo, um método que exibe qualquer valor, seja texto, número ou booleano. Ou um método que devolve o primeiro elemento de uma lista, com o mesmo tipo da lista, sem conversão.

E aqui entra um recurso poderoso: o tipo limitado. Imagine um método que encontra o maior elemento de uma lista. Para isso, ele precisa comparar os elementos. Só que um T qualquer pode ser algo que não sabe se comparar. A solução é dizer que T precisa estender Comparable de T. Isso é uma promessa: só entram tipos que sabem se comparar. E o compilador cobra essa promessa de quem chama o método. Com isso, o mesmo método encontra o maior número de uma lista de inteiros e a maior palavra de uma lista de textos.

## Capítulo 9 — Coringas, PECS e o apagamento de tipos

Agora uma ideia que confunde muita gente, então vamos devagar.

Integer é filho de Number. Mas uma lista de Integer não é filha de uma lista de Number. Por quê? Imagine que fosse. Então você poderia passar uma lista de inteiros para um método que recebe lista de Number, e esse método poderia adicionar três vírgula catorze. Pronto: um número decimal dentro de uma lista de inteiros. Para impedir esse desastre, os Generics do Java são invariantes.

Para afrouxar essa regra com segurança, existem os coringas, representados por um ponto de interrogação.

O primeiro é "interrogação extends Number". Ele aceita uma lista de Number ou de qualquer filho, como Integer ou Double. Com ele, você pode ler os elementos como números com segurança. Mas não pode adicionar nada, porque não sabe se a lista é de inteiros ou de decimais. Um método que soma todos os números de qualquer lista numérica usa esse coringa.

O segundo é "interrogação super Integer". Ele aceita uma lista de Integer ou de qualquer pai, como Number ou Object. Com ele, você pode adicionar inteiros com segurança, porque qualquer uma dessas listas aceita inteiros. Mas, na leitura, o único tipo garantido é Object.

Para lembrar quando usar cada um, Joshua Bloch, no livro Java Efetivo, criou a regra PECS: Producer Extends, Consumer Super. Se o parâmetro produz dados que você vai ler, use extends. Se o parâmetro consome dados que você vai escrever, use super. O próprio Java usa essa regra: o método que copia uma lista para outra recebe a origem com extends, porque ela produz, e o destino com super, porque ele consome.

E agora, o que acontece por baixo do capô. Os Generics do Java são verificados pelo compilador e depois apagados. Esse processo se chama type erasure, apagamento de tipos. No arquivo compilado, uma lista de String e uma lista de Integer viram simplesmente List, e o compilador insere as conversões necessárias, garantindo que elas nunca falhem. Isso foi uma escolha de compatibilidade: código novo com Generics precisava conviver com bibliotecas antigas sem Generics.

Esse apagamento traz algumas limitações. Você não pode criar um objeto novo do tipo T, porque em execução ninguém sabe o que T é. A alternativa é receber uma fábrica, como um Supplier de T. Você não pode criar um array de T. Você não pode perguntar se um objeto é uma lista de String, só se é uma lista de qualquer coisa. E não pode usar tipos primitivos, porque depois do apagamento tudo vira Object, e int não é objeto.

## Capítulo 10 — Como escolher, e onde isso aparece no mercado

Com tantas opções, como escolher? Faça três perguntas, nesta ordem.

Primeira pergunta: preciso achar valores por uma chave? Se sim, use um Map. HashMap por padrão, LinkedHashMap se a ordem de inserção importa, TreeMap se as chaves precisam estar ordenadas.

Segunda pergunta: preciso proibir repetidos? Se sim, use um Set. HashSet por padrão, LinkedHashSet para ordem de inserção, TreeSet para ordem crescente.

Terceira pergunta: processo os itens por ordem de chegada ou por prioridade? Se sim, use ArrayDeque para filas e pilhas, ou PriorityQueue para prioridade.

Se a resposta foi não para as três, use uma List, e quase sempre uma ArrayList.

Sobre desempenho, guarde o essencial. Ler uma posição de uma ArrayList é instantâneo. Procurar um elemento num HashSet ou numa chave de HashMap também é, em média, instantâneo. As estruturas em árvore, TreeSet e TreeMap, são um pouco mais lentas, mas crescem muito devagar com o tamanho dos dados. E procurar um valor percorrendo uma lista inteira fica mais lento à medida que a lista cresce.

E isso não é assunto só de faculdade. As bibliotecas que movem empresas inteiras são construídas em cima de coleções e Generics. No Spring Data JPA, muito usado em back-end, os repositórios são interfaces genéricas: você declara um repositório de Aluno com chave do tipo Long, e as consultas devolvem listas de alunos. No Apache Kafka, plataforma de dados em tempo real, o consumidor de mensagens é genérico na chave e no valor. No Android, a biblioteca Room devolve listas de objetos direto do banco de dados. O Google mantém a biblioteca Guava, que estende as coleções com listas imutáveis e com mapas em que uma chave aponta para vários valores. O Eclipse Collections nasceu dentro do banco Goldman Sachs e foi doado à Eclipse Foundation. A biblioteca Jackson, que converte JSON em objetos, usa um truque com classes anônimas para contornar o apagamento de tipos e preservar o tipo genérico de uma lista. O Hibernate devolve resultados de consultas tipadas como listas, sem conversão. E no mundo dos games, a biblioteca fastutil, com coleções especializadas em tipos primitivos, é muito usada no ecossistema do Minecraft Java Edition, justamente para fugir do custo do autoboxing.

Quando você ler essas assinaturas num projeto real, vai saber exatamente o que está acontecendo. É isso que separa quem copia exemplos de quem entende a API.

## Capítulo 11 — Projeto: o studio de dança

Para amarrar tudo, a apostila traz um projeto completo: o sistema de turmas de um studio de dança. Vamos percorrer as decisões de projeto, porque é aí que a teoria vira prática.

Cada aluno é um record com CPF, nome e idade. Por ser record, dois alunos com os mesmos dados são iguais, e isso faz os Sets funcionarem corretamente.

Cada turma tem um estilo, como samba, forró ou jazz funk, e um número máximo de vagas. Os alunos matriculados ficam num LinkedHashSet. Set, porque um aluno não pode ser matriculado duas vezes na mesma turma. Linked, porque queremos lembrar a ordem de matrícula.

Quando a turma está cheia, o aluno vai para a lista de espera, que é uma Queue implementada com ArrayDeque. Quando alguém cancela a matrícula, o primeiro da espera entra automaticamente, com um poll.

As turmas ficam num TreeMap, com o nome do estilo como chave. Assim, buscar a turma de samba é imediato, e listar todas as turmas sai em ordem alfabética.

Existe também um repositório genérico, com dois parâmetros de tipo: K para a chave e T para a entidade. Por dentro, ele usa um Map. O mesmo repositório poderia guardar alunos por CPF, professores por matrícula ou turmas por código, sem uma linha de código duplicada.

Para o relatório, os alunos são copiados para uma ArrayList e ordenados com um comparador por idade e, em caso de empate, por nome. E a contagem de alunos por faixa etária usa merge num TreeMap.

Na simulação da apostila, a turma de samba tem duas vagas. Ana e Bruno entram. Carla vai para a espera. Quando Ana tenta se matricular de novo, o sistema avisa que ela já está na turma. Quando Ana cancela, Carla sai da espera e entra automaticamente. Repare como cada regra de negócio foi resolvida pela escolha da estrutura, e não por um monte de ifs.

## Capítulo 12 — Erros comuns e boas práticas

Vamos revisar os erros que todo mundo comete pelo menos uma vez.

Remover elementos dentro do for melhorado causa exceção de modificação concorrente; use removeIf. Tentar alterar uma lista criada com List ponto of causa exceção de operação não suportada; copie para uma ArrayList. Usar uma classe sem equals e hashCode num HashSet ou como chave de HashMap gera duplicatas invisíveis. Alterar um campo usado no hashCode depois de inserir o objeto num HashSet faz o objeto "sumir", porque ele fica na gaveta errada; por isso, chaves devem ser imutáveis. Remover pelo número numa lista de inteiros remove a posição, não o valor. Esperar ordem de um HashSet ou de um HashMap é pedir para ter surpresa. Usar o tipo cru, sem Generics, empurra erros para a execução. Ler um valor inexistente de um Map e guardar num inteiro primitivo causa NullPointerException. E colocar num TreeSet objetos que não sabem se comparar causa erro, a menos que você entregue um Comparator.

E agora as boas práticas de quem trabalha com isso todo dia. Declare variáveis, parâmetros e retornos pela interface. Devolva coleção vazia, nunca nulo, para não espalhar verificações de nulo pelo código. Prefira coleções imutáveis quando não houver motivo para alterar. Não exponha a coleção interna de uma classe; devolva uma vista somente leitura ou uma cópia, exatamente como a turma do projeto faz. Use record para dados que entram em Set ou servem de chave em Map. Dê nomes no plural, como alunos ou emailsCadastrados. Se souber o tamanho aproximado, informe a capacidade inicial. Aplique a regra PECS em métodos que recebem coleções. E conheça a classe utilitária Collections, que já traz ordenação, embaralhamento, contagem de frequência, maior e menor elemento.

## Encerramento — revisão final

Vamos fechar com uma revisão rápida, como se fosse a véspera da prova.

Collections Framework é o conjunto de interfaces, implementações e algoritmos para grupos de objetos. List tem ordem, índice e aceita repetidos. Set não aceita repetidos. Map associa chave única a valor e não é uma Collection. Queue atende por ordem de chegada, Deque também serve de pilha, e PriorityQueue atende por prioridade. Equals e hashCode definem igualdade nas estruturas de hash e devem ser implementados juntos, ou substituídos por um record. Comparable é a ordem natural; Comparator é a regra externa. Coleções criadas com of são imutáveis. Generics colocam o tipo como parâmetro, levam o erro para a compilação e eliminam conversões. Tipos limitados garantem que certos métodos existam. Extends é para ler, super é para escrever. E os tipos genéricos são apagados depois da compilação.

Antes de terminar, tente responder mentalmente a estas perguntas. Qual estrutura aceita repetição e preserva a ordem? Qual evita duplicatas? Qual associa chave e valor? Por que uma lista de String é mais segura que uma lista sem tipo? Quando usar HashSet, LinkedHashSet ou TreeSet? E como percorrer um Map usando o entrySet? Se alguma resposta não veio na hora, volte ao capítulo correspondente.

O próximo passo é abrir a apostila, rodar os exemplos, fazer os exercícios e encarar o quiz de fixação, com vinte e quatro questões e placar por tema.

Obrigado por estudar com o dev-Kalixto. Professor, programador e gamer. Até a próxima!

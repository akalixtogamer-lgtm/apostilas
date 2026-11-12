# Layout Console Kalixto

Layout padrão das apostilas, tirado de `apostilakalixto-console-git-gh`:
cena de névoa néon com bolhas de vidro, cabeçalho HUD com título em gradiente
e busca, um painel de vidro por capítulo (emblema numerado à esquerda,
conteúdo à direita) e botão flutuante que abre o índice.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| `aplicar.py` | Aplica o layout num `index.html`. A tabela `APOSTILAS` diz, por apostila, onde estão capa, capítulos e navegação antiga. |
| `tokens.css` | Tokens do Kalixto Design System (injetados só em apostilas que ainda não os tinham). |
| `console-base.css` | CSS do layout de referência, ligado aos tokens do DS. |
| `console-apostila.css` | Extensões: painel por capítulo, divisor de parte, índice, responsivo. |
| `console.js` | Busca por capítulo e índice flutuante. |
| `_kxbar.html`, `_kxsig.html` | Barra e assinatura dev-Kalixto com o logo embutido. |

Tudo é embutido no próprio `index.html`, então cada apostila continua sendo um
arquivo único.

## Apostila nova

1. Crie a pasta `apostilakalixto-<nome>/index.html` normalmente.
2. Acrescente uma entrada em `APOSTILAS` (o comentário acima da tabela explica cada chave).
3. Rode:

```bash
pip install beautifulsoup4 html5lib
python3 _layout/aplicar.py <nome>
```

O script ignora apostilas que já têm `.moldura`, então pode ser rodado de novo
sem risco. Sidebars, topbars e capas antigas recebem a classe `kx-oculto` em vez
de serem apagadas, para o JavaScript de cada apostila (quiz, progresso,
checklists) seguir funcionando.

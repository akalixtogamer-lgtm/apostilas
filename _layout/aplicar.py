#!/usr/bin/env python3
"""
Console Kalixto — aplica o layout da apostila de referência
(apostilakalixto-console-git-gh) nas demais apostilas do repositório.

O que o script faz em cada index.html:
  1. cena de fundo (névoa néon + bolhas de vidro) e barra dev-Kalixto;
  2. cabeçalho HUD: título em gradiente, resumo e busca por capítulo;
  3. cada capítulo vira um painel de vidro (.bloco) com emblema numerado
     na coluna esquerda e o conteúdo original na direita;
  4. botão flutuante que abre o índice de capítulos;
  5. sidebars, topbars e capas antigas ficam ocultas (não são apagadas,
     para o JavaScript de cada apostila continuar funcionando).

Uso:
    python3 _layout/aplicar.py                 # todas as apostilas da tabela
    python3 _layout/aplicar.py excel angular   # só as indicadas

É seguro rodar de novo: apostila que já tem .moldura é ignorada.
Para uma apostila nova, acrescente uma entrada em APOSTILAS.
Requer: pip install beautifulsoup4 html5lib
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

FONTES = ('https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700&family=Sora:wght@600'
          '&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap')

# Variáveis próprias de cada apostila apontadas para os tokens do Design System.
FONTES_DS = {
    'display': '"Unbounded","Sora",system-ui,sans-serif',
    'body': '"Inter",system-ui,-apple-system,"Segoe UI",sans-serif',
    'mono': '"JetBrains Mono",ui-monospace,Consolas,monospace',
}

# ----------------------------------------------------------------------------
# Tabela de apostilas
#   capitulos  seletor dos elementos que viram painel
#   titulo     seletor (dentro do capítulo) do título que vai para a coluna
#   marca      seletor (dentro do capítulo) do rótulo curto acima do título
#   partes     seletor dos divisores de parte
#   capa       seletor da capa/hero antiga (fica oculta; o h1 sobe para o HUD)
#   resumo     seletor (dentro da capa) do texto de apresentação
#   fichas     seletor (dentro da capa) de itens curtos que viram chips no HUD
#   ocultar    seletores de navegação antiga
#   dividir    (contêiner, tag) quando os capítulos são só títulos soltos
#   embrulhar  seletor de elementos soltos que viram um capítulo cada
#   largo      True = painel em coluna única (conteúdo que precisa de largura total)
#   css        CSS extra só desta apostila
#   numerar    'ordem' ignora a numeração própria e conta os painéis em sequência
#   nome       ('Capítulo', 'capítulos') usado no emblema e na busca
#   vars       ponte variável-da-apostila -> token do DS
#   tema       'escuro' fixa o tema escuro (apostilas sem modo claro próprio)
# ----------------------------------------------------------------------------
AP = dict(capitulos='section.ap-cap', titulo='header h2', marca='header .kx-eyebrow, header .t-overline',
          partes='div.ap-part', capa='header.ap-hero', resumo='p.sub',
          fichas='.ap-meta > *', ocultar=['nav.ap-toc'])
BIO = dict(capitulos='main .wrap > section', titulo='h1.ch', marca='.eyebrow, .overline',
           capa='header.cover', resumo='p.sub, .cover-in p',
           ocultar=['.topbar', 'aside.rail', '.rail', '.scrim', '.kx-orbs'])
AULA = dict(capitulos='section.aula', titulo='.sec-head h2', marca='.sec-head .kx-eyebrow',
            capa='header.hero', resumo='p', ocultar=['.toc', 'a.kx-back'],
            nome=('Aula', 'aulas'))

APOSTILAS = {
    'collections-generics': AP,
    'etimologia-medica': AP,
    'logica-de-programacao': AP,
    'machine-learning': AP,
    'biomecanica': BIO,
    'bioquimica-do-exercicio': BIO,
    'cinesiologia': BIO,
    'treinamento-resistido': BIO,
    'design-patterns': dict(BIO, capa='section.cover', partes='div.part', numerar='ordem',
                            ocultar=['.topbar', 'aside.rail', '.scrim'],
                            css='body.kxc .calmtog{right:auto !important;left:16px !important}\n'),
    'como-estudar-danca': AULA,
    'probabilidade': AULA,
    'angular': dict(
        capitulos='section.ch', titulo='.ch-head h2', marca='.ch-head .ch-num',
        capa='header.cover', resumo='p', ocultar=['div.topbar', 'nav.toc'],
        vars={'--bg': 'var(--bg-base)', '--bg2': 'var(--bg-surface)', '--surface': 'var(--glass-fill)',
              '--surface-2': 'color-mix(in srgb,var(--text-primary) 10%,transparent)',
              '--fg': 'var(--text-primary)', '--fg-dim': 'var(--text-secondary)',
              '--line': 'var(--glass-stroke)', '--purple': 'var(--brand-primary)',
              '--pink': 'var(--brand-secondary)', '--blue': 'var(--brand-tertiary)',
              '--accent': 'var(--brand-tertiary)', '--accent-2': 'var(--brand-secondary)',
              '--link': 'var(--brand-tertiary)', '--f-mono': FONTES_DS['mono']}),
    'angular-cadastro': dict(
        capitulos='section.block', titulo='h2', capa='section.hero', resumo='p',
        ocultar=['header.topbar', 'aside.drawer', '.scrim', 'main > nav.toc'], tema='escuro',
        nome=('Etapa', 'etapas'),
        vars={'--bg': 'var(--bg-base)', '--bg2': 'var(--bg-surface)', '--card': 'var(--glass-fill)',
              '--line': 'var(--glass-stroke)', '--text': 'var(--text-primary)',
              '--muted': 'var(--text-secondary)', '--magenta': 'var(--brand-secondary)',
              '--purple': 'var(--brand-primary)', '--blue': 'var(--brand-tertiary)',
              '--mono': FONTES_DS['mono']}),
    'apps-no-figma': dict(
        capitulos='section.chapter', titulo='.ch-head h2', marca='.ch-head .ch-eyebrow',
        capa='header.hero', resumo='p',
        ocultar=['aside.sidebar', 'div.topbar', '.drawer-scrim', 'button.totop', '.ring-float'],
        tema='claro'),
    'excel': dict(dividir=('article.doc', 'h2'), capitulos='section.kx-cap', titulo='h2',
                  capa=None, h1='article.doc > h1', resumo_sel='article.doc > p.meta',
                  ocultar=['div.wrap > div.top', 'div.wrap > hr.kx-rule', 'footer.sig']),
    'figma-claude-mcp': dict(
        capitulos='section.section:not(.section--cover)', titulo='h2.mod-title, h1.title, h2',
        marca='.eyebrow', capa='section.section--cover', resumo='p',
        ocultar=['aside.rail', 'header.topbar', '.scrim'], tema='escuro',
        nome=('Módulo', 'módulos'),
        vars={'--bg': 'var(--bg-base)', '--bg-grad-1': 'transparent', '--bg-grad-2': 'transparent',
              '--surface': 'var(--glass-fill)', '--ink': 'var(--text-primary)',
              '--ink-2': 'var(--text-secondary)', '--ink-3': 'var(--text-muted)',
              '--magenta': 'var(--brand-secondary)', '--purple': 'var(--purple-300)',
              '--blue': 'var(--brand-tertiary)', '--cyan': 'var(--brand-tertiary)',
              '--line': 'var(--glass-stroke)'}),
    'frontend-ii': dict(
        capitulos='section.module', titulo='.mhead h2', marca='.mhead .eb',
        capa='section.hero', resumo='p',
        ocultar=['aside.sidebar', '.menu-btn', '.scrim', '.toTop'], nome=('Módulo', 'módulos')),
    'git-do-zero-ao-push': dict(
        capitulos='div.page div.step, div.page section.block', titulo='h2',
        capa='header.hero', resumo='p', marca='.eyebrow', nome=('Passo', 'passos'),
        ocultar=['div.step > .num'],
        css='body.kxc .err code{white-space:normal !important;overflow-wrap:anywhere}\n'),
    'hash-senhas-python': dict(
        capitulos='div.wrap > section', titulo='h2', marca='p.kicker',
        capa='header.hero', resumo='p:not(.hero-eyebrow)', ocultar=['nav.topnav'],
        css='@media (max-width:600px){body.kxc .vs{grid-template-columns:minmax(0,1fr) !important}}\n',
        nome=('Seção', 'seções')),
    'luiz-gama': dict(
        capitulos='main > article.cap, main > section.parte-capa:not([id^="parte"])',
        partes='main > section.parte-capa[id^="parte"]',
        titulo='h2, h3', marca='.rotulo, .miolo > span.num', capa='header.hero', resumo='p.sub',
        ocultar=['nav.topo', '#subir', 'a.kx-back', 'div.faixa']),
    'mcp-no-terminal': dict(
        capitulos='div.page > section', titulo='h2', capa='div.page > header', resumo='p',
        nome=('Passo', 'passos')),
    'personalidades-negras': dict(
        renomear={'bloco': 'pn-bloco', 'lista': 'pn-lista'},
        capitulos='main > section.pn-bloco', titulo='h2, .cap-hero h3, h3', marca='.cap-hero .num',
        partes='main > div.parte', capa='header.capa', resumo='p.sub',
        ocultar=['#topo-btn', 'div.faixa-kente'], tema='escuro',
        vars={'--noite': 'var(--bg-base)', '--carvao': 'var(--glass-fill)',
              '--carvao-2': 'color-mix(in srgb,var(--text-primary) 10%,transparent)',
              '--papel': 'var(--text-primary)', '--papel-suave': 'var(--text-secondary)',
              '--linha': 'var(--glass-stroke)'}),
    'portas-logicas': dict(
        capitulos='div.wrap > section.block', titulo='h2', marca='.eyebrow',
        capa='header.hero', resumo='p', tema='escuro', nome=('Seção', 'seções'),
        ocultar=['div.wrap > nav.toc'],
        vars={'--bg': 'var(--bg-base)', '--panel': 'var(--glass-fill)',
              '--panel2': 'color-mix(in srgb,var(--text-primary) 10%,transparent)',
              '--line': 'var(--glass-stroke)', '--fg': 'var(--text-primary)',
              '--muted': 'var(--text-secondary)', '--magenta': 'var(--brand-secondary)',
              '--purple': 'var(--purple-300)', '--blue': 'var(--brand-tertiary)',
              '--f-display': FONTES_DS['display'], '--f-body': FONTES_DS['body'],
              '--f-mono': FONTES_DS['mono']}),
    'programming-symbols': dict(
        embrulhar='div.stage', capitulos='section.kx-cap', titulo=None, capa='header.hero',
        resumo='p.t-body-l', ocultar=['a.kx-back', 'footer.sig'], nome=('Painel', 'painéis'),
        rotulo_fixo='26 símbolos em 7 categorias', largo=True),
    'ui-figma': dict(
        capitulos='section.module', titulo='.module__head h2', marca='.module__head .module__kicker',
        capa='section.hero', resumo='p',
        ocultar=['header.topbar', 'aside.sidebar', '.sidebar', '.scrim'], tema='escuro',
        nome=('Módulo', 'módulos'),
        vars={'--kx-void': 'var(--bg-base)', '--kx-surface': 'var(--glass-fill)',
              '--kx-surface-2': 'color-mix(in srgb,var(--text-primary) 10%,transparent)',
              '--kx-line': 'var(--glass-stroke)', '--kx-magenta': 'var(--brand-secondary)',
              '--kx-purple': 'var(--purple-300)', '--kx-blue': 'var(--brand-tertiary)',
              '--kx-text': 'var(--text-primary)', '--kx-text-soft': 'var(--text-secondary)',
              '--kx-text-mute': 'var(--text-muted)',
              '--font-display': FONTES_DS['display'], '--font-body': FONTES_DS['body'],
              '--font-mono': FONTES_DS['mono']}),
}

CENA = '''<div class="cena" aria-hidden="true">
  <div class="cena__nevoa cena__nevoa--ciano"></div>
  <div class="cena__nevoa cena__nevoa--magenta"></div>
  <div class="cena__nevoa cena__nevoa--violeta"></div>
  <div class="cena__bolha cena__bolha--1"></div>
  <div class="cena__bolha cena__bolha--2"></div>
  <div class="cena__bolha cena__bolha--3"></div>
  <div class="cena__bolha cena__bolha--4"></div>
  <div class="cena__bolha cena__bolha--5"></div>
</div>'''

BUSCA = '''<div class="busca">
  <svg class="busca__icone" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
  <input class="busca__campo" id="kx-busca" type="search" data-nome="{plural}"
         placeholder="Filtrar {plural} por palavra" aria-label="Filtrar {plural}"
         enterkeyhint="search" inputmode="search"
         autocomplete="off" autocorrect="off" autocapitalize="none" spellcheck="false">
  <span class="busca__contagem" id="kx-contagem"></span>
</div>'''

FLUTUANTE = '''<button class="flutuante" id="kx-alternar" type="button" aria-expanded="false" aria-controls="kx-indice" aria-label="Abrir índice">
  <span class="flutuante__dica">Índice</span>
  <svg class="flutuante__cruz" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>
</button>'''

FIOS = '''<svg class="bloco__fios" viewBox="0 0 60 400" preserveAspectRatio="none" aria-hidden="true">
  <path class="bloco__fio" d="M0 60 C 30 60, 30 20, 60 20"/>
  <path class="bloco__fio" d="M0 60 C 30 60, 30 120, 60 120"/>
  <path class="bloco__fio" d="M0 60 C 34 60, 34 230, 60 230"/>
  <path class="bloco__fio" d="M0 60 C 34 60, 34 340, 60 340"/>
</svg>'''

TEMA_CEDO = ("(function(){try{var t=localStorage.getItem('kx-theme');if(t==='light'||t==='dark')"
             "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();")

TEMA_BOTAO = ('<button class="kx-theme" id="kx-theme" type="button" aria-label="Alternar modo claro e escuro">'
              '<span class="ic" aria-hidden="true"></span><span id="kx-theme-t">Modo claro</span></button>')

TEMA_CSS = '''.kx-theme{position:fixed;right:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:50;display:inline-flex;align-items:center;gap:8px;
  font:600 14px/20px var(--f-heading,'Sora',system-ui,sans-serif);color:var(--text-primary,#fff);cursor:pointer;
  background:var(--glass-fill,rgba(255,255,255,.06));border:1px solid var(--glass-stroke,rgba(255,255,255,.14));border-radius:999px;padding:10px 16px;
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);box-shadow:var(--glass-shadow-s,0 12px 32px rgba(0,0,0,.35))}
.kx-theme:hover{box-shadow:0 0 32px rgba(123,46,255,.45)}
.kx-theme:focus-visible{outline:2px solid var(--brand-tertiary,#00D9FF);outline-offset:3px}
.kx-theme .ic{width:18px;height:18px;border-radius:50%;background:linear-gradient(90deg,#7B2EFF,#FF2DAA);flex:none}
@media print{.kx-theme{display:none}}'''

TEMA_JS = '''(function(){
  var root=document.documentElement, b=document.getElementById('kx-theme'), t=document.getElementById('kx-theme-t');
  function cur(){var a=root.getAttribute('data-theme');if(a)return a;return window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';}
  function paint(){t.textContent=cur()==='dark'?'Modo claro':'Modo escuro';}
  b.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('kx-theme',n);}catch(e){}paint();
    if(document.querySelector('.mermaid'))location.reload();});
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change',paint);
  paint();
})();'''


def frag(soup, html):
    """Converte um trecho de HTML em nós do documento."""
    tmp = BeautifulSoup('<div id="kx-tmp">' + html + '</div>', 'html5lib').find(id='kx-tmp')
    return [n.extract() for n in list(tmp.contents)]


def emblema(n, rotulo, num):
    return f'''<svg class="bloco__emblema" width="150" height="150" viewBox="0 0 120 120" role="img" aria-label="{rotulo} {num}">
  <defs>
    <linearGradient id="kxv{n}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".85"/>
      <stop offset="45%" style="stop-color:var(--luz)" stop-opacity=".55"/>
      <stop offset="100%" style="stop-color:var(--luz-2)" stop-opacity=".35"/>
    </linearGradient>
    <radialGradient id="kxb{n}" cx="35%" cy="28%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".95"/>
      <stop offset="55%" style="stop-color:var(--luz)" stop-opacity=".45"/>
      <stop offset="100%" stop-color="#0d0a1d" stop-opacity=".15"/>
    </radialGradient>
  </defs>
  <rect x="8" y="8" width="104" height="104" rx="30" fill="url(#kxv{n})" opacity=".16" style="stroke:var(--luz)" stroke-opacity=".45" stroke-width="1.2"/>
  <path d="M26 92 H70" fill="none" style="stroke:var(--luz)" stroke-opacity=".8" stroke-width="3" stroke-linecap="round"/>
  <path d="M26 82 H52" fill="none" style="stroke:var(--luz-2)" stroke-opacity=".75" stroke-width="3" stroke-linecap="round"/>
  <text class="bloco__numero" x="26" y="66">{num}</text>
  <circle cx="90" cy="32" r="9" fill="url(#kxb{n})" stroke="#ffffff" stroke-opacity=".5"/>
  <circle cx="90" cy="88" r="5" fill="url(#kxb{n})" stroke="#ffffff" stroke-opacity=".4"/>
  <ellipse cx="46" cy="26" rx="18" ry="9" fill="#ffffff" opacity=".10" transform="rotate(-28 46 26)"/>
</svg>'''


def texto(el, limite=None):
    t = re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip()
    if limite and len(t) > limite:
        t = t[:limite].rsplit(' ', 1)[0].rstrip(' ,;:—-') + '…'
    return t


def add_classe(el, *nomes):
    atual = el.get('class', [])
    for n in nomes:
        if n not in atual:
            atual.append(n)
    el['class'] = atual


def ancestrais(el):
    out = []
    p = el.parent
    while p is not None and p.name not in ('body', 'html', '[document]'):
        out.append(p)
        p = p.parent
    return out


def ancestral_comum(els):
    comuns = None
    for e in els:
        cadeia = [e] + ancestrais(e)
        ids = [id(x) for x in cadeia]
        if comuns is None:
            comuns = cadeia[1:]
        else:
            comuns = [c for c in comuns if id(c) in ids]
    return comuns[0] if comuns else None


def renomear_classes(html, mapa):
    """Evita choque entre classes da apostila e as do layout (.bloco, .lista)."""
    for antigo, novo in mapa.items():
        def troca_attr(m):
            classes = [novo if c == antigo else c for c in m.group(2).split()]
            return m.group(1) + ' '.join(classes) + m.group(3)
        html = re.sub(r'(class=")([^"]*)(")', troca_attr, html)
        html = re.sub(r'\.' + re.escape(antigo) + r'(?![\w-])', '.' + novo, html)
    return html


def dividir(soup, seletor, tag):
    """Agrupa 'título + irmãos até o próximo título' em <section class="kx-cap">."""
    caixa = soup.select_one(seletor)
    atual = None
    for no in list(caixa.children):
        if getattr(no, 'name', None) == tag:
            atual = soup.new_tag('section', attrs={'class': 'kx-cap'})
            no.insert_before(atual)
        if atual is not None:
            atual.append(no.extract())


def aplicar(slug, cfg):
    caminho = RAIZ / f'apostilakalixto-{slug}' / 'index.html'
    html = caminho.read_text(encoding='utf-8')
    if 'class="moldura' in html:
        return f'{slug}: já está no layout, ignorada'

    if cfg.get('renomear'):
        html = renomear_classes(html, cfg['renomear'])
    tem_ds = 'Primitives' in html and '--glass-fill' in html
    soup = BeautifulSoup(html, 'html5lib')
    head, body = soup.head, soup.body
    singular, plural = cfg.get('nome', ('Capítulo', 'capítulos'))

    if cfg.get('dividir'):
        dividir(soup, *cfg['dividir'])
    for el in (soup.select(cfg['embrulhar']) if cfg.get('embrulhar') else []):
        el.wrap(soup.new_tag('section', attrs={'class': 'kx-cap'}))

    for sel in cfg.get('ocultar', []):
        for el in soup.select(sel):
            add_classe(el, 'kx-oculto')

    # ---------- capa -> HUD ----------
    capa = soup.select_one(cfg['capa']) if cfg.get('capa') else None
    h1 = soup.select_one(cfg['h1']) if cfg.get('h1') else (capa or soup).find('h1')
    resumo = ''
    if capa and cfg.get('resumo'):
        for p in capa.select(cfg['resumo']):
            if len(texto(p)) > 40:
                resumo = texto(p, 300)
                break
    if cfg.get('resumo_sel'):
        p = soup.select_one(cfg['resumo_sel'])
        if p:
            resumo = texto(p, 300)
            add_classe(p, 'kx-oculto')
    fichas = []
    if capa and cfg.get('fichas'):
        fichas = [texto(f, 60) for f in capa.select(cfg['fichas']) if texto(f)]

    hud = soup.new_tag('header', attrs={'class': 'hud'})
    for n in frag(soup, '<span class="hud__marca"><span class="hud__ponto"></span>dev-Kalixto</span>'):
        hud.append(n)
    if h1 is not None:
        h1.extract()
        for br in h1.find_all('br'):
            br.replace_with(' ')
        for filho in h1.find_all(True, recursive=False):
            filho.insert_before(' ')
        add_classe(h1, 'hud__titulo')
        hud.append(h1)
    if resumo:
        p = soup.new_tag('p', attrs={'class': 'hud__resumo'})
        p.string = resumo
        hud.append(p)
    if fichas:
        caixa = soup.new_tag('div', attrs={'class': 'hud__extras'})
        for f in fichas[:6]:
            s = soup.new_tag('span', attrs={'class': 'hud__ficha'})
            s.string = f
            caixa.append(s)
        hud.append(caixa)
    for n in frag(soup, BUSCA.format(plural=plural)):
        hud.append(n)
    if capa is not None:
        add_classe(capa, 'kx-oculto')

    # ---------- capítulos -> painéis ----------
    capitulos = [c for c in soup.select(cfg['capitulos']) if 'kx-oculto' not in c.get('class', [])]
    capitulos = [c for c in capitulos if not any('kx-oculto' in a.get('class', []) for a in ancestrais(c))]
    if not capitulos:
        raise SystemExit(f'{slug}: nenhum capítulo encontrado com {cfg["capitulos"]!r}')
    partes = soup.select(cfg['partes']) if cfg.get('partes') else []
    for p in partes:
        add_classe(p, 'kx-parte')

    miolo = ancestral_comum(capitulos) if len(capitulos) > 1 else capitulos[0].parent
    if miolo is None or miolo.name == 'body':
        miolo = soup.new_tag('div')
        capitulos[0].insert_before(miolo)
        fim = capitulos[-1]
        no = miolo.next_sibling
        while no is not None:
            prox = no.next_sibling
            miolo.append(no.extract())
            if no is fim:
                break
            no = prox
    add_classe(miolo, 'moldura')
    for a in ancestrais(miolo):
        add_classe(a, 'kx-plano')
    for c in capitulos:
        for a in ancestrais(c):
            if a is miolo:
                break
            add_classe(a, 'kx-plano')

    # número do emblema: o da própria apostila quando o rótulo traz um ("Capítulo 03");
    # sem numeração própria, a ordem dos painéis
    def numero_proprio(cap):
        marca = cap.select_one(cfg['marca']) if cfg.get('marca') else None
        achado = re.search(r'(?<![\w.])(\d{1,2})(?![\w])', texto(marca)) if marca is not None else None
        return int(achado.group(1)) if achado else None
    proprios = {id(c): numero_proprio(c) for c in capitulos}
    usa_proprio = sum(v is not None for v in proprios.values()) >= max(2, len(capitulos) // 2)
    if cfg.get('numerar') == 'ordem':
        usa_proprio = False

    itens_indice = []
    ordem = {id(c): n for n, c in enumerate(capitulos, 1)}
    for el in soup.find_all(True):
        if id(el) in ordem:
            n = ordem[id(el)]
            cap = el
            titulo = cap.select_one(cfg['titulo']) if cfg.get('titulo') else None
            if titulo is None and not cfg.get('rotulo_fixo'):
                titulo = cap.find(['h1', 'h2', 'h3', 'h4'])
            marca = cap.select_one(cfg['marca']) if cfg.get('marca') else None
            if marca is not None and titulo is not None and titulo in marca.find_all(True):
                marca = None

            coluna = soup.new_tag('div', attrs={'class': 'bloco__coluna'})
            fixo = soup.new_tag('div', attrs={'class': 'bloco__fixo'})
            coluna.append(fixo)
            num = f'{n:02d}'
            if usa_proprio:
                num = f'{proprios[id(el)]:02d}' if proprios[id(el)] is not None else '◆'
            for nd in frag(soup, emblema(n, singular, num)):
                fixo.append(nd)
            m = soup.new_tag('span', attrs={'class': 'bloco__marca'})
            if marca is not None and texto(marca):
                m.string = texto(marca, 48)
                marca.extract()
            else:
                m.string = f'{singular} {num}' if num != '◆' else singular
            fixo.append(m)
            if titulo is not None:
                titulo.extract()
                add_classe(titulo, 'bloco__rotulo')
                rotulo = texto(titulo)
            else:
                rotulo = cfg.get('rotulo_fixo') or (cap.get('id') or f'{singular} {n}')
                titulo = soup.new_tag('h2', attrs={'class': 'bloco__rotulo'})
                titulo.string = rotulo
            fixo.append(titulo)
            for nd in frag(soup, FIOS):
                coluna.append(nd)

            conteudo = soup.new_tag('div', attrs={'class': 'bloco__conteudo'})
            for no in list(cap.contents):
                conteudo.append(no.extract())
            cap.append(coluna)
            cap.append(conteudo)
            add_classe(cap, 'bloco', f'bloco--c{(n - 1) % 4 + 1}', *(['bloco--largo'] if cfg.get('largo') else []))
            cap['data-item'] = ''
            if not cap.get('id'):
                cap['id'] = f'kx-cap-{n}'
            itens_indice.append(('cap', num, rotulo, cap['id']))
        elif 'kx-parte' in el.get('class', []):
            cab = el.find(['h1', 'h2', 'h3'])
            itens_indice.append(('parte', '', texto(cab or el, 70), ''))

    vazio = soup.new_tag('p', attrs={'class': 'vazio'})
    vazio.string = f'Nenhum resultado nos {plural}. Tente outra palavra.'
    miolo.append(vazio)

    # ---------- índice flutuante ----------
    linhas = []
    for tipo, n, rot, alvo in itens_indice:
        rot = rot.replace('&', '&amp;').replace('<', '&lt;')
        if tipo == 'parte':
            linhas.append(f'<li class="indice__parte">{rot}</li>')
        else:
            linhas.append(f'<li><a class="indice__link" href="#{alvo}"><b>{n}</b><span>{rot}</span></a></li>')
    indice = (f'<nav class="indice" id="kx-indice" aria-label="Índice de {plural}">'
              f'<p class="indice__topo">Índice · {len(capitulos)} {plural}</p>'
              f'<ul class="indice__lista">{"".join(linhas)}</ul></nav>')

    # ---------- montagem do body ----------
    add_classe(body, 'kxc')
    add_classe(soup.html, 'kxc-raiz')
    barra = body.select_one('.kx-bar')
    if barra is None:
        barra = frag(soup, (AQUI / '_kxbar.html').read_text(encoding='utf-8'))[0]
    else:
        barra.extract()
    hud_caixa = soup.new_tag('div', attrs={'class': 'moldura moldura--hud'})
    hud_caixa.append(hud)
    for n in reversed(frag(soup, CENA)):
        body.insert(0, n)
    cena = body.select_one('.cena')
    cena.insert_after(barra)
    barra.insert_after(hud_caixa)

    assinatura = body.select_one('footer.kx-sig')
    if assinatura is None:
        assinatura = frag(soup, (AQUI / '_kxsig.html').read_text(encoding='utf-8'))[0]
        body.append(assinatura)
    for n in frag(soup, FLUTUANTE + indice):
        body.append(n)

    # ---------- head ----------
    if 'family=Unbounded' not in html:
        for n in frag(soup, '<link rel="preconnect" href="https://fonts.googleapis.com">'
                            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                            f'<link rel="stylesheet" href="{FONTES}">'):
            head.append(n)
    if not head.find('meta', attrs={'name': 'viewport'}):
        head.insert(0, soup.new_tag('meta', attrs={'name': 'viewport', 'content': 'width=device-width, initial-scale=1, viewport-fit=cover'}))
    if not head.find('meta', attrs={'charset': True}):
        head.insert(0, soup.new_tag('meta', attrs={'charset': 'UTF-8'}))

    css = ''
    if not tem_ds:
        css += (AQUI / 'tokens.css').read_text(encoding='utf-8') + '\n'
    if cfg.get('vars'):
        css += ('/* ponte: variáveis desta apostila -> tokens do Kalixto DS */\n:root:not(#kx){'
                + ';'.join(f'{k}:{v}' for k, v in cfg['vars'].items()) + '}\n')
    css += (AQUI / 'console-base.css').read_text(encoding='utf-8')
    css += (AQUI / 'console-apostila.css').read_text(encoding='utf-8')
    if cfg.get('css'):
        css += cfg['css']
    estilo = soup.new_tag('style', attrs={'id': 'kx-console'})
    estilo.string = '\n' + css
    # depois de todos os estilos da apostila, inclusive os que ficam no body
    head.append(estilo)

    tema = cfg.get('tema')
    if tema == 'escuro':
        soup.html['data-theme'] = 'dark'
    elif tema == 'claro':
        soup.html['data-theme'] = 'light'
    elif not body.select_one('#kx-theme, .themetog'):
        cedo = soup.new_tag('script')
        cedo.string = TEMA_CEDO
        head.insert(0, cedo)
        st = soup.new_tag('style')
        st.string = TEMA_CSS
        body.append(st)
        for n in frag(soup, TEMA_BOTAO):
            body.append(n)
        sc = soup.new_tag('script')
        sc.string = TEMA_JS
        body.append(sc)

    js = soup.new_tag('script', attrs={'id': 'kx-console-js'})
    js.string = '\n' + (AQUI / 'console.js').read_text(encoding='utf-8')
    body.append(js)

    saida = str(soup)
    if not saida.lower().startswith('<!doctype'):
        saida = '<!DOCTYPE html>\n' + saida
    caminho.write_text(saida, encoding='utf-8')
    return f'{slug}: {len(capitulos)} {plural}, {len(partes)} partes | ' + ' '.join(i[1] for i in itens_indice if i[0] == 'cap')


if __name__ == '__main__':
    alvos = sys.argv[1:] or list(APOSTILAS)
    for slug in alvos:
        print(aplicar(slug, APOSTILAS[slug]))

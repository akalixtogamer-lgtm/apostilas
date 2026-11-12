/* Console Kalixto — busca por capítulo e índice flutuante */
(function(){
  var campo = document.getElementById('kx-busca');
  var contador = document.getElementById('kx-contagem');
  var itens = [].slice.call(document.querySelectorAll('.bloco[data-item]'));
  var partes = [].slice.call(document.querySelectorAll('.kx-parte'));
  var nome = (campo && campo.dataset.nome) || 'capítulos';
  var textos = null;

  function filtrar(){
    var termo = campo.value.trim().toLowerCase();
    if (termo && !textos) textos = itens.map(function(i){ return i.textContent.toLowerCase(); });
    var visiveis = 0;
    itens.forEach(function(item, n){
      var bate = !termo || textos[n].indexOf(termo) !== -1;
      item.hidden = !bate;
      if (bate) visiveis++;
    });
    partes.forEach(function(p){ p.hidden = !!termo; });
    document.body.classList.toggle('kx-sem-resultado', visiveis === 0);
    contador.textContent = termo ? visiveis + '/' + itens.length : itens.length + ' ' + nome;
  }
  if (campo){
    campo.addEventListener('input', filtrar);
    campo.addEventListener('keydown', function(e){
      if (e.key === 'Enter'){ e.preventDefault(); campo.blur(); }
    });
    filtrar();
  }

  /* ---------- Botão flutuante: abre o índice ---------- */
  var botao = document.getElementById('kx-alternar');
  var indice = document.getElementById('kx-indice');
  if (!botao || !indice) return;
  var dica = botao.querySelector('.flutuante__dica');

  function abrir(sim){
    document.body.classList.toggle('kx-indice-aberto', sim);
    botao.setAttribute('aria-expanded', String(sim));
    botao.setAttribute('aria-label', sim ? 'Fechar índice' : 'Abrir índice');
    if (dica) dica.textContent = sim ? 'Fechar' : 'Índice';
    indice.inert = !sim;
  }
  abrir(false);

  if (window.matchMedia('(hover:none)').matches){
    botao.classList.add('flutuante--apresenta');
    setTimeout(function(){ botao.classList.remove('flutuante--apresenta'); }, 3200);
  }
  botao.addEventListener('click', function(){
    if (navigator.vibrate) { try { navigator.vibrate(12); } catch(e){} }
    abrir(!document.body.classList.contains('kx-indice-aberto'));
  });
  indice.addEventListener('click', function(e){
    var link = e.target.closest('a');
    if (!link) return;
    /* capítulo escondido pela busca volta a aparecer antes de rolar até ele */
    if (campo && campo.value){ campo.value = ''; filtrar(); }
    abrir(false);
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && document.body.classList.contains('kx-indice-aberto')){ abrir(false); botao.focus(); }
  });
  document.addEventListener('click', function(e){
    if (!document.body.classList.contains('kx-indice-aberto')) return;
    if (indice.contains(e.target) || botao.contains(e.target)) return;
    abrir(false);
  });
})();

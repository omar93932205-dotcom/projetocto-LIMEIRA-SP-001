import re
base='/app/frontend/public/'

# Remove o card interno do concurso (imagem + dados) mantendo o wrapper #TopoInformacoes
CARD_RE = re.compile(r'<div class="imagem">.*?<p class="periodoInscricoes">.*?</p>\s*</div>', re.S)
for fn in ['inscricao.html','dados-inscricao.html','confirmacao.html']:
    p=base+fn
    h=open(p,encoding='utf-8').read()
    h2,n = CARD_RE.subn('', h, count=1)
    open(p,'w',encoding='utf-8').write(h2)
    left = h2.count('class="tipo">Concurso')
    print(f"{fn}: card removido={n} | residuo tipo>Concurso={left}")

# Remove o <h2> subtítulo do concurso (mantém recibo do PIX)
H2='<h2>Concurso Público - 01/2026 - Prefeitura Municipal de Limeira</h2>'
for fn in ['pagamento-pix.html','inscricao-realizada.html']:
    p=base+fn
    h=open(p,encoding='utf-8').read()
    c=h.count(H2)
    h=h.replace(H2,'',1)
    open(p,'w',encoding='utf-8').write(h)
    rest = h.count('Concurso Público - 01/2026 - Prefeitura Municipal de Limeira')
    print(f"{fn}: h2 removido={c} | ocorrencias restantes(concurso)={rest}")

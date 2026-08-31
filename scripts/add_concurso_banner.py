base='/app/frontend/public/'
files=['termos.html','dados-inscricao.html','inscricao.html','confirmacao.html','pagamento-pix.html','inscricao-realizada.html']

# âncora = final exato do cabeçalho av-header (inserido anteriormente)
ANCHOR = """Área do Candidato
</a>
</div>
</div>
</div></div>"""

BANNER = """
<div class="av-cbanner" data-testid="concurso-banner">
<style>
.av-cbanner{max-width:980px;margin:22px auto 0;padding:0 15px;font-family:Arial,Helvetica,sans-serif;box-sizing:border-box}
.av-cbanner *{box-sizing:border-box}
.av-cbanner .av-cb-title{background:linear-gradient(#ededed,#dcdcdc)!important;border:1px solid #d2d2d2;border-bottom:3px solid #cfcfcf;border-radius:6px 6px 0 0;padding:15px 20px;color:#555!important;font-size:18px;font-weight:bold;text-transform:uppercase;letter-spacing:1px}
.av-cbanner .av-cb-card{display:flex;align-items:center;gap:20px;padding:22px 6px 8px;border-bottom:1px solid #eee}
.av-cbanner .av-cb-img{width:98px;height:98px;min-width:98px;border:1px solid #d6d6d6;border-radius:5px;box-shadow:0 3px 0 0 #f5f5f5;display:flex;align-items:center;justify-content:center;background:#fff!important}
.av-cbanner .av-cb-img img{max-height:77px;max-width:92px;display:block}
.av-cbanner .av-cb-dados{flex:1;min-width:0}
.av-cbanner .av-cb-dados .av-cb-tipo{font-size:15px;color:#666!important;margin:0 0 4px}
.av-cbanner .av-cb-dados h2{font-size:26px;letter-spacing:-1px;margin:0 0 8px;color:#403C3B!important;line-height:1.15;font-weight:bold;border:0;padding:0}
.av-cbanner .av-cb-dados .av-cb-periodo{font-size:15px;color:#333!important;margin:0}
@media(max-width:768px){
.av-cbanner .av-cb-card{flex-direction:column;text-align:center}
.av-cbanner .av-cb-dados h2{font-size:20px}
}
</style>
<div class="av-cb-title">Concursos</div>
<div class="av-cb-card">
<div class="av-cb-img"><img src="/limeira-brasao.png" alt="Prefeitura Municipal de Limeira"></div>
<div class="av-cb-dados">
<p class="av-cb-tipo">Concurso Público</p>
<h2>Concurso Público - 01/2026 - PREFEITURA MUNICIPAL DE LIMEIRA</h2>
<p class="av-cb-periodo">Inscrições de <b>31/07/2026</b> a <b>31/08/2026</b></p>
</div>
</div>
</div>"""

for fn in files:
    p=base+fn
    h=open(p,encoding='utf-8').read()
    if 'av-cbanner' in h:
        print(f"{fn}: JA possui banner (skip)"); continue
    c=h.count(ANCHOR)
    if c!=1:
        print(f"{fn}: ANCHOR encontrada {c}x (esperado 1) -- NAO alterado"); continue
    h=h.replace(ANCHOR, ANCHOR+BANNER, 1)
    open(p,'w',encoding='utf-8').write(h)
    print(f"{fn}: banner inserido OK")

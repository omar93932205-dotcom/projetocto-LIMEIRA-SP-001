import re, sys

NEW_HEADER = '''<div id="__cebraspe_topbar_root"><div class="av-header" data-testid="site-header">
<style>
.av-header,.av-footer{font-family:Arial,Helvetica,sans-serif;box-sizing:border-box}
.av-header *,.av-footer *{box-sizing:border-box}
.av-topmenu{background:#333!important}
.av-topmenu ul{max-width:980px;margin:0 auto;padding:0;list-style:none;display:flex;flex-wrap:wrap}
.av-topmenu li{list-style:none}
.av-topmenu a{display:block;padding:10px 15px;color:#fff!important;text-transform:uppercase;font-size:15px;font-weight:normal;text-decoration:none!important}
.av-topmenu a:hover{background:#444!important}
.av-topo{background:#fff!important}
.av-topo .av-conteudo{max-width:980px;margin:0 auto;padding:18px 15px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.av-logo img{max-height:90px;width:auto;display:block}
.av-areacandidato{white-space:nowrap;line-height:1;border-radius:63px;padding:10px 18px 10px 12px;display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:500;background:#000000d6!important;color:#fff!important;text-decoration:none!important}
.av-areacandidato:hover{background:#222!important}
.av-areacandidato svg{width:26px;height:26px}
.av-footer .av-proseleta{background:#fff!important;border-top:1px solid #eee}
.av-footer .av-proseleta .av-conteudo{max-width:980px;margin:0 auto;padding:15px 10px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.av-footer .av-info{font-weight:500;color:#666;font-size:14px}
.av-footer .av-info a{color:#666!important;text-decoration:none!important}
.av-footer .av-info a:hover{text-decoration:underline!important}
.av-footer .av-siteseguro{color:#2e7d32;font-weight:600;font-size:13px}
.av-footer .av-final{background:#f5f5f5!important}
.av-footer .av-final .av-conteudo{max-width:980px;margin:0 auto;padding:12px 10px;text-align:center;font-size:12px;color:#777}
.av-footer .av-final a{color:#777!important;text-decoration:none!important}
@media (max-width:768px){
.av-topmenu ul{justify-content:center}
.av-topmenu a{padding:8px 10px;font-size:12px}
.av-topo .av-conteudo{flex-direction:column;padding:14px 12px;gap:12px}
.av-logo img{max-height:70px}
.av-footer .av-proseleta .av-conteudo{flex-direction:column;text-align:center}
}
</style>
<div class="av-topmenu">
<ul>
<li><a href="#" data-testid="nav-inicio">Início</a></li>
<li><a href="#" data-testid="nav-educacao">Educação Governamental e Legislativa</a></li>
<li><a href="#" data-testid="nav-quem-somos">Quem Somos</a></li>
<li><a href="#" data-testid="nav-fale-conosco">Fale Conosco</a></li>
<li><a href="#" data-testid="nav-orcamentos">Orçamentos</a></li>
</ul>
</div>
<div class="av-topo">
<div class="av-conteudo">
<div class="av-logo"><a href="/inicio.html" data-testid="header-logo-link"><img src="/avanca-logo.jpg" alt="Avança SP"></a></div>
<a class="av-areacandidato" href="#" data-testid="area-candidato-btn">
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.2" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
Área do Candidato
</a>
</div>
</div>
</div></div>'''

NEW_FOOTER = '''<div id="__cebraspe_footer_root"><div class="av-footer" data-testid="site-footer">
<div class="av-proseleta">
<div class="av-conteudo">
<div class="av-info">
<a href="#" data-testid="footer-inicio">Início</a> / <a href="#" data-testid="footer-educacao">Educação Governamental e Legislativa</a> / <a href="#" data-testid="footer-quem-somos">Quem Somos</a> / <a href="#" data-testid="footer-fale-conosco">Fale Conosco</a>
</div>
<div class="av-siteseguro">Site 100% Seguro</div>
</div>
</div>
<div class="av-final">
<div class="av-conteudo">
© AVANÇA SP &middot; Desenvolvido por <a href="#" target="_blank" data-testid="footer-proseleta">ProSeleta - Gestão de Processos Seletivos Online</a>
</div>
</div>
</div></div>'''

TITLES = {
 'termos.html': 'Termos e Condições - Concurso Prefeitura Municipal de Limeira | Avança SP',
 'dados-inscricao.html': 'Dados da Inscrição - Concurso Prefeitura Municipal de Limeira | Avança SP',
 'inscricao.html': 'Inscrição - Concurso Prefeitura Municipal de Limeira | Avança SP',
 'confirmacao.html': 'Confirmação - Concurso Prefeitura Municipal de Limeira | Avança SP',
 'pagamento-pix.html': 'Pagamento PIX - Concurso Prefeitura Municipal de Limeira | Avança SP',
 'inscricao-realizada.html': 'Inscrição Realizada - Concurso Prefeitura Municipal de Limeira | Avança SP',
}

TOPBAR_RE = re.compile(r'<div data-cebraspe-marker="__cebraspe_layout_v1" id="__cebraspe_topbar_root">.*?</section>\s*</div>', re.S)
FOOTER_RE = re.compile(r'<div data-cebraspe-marker="__cebraspe_layout_v1" id="__cebraspe_footer_root">.*?</footer>\s*</div>', re.S)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)

base='/app/frontend/public/'
for fn, title in TITLES.items():
    p = base+fn
    html = open(p,encoding='utf-8').read()
    h, nh = TOPBAR_RE.subn(NEW_HEADER, html, count=1)
    f, nf = FOOTER_RE.subn(NEW_FOOTER, h, count=1)
    t, nt = TITLE_RE.subn(f'<title>{title}</title>', f, count=1)
    open(p,'w',encoding='utf-8').write(t)
    print(f"{fn}: header={nh} footer={nf} title={nt}")

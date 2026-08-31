import re
base='/app/frontend/public/'
files=['termos.html','dados-inscricao.html','inscricao.html','confirmacao.html','pagamento-pix.html','inscricao-realizada.html']

NOVO='Concurso Público - 01/2026 - Prefeitura Municipal de Limeira'
# ordem importa: mais específico primeiro
REPLACEMENTS=[
 ('Concurso Público da Secretaria de Estado de Administração Penitenciária do Maranhão (SEAP_MA_26)', NOVO),
 ('concurso público da Secretaria de Estado de Administração Penitenciária do Maranhão', 'concurso público da Prefeitura Municipal de Limeira'),
 ('Concurso Público da Secretaria de Estado de Administração Penitenciária do Maranhão', NOVO),
 ('Secretaria de Estado de Administração Penitenciária do Maranhão', 'Prefeitura Municipal de Limeira'),
 ('SEAP MA 26 \u2013 ', ''),
 ('001/2026-SEAP-MA', '001/2026'),
 ('CONCURSO PÚBLICO SEAP_MA_26', 'CONCURSO PÚBLICO PREFEITURA DE LIMEIRA'),
 ('CONCURSO PÚBLICO SEAP-MA', 'CONCURSO PÚBLICO PREFEITURA DE LIMEIRA'),
 ('SEAP_MA_26', 'Prefeitura de Limeira'),
 ('SEAP-MA', 'Prefeitura de Limeira'),
 ('SEAP MA 26', 'Prefeitura de Limeira'),
]

for fn in files:
    p=base+fn
    html=open(p,encoding='utf-8').read()
    counts={}
    for old,new in REPLACEMENTS:
        c=html.count(old)
        if c:
            html=html.replace(old,new)
            counts[old[:40]]=c
    open(p,'w',encoding='utf-8').write(html)
    print(f"{fn}: {counts}")

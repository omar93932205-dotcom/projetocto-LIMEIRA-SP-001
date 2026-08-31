import re
base='/app/frontend/public/'
NEW_OG = open('/tmp/optgroups.html',encoding='utf-8').read().strip()

# ---------- dados-inscricao.html ----------
p=base+'dados-inscricao.html'
h=open(p,encoding='utf-8').read()

# 1) substituir optgroups de cargo (SEAP -> Limeira por escolaridade)
h,n1 = re.subn(r'<optgroup label="Inspetor e Monitor">.*?</optgroup>\s*</select>',
               NEW_OG+'\n</select>', h, count=1, flags=re.S)

# 2) UF da prova
h,n2 = re.subn(r'<option value="MA" selected="">Maranhão / MA</option>',
               '<option value="SP" selected="">São Paulo / SP</option>', h, count=1)

# 3) Município da prova
h,n3 = re.subn(r'<option value="São Luís / MA" selected="">São Luís / MA</option>',
               '<option value="LIMEIRA / SP" selected="">LIMEIRA / SP</option>', h, count=1)

# 4) JS que força UF = MA -> SP + comentário
h,n4 = re.subn(r"// Maranhão fixo: pre-seleciona MA \(único estado do certame SEAP MA\)",
               "// São Paulo fixo: pre-seleciona SP (único estado do certame Prefeitura de Limeira)", h, count=1)
h,n5 = re.subn(r"if\(uf\.value !== 'MA'\)\{ uf\.value = 'MA'; \}",
               "if(uf.value !== 'SP'){ uf.value = 'SP'; }", h, count=1)

# 5) fallback de valor 180 -> 98
h,n6 = re.subn(r"__valor: vagaInfo\.valor \|\| 180", "__valor: vagaInfo.valor || 98", h, count=1)

open(p,'w',encoding='utf-8').write(h)
print(f"dados-inscricao: optgroups={n1} uf={n2} mun={n3} coment={n4} jsforce={n5} fallback={n6}")

# ---------- confirmacao.html ----------
p=base+'confirmacao.html'
h=open(p,encoding='utf-8').read()
h,c1 = re.subn(r"\(\{'MA':'Maranhão'\}\[d\.UF_PROVA\]",
               "({'SP':'São Paulo','MA':'Maranhão'}[d.UF_PROVA]", h, count=1)
open(p,'w',encoding='utf-8').write(h)
print(f"confirmacao: uf_map={c1}")

# ---------- pagamento-pix.html ----------
p=base+'pagamento-pix.html'
h=open(p,encoding='utf-8').read()
h,x1 = re.subn(r"if\(!storedValor \|\| storedValor <= 0\)\{ storedValor = 180; \}",
               "if(!storedValor || storedValor <= 0){ storedValor = 98; }", h, count=1)
h,x2 = re.subn(r"// Valor SEMPRE vem do valor real da inscrição \(data-price da vaga\)\. Fallback: 180\.",
               "// Valor SEMPRE vem do valor real da inscrição (data-price da vaga). Fallback: 98.", h, count=1)
open(p,'w',encoding='utf-8').write(h)
print(f"pagamento-pix: fallback={x1} coment={x2}")

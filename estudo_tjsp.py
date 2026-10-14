#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TJ-SP Escrevente — Missão Aprovação (versão gamificada, método Pareto 80/20)

Como usar (sem instalar nada, só Python 3.8+):
    python estudo_tjsp.py              -> abre no navegador (http://127.0.0.1:8765)
    python estudo_tjsp.py --rede       -> libera acesso pelo celular na mesma rede Wi-Fi
Seu progresso fica em 'progresso_tjsp.json' (na mesma pasta). Faça backup desse arquivo.
"""
import json, os, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(PASTA, "progresso_tjsp.json")

TOPICS = json.loads(r'''[{"id": 0, "disc": "Língua Portuguesa", "tema": "PT – Interpretação de textos", "onde": "Textos verbais/não verbais; informações literais, inferências, ponto de vista do autor", "inc": 0.4431, "h": 12, "kw": "interpretação de texto", "eq": 7.0896}, {"id": 1, "disc": "Raciocínio Lógico", "tema": "RL – Teoria dos conjuntos", "onde": "Conjuntos e diagramas de Venn", "inc": 0.6609, "h": 9, "kw": "teoria dos conjuntos", "eq": 4.6263}, {"id": 2, "disc": "Atualidades", "tema": "Atualidades 2025–2026 + Estatuto da Pessoa com Deficiência", "onde": "Fatos de 2025 em diante; Lei 13.146/2015 arts. 1–13 e 34–38", "inc": 1.0, "h": 8, "kw": "atualidades", "eq": 4.0}, {"id": 3, "disc": "Direito Administrativo", "tema": "Adm – Improbidade (Lei 8.429/92)", "onde": "Lei seca: Lei 8.429/92 (atualizada)", "inc": 0.6173, "h": 7, "kw": "improbidade administrativa lei 8.429", "eq": 3.0865}, {"id": 4, "disc": "Informática", "tema": "Info – Internet", "onde": "Navegação, URL, links, sites, busca e impressão", "inc": 0.2706, "h": 6, "kw": "internet navegação url", "eq": 2.4354}, {"id": 5, "disc": "Direito Penal", "tema": "Penal – Funcionário público contra a Administração", "onde": "Lei seca: CP arts. 312–317; 319–327", "inc": 0.4857, "h": 6, "kw": "crimes praticados por funcionário público contra a administração em geral", "eq": 2.4285}, {"id": 6, "disc": "Informática", "tema": "Info – Excel", "onde": "Planilhas, fórmulas, funções, gráficos, classificação", "inc": 0.2535, "h": 5, "kw": "microsoft excel fórmulas funções", "eq": 2.2815}, {"id": 7, "disc": "Informática", "tema": "Info – Word", "onde": "Edição, formatação, tabelas, índices, quebras", "inc": 0.2357, "h": 5, "kw": "microsoft word formatação", "eq": 2.1213}, {"id": 8, "disc": "Direito Constitucional", "tema": "CF – Administração Pública e servidores", "onde": "Lei seca: CF arts. 37–41", "inc": 0.3894, "h": 5, "kw": "administração pública servidores públicos", "eq": 1.947}, {"id": 9, "disc": "Direito Administrativo", "tema": "Adm – Estatuto dos Funcionários (Lei 10.261/68)", "onde": "Lei seca: arts. 1–86; 171–175; 239–323", "inc": 0.3827, "h": 5, "kw": "estatuto dos funcionários públicos civis do estado de são paulo", "eq": 1.9135}, {"id": 10, "disc": "Direito Constitucional", "tema": "CF – Direitos e deveres individuais e coletivos", "onde": "Lei seca: CF art. 5º", "inc": 0.3761, "h": 5, "kw": "direitos e deveres individuais e coletivos art 5", "eq": 1.8805}, {"id": 11, "disc": "Língua Portuguesa", "tema": "PT – Regência e crase", "onde": "Regência verbal e nominal; crase", "inc": 0.0943, "h": 4, "kw": "regência crase", "eq": 1.5088}, {"id": 12, "disc": "Direito Penal", "tema": "Penal – Fé pública", "onde": "Lei seca: CP arts. 293–305; 307; 308; 311-A", "inc": 0.2714, "h": 4, "kw": "crimes contra a fé pública", "eq": 1.357}, {"id": 13, "disc": "Língua Portuguesa", "tema": "PT – Concordância", "onde": "Concordância verbal e nominal", "inc": 0.0817, "h": 4, "kw": "concordância verbal nominal", "eq": 1.3072}, {"id": 14, "disc": "Língua Portuguesa", "tema": "PT – Preposições e conjunções", "onde": "Classes de palavras: preposição e conjunção", "inc": 0.0765, "h": 4, "kw": "preposições conjunções", "eq": 1.224}, {"id": 15, "disc": "Direito Processual Civil", "tema": "PC – Lei 9.099/95 e Lei 12.153/2009", "onde": "Lei seca: Lei 9.099 arts. 3º–19; Lei 12.153/2009", "inc": 0.2391, "h": 4, "kw": "juizados especiais cíveis lei 9.099", "eq": 1.1955}, {"id": 16, "disc": "Direito Processual Civil", "tema": "PC – Comunicação dos atos processuais", "onde": "Lei seca: CPC arts. 188–275", "inc": 0.2391, "h": 4, "kw": "comunicação dos atos processuais citação intimação", "eq": 1.1955}, {"id": 17, "disc": "Informática", "tema": "Info – Correio eletrônico", "onde": "Envio, anexos, preparo de mensagens", "inc": 0.1271, "h": 4, "kw": "correio eletrônico e-mail", "eq": 1.1439}, {"id": 18, "disc": "Legislação Interna e CGJ", "tema": "CGJ – Ofícios de justiça, livros e escrituração", "onde": "Normas da CGJ – Tomo I (seções do edital)", "inc": 0.2286, "h": 4, "kw": "normas corregedoria geral da justiça ofícios de justiça", "eq": 1.143}, {"id": 19, "disc": "Direito Processual Penal", "tema": "PP – Juizados Especiais Criminais", "onde": "Lei seca: Lei 9.099/95 arts. 60–83; 88–89", "inc": 0.2083, "h": 4, "kw": "juizados especiais criminais lei 9.099", "eq": 1.0415}, {"id": 20, "disc": "Língua Portuguesa", "tema": "PT – Pontuação", "onde": "Emprego dos sinais de pontuação", "inc": 0.0628, "h": 4, "kw": "pontuação", "eq": 1.0048}, {"id": 21, "disc": "Legislação Interna e CGJ", "tema": "CGJ – Processo eletrônico e peticionamento", "onde": "Normas da CGJ – Tomo I", "inc": 0.1905, "h": 3, "kw": "corregedoria processo eletrônico peticionamento", "eq": 0.9525}, {"id": 22, "disc": "Língua Portuguesa", "tema": "PT – Pronomes e colocação pronominal", "onde": "Pronomes; colocação pronominal", "inc": 0.0581, "h": 3, "kw": "pronomes colocação pronominal", "eq": 0.9296}, {"id": 23, "disc": "Língua Portuguesa", "tema": "PT – Significação de palavras", "onde": "Significação contextual; sinônimos/antônimos; sentido próprio e figurado", "inc": 0.0572, "h": 3, "kw": "significação contextual sinônimos antônimos", "eq": 0.9152}, {"id": 24, "disc": "Direito Penal", "tema": "Penal – Administração da Justiça", "onde": "Lei seca: CP arts. 339–347; 357; 359", "inc": 0.1714, "h": 3, "kw": "crimes contra a administração da justiça", "eq": 0.857}, {"id": 25, "disc": "Direito Processual Penal", "tema": "PP – Tribunal do Júri", "onde": "Lei seca: CPP arts. 406–497", "inc": 0.1667, "h": 3, "kw": "tribunal do júri", "eq": 0.8335}, {"id": 26, "disc": "Direito Processual Penal", "tema": "PP – Sujeitos processuais", "onde": "Lei seca: CPP arts. 251–258; 261–267; 274", "inc": 0.1528, "h": 3, "kw": "sujeitos processuais auxiliares da justiça", "eq": 0.764}, {"id": 27, "disc": "Direito Processual Penal", "tema": "PP – Habeas corpus", "onde": "Lei seca: CPP arts. 647–667", "inc": 0.1528, "h": 3, "kw": "habeas corpus", "eq": 0.764}, {"id": 28, "disc": "Legislação Interna e CGJ", "tema": "CGJ – Ordem dos serviços, autuação, juntada, certidões", "onde": "Normas da CGJ – Tomo I", "inc": 0.1524, "h": 3, "kw": "corregedoria ordem dos serviços autuação juntada", "eq": 0.762}, {"id": 29, "disc": "Direito Processual Civil", "tema": "PC – Procedimento comum e cumprimento de sentença", "onde": "Lei seca: CPC arts. 318–538", "inc": 0.1522, "h": 3, "kw": "procedimento comum cumprimento de sentença", "eq": 0.761}, {"id": 30, "disc": "Informática", "tema": "Info – Windows 10/11", "onde": "Pastas, arquivos, atalhos, área de transferência", "inc": 0.084, "h": 3, "kw": "windows 10 pastas arquivos", "eq": 0.756}, {"id": 31, "disc": "Língua Portuguesa", "tema": "PT – Verbos", "onde": "Verbo: tempos e modos verbais", "inc": 0.047, "h": 3, "kw": "verbos tempos modos verbais", "eq": 0.752}, {"id": 32, "disc": "Direito Processual Penal", "tema": "PP – Processo comum", "onde": "Lei seca: CPP arts. 394–405; 531–538", "inc": 0.1389, "h": 3, "kw": "processo comum procedimento", "eq": 0.6945}, {"id": 33, "disc": "Matemática", "tema": "Mat – Equações e sistemas", "onde": "Equação 1º e 2º graus; sistemas do 1º grau", "inc": 0.1639, "h": 3, "kw": "equação do 2º grau sistema de equações", "eq": 0.6556}, {"id": 34, "disc": "Direito Processual Civil", "tema": "PC – Auxiliares da Justiça", "onde": "Lei seca: CPC arts. 144–155 (escrivão, chefe de secretaria, oficial de justiça)", "inc": 0.1304, "h": 3, "kw": "auxiliares da justiça escrivão oficial de justiça", "eq": 0.652}, {"id": 35, "disc": "Direito Processual Civil", "tema": "PC – Recursos", "onde": "Lei seca: CPC arts. 994–1026", "inc": 0.1304, "h": 3, "kw": "recursos apelação agravo embargos de declaração", "eq": 0.652}, {"id": 36, "disc": "Raciocínio Lógico", "tema": "RL – Lógicas de argumentação", "onde": "Argumentos válidos/inválidos", "inc": 0.0921, "h": 3, "kw": "lógica de argumentação", "eq": 0.6447}, {"id": 37, "disc": "Direito Constitucional", "tema": "CF – Direitos sociais", "onde": "Lei seca: CF arts. 6º–11", "inc": 0.1239, "h": 3, "kw": "direitos sociais", "eq": 0.6195}, {"id": 38, "disc": "Matemática", "tema": "Mat – Geometria plana", "onde": "Forma, perímetro, área, ângulo, Pitágoras", "inc": 0.1458, "h": 3, "kw": "geometria plana área perímetro", "eq": 0.5832}, {"id": 39, "disc": "Língua Portuguesa", "tema": "PT – Substantivo, adjetivo, artigo, numeral, advérbio", "onde": "Demais classes de palavras", "inc": 0.0359, "h": 3, "kw": "classes de palavras substantivo adjetivo advérbio", "eq": 0.5744}, {"id": 40, "disc": "Legislação Interna e CGJ", "tema": "CGJ – Comunicações, precatórias, intimações e carga", "onde": "Normas da CGJ – Tomo I", "inc": 0.1143, "h": 3, "kw": "corregedoria comunicações oficiais cartas precatórias", "eq": 0.5715}, {"id": 41, "disc": "Legislação Interna e CGJ", "tema": "CGJ – Função correicional", "onde": "Normas da CGJ – Tomo I", "inc": 0.1143, "h": 3, "kw": "função correicional", "eq": 0.5715}, {"id": 42, "disc": "Língua Portuguesa", "tema": "PT – Estruturação do texto e coesão", "onde": "Relações entre ideias; recursos de coesão", "inc": 0.0342, "h": 3, "kw": "coesão estruturação do texto", "eq": 0.5472}, {"id": 43, "disc": "Direito Processual Civil", "tema": "PC – Tutela provisória", "onde": "Lei seca: CPC arts. 294–311", "inc": 0.1087, "h": 3, "kw": "tutela provisória", "eq": 0.5435}, {"id": 44, "disc": "Raciocínio Lógico", "tema": "RL – Equivalências lógicas", "onde": "Equivalências e negações", "inc": 0.0775, "h": 3, "kw": "equivalências lógicas", "eq": 0.5425}, {"id": 45, "disc": "Raciocínio Lógico", "tema": "RL – Raciocínio sequencial", "onde": "Sequências numéricas e figurais", "inc": 0.074, "h": 3, "kw": "raciocínio sequencial", "eq": 0.518}, {"id": 46, "disc": "Matemática", "tema": "Mat – Frações, razão e proporção", "onde": "Frações; razão e proporção; proporcionalidade", "inc": 0.1253, "h": 3, "kw": "razão e proporção frações", "eq": 0.5012}, {"id": 47, "disc": "Direito Constitucional", "tema": "CF – Nacionalidade", "onde": "Lei seca: CF arts. 12–13", "inc": 0.0929, "h": 3, "kw": "nacionalidade", "eq": 0.4645}, {"id": 48, "disc": "Direito Processual Penal", "tema": "PP – Citações e intimações", "onde": "Lei seca: CPP arts. 351–372", "inc": 0.0833, "h": 3, "kw": "citações intimações", "eq": 0.4165}, {"id": 49, "disc": "Direito Processual Penal", "tema": "PP – Recursos", "onde": "Lei seca: CPP arts. 574–646", "inc": 0.0833, "h": 3, "kw": "recursos", "eq": 0.4165}, {"id": 50, "disc": "Matemática", "tema": "Mat – Porcentagem", "onde": "Porcentagem", "inc": 0.1038, "h": 3, "kw": "porcentagem", "eq": 0.4152}, {"id": 51, "disc": "Direito Penal", "tema": "Penal – Particular contra a Administração", "onde": "Lei seca: CP arts. 328–333; 336; 337", "inc": 0.0714, "h": 3, "kw": "crimes praticados por particular contra a administração em geral", "eq": 0.357}, {"id": 52, "disc": "Matemática", "tema": "Mat – Regra de três", "onde": "Regra de três simples e composta", "inc": 0.0813, "h": 2, "kw": "regra de três", "eq": 0.3252}, {"id": 53, "disc": "Matemática", "tema": "Mat – MMC e MDC", "onde": "Múltiplos e divisores; MMC e MDC", "inc": 0.0794, "h": 2, "kw": "mmc mdc", "eq": 0.3176}, {"id": 54, "disc": "Raciocínio Lógico", "tema": "RL – Problemas de lógica", "onde": "Relações arbitrárias entre pessoas, lugares, coisas", "inc": 0.0448, "h": 2, "kw": "problemas de lógica", "eq": 0.3136}, {"id": 55, "disc": "Matemática", "tema": "Mat – Tabelas e gráficos", "onde": "Relação entre grandezas: tabelas e gráficos", "inc": 0.0747, "h": 2, "kw": "tabelas e gráficos grandezas", "eq": 0.2988}, {"id": 56, "disc": "Matemática", "tema": "Mat – Médias", "onde": "Média aritmética simples e ponderada", "inc": 0.0718, "h": 2, "kw": "média aritmética ponderada", "eq": 0.2872}, {"id": 57, "disc": "Raciocínio Lógico", "tema": "RL – Diagramas lógicos", "onde": "Diagramas lógicos", "inc": 0.0379, "h": 2, "kw": "diagramas lógicos", "eq": 0.2653}, {"id": 58, "disc": "Legislação Interna e CGJ", "tema": "Res. TJSP 850/2021 – Teletrabalho", "onde": "Resolução TJSP 850/2021", "inc": 0.05, "h": 2, "kw": "resolução 850/2021 teletrabalho tjsp", "eq": 0.25}, {"id": 59, "disc": "Legislação Interna e CGJ", "tema": "Res. TJSP 963/2025 – eproc", "onde": "Resolução TJSP 963/2025", "inc": 0.05, "h": 2, "kw": "resolução 963/2025 eproc tjsp", "eq": 0.25}, {"id": 60, "disc": "Legislação Interna e CGJ", "tema": "LC 1.111/2010 – Plano de Cargos e Carreiras", "onde": "Lei Complementar 1.111/2010", "inc": 0.05, "h": 2, "kw": "lei complementar 1.111/2010 tjsp", "eq": 0.25}, {"id": 61, "disc": "Legislação Interna e CGJ", "tema": "Regimento Interno do TJSP", "onde": "Regimento Interno do Tribunal de Justiça", "inc": 0.05, "h": 2, "kw": "regimento interno tjsp", "eq": 0.25}, {"id": 62, "disc": "Informática", "tema": "Info – Busca e pesquisa", "onde": "Busca e pesquisa na internet", "inc": 0.0238, "h": 2, "kw": "busca e pesquisa internet", "eq": 0.2142}, {"id": 63, "disc": "Matemática", "tema": "Mat – Geometria espacial", "onde": "Volume e sólidos", "inc": 0.0516, "h": 2, "kw": "geometria espacial volume", "eq": 0.2064}, {"id": 64, "disc": "Matemática", "tema": "Mat – Medidas", "onde": "Sistemas de medidas usuais", "inc": 0.0484, "h": 2, "kw": "sistema de medidas unidades", "eq": 0.1936}, {"id": 65, "disc": "Língua Portuguesa", "tema": "PT – Correlação e vozes verbais", "onde": "Correlação verbal; vozes verbais", "inc": 0.0093, "h": 2, "kw": "vozes verbais", "eq": 0.1488}, {"id": 66, "disc": "Matemática", "tema": "Mat – Operações básicas", "onde": "Operações com reais; potenciação e radiciação", "inc": 0.0354, "h": 2, "kw": "potenciação radiciação operações", "eq": 0.1416}, {"id": 67, "disc": "Raciocínio Lógico", "tema": "RL – Estruturas lógicas", "onde": "Proposições e conectivos", "inc": 0.0112, "h": 2, "kw": "estruturas lógicas proposições", "eq": 0.0784}, {"id": 68, "disc": "Matemática", "tema": "Mat – Juros simples", "onde": "Juros simples", "inc": 0.0187, "h": 2, "kw": "juros simples", "eq": 0.0748}, {"id": 69, "disc": "Direito Processual Penal", "tema": "PP – Restauração de autos", "onde": "Lei seca: CPP arts. 541–548", "inc": 0.0139, "h": 2, "kw": "restauração de autos extraviados", "eq": 0.0695}, {"id": 70, "disc": "Direito Constitucional", "tema": "CF – Poder Judiciário (art. 92)", "onde": "Lei seca: CF art. 92", "inc": 0.0133, "h": 2, "kw": "poder judiciário disposições gerais", "eq": 0.0665}, {"id": 71, "disc": "Informática", "tema": "Info – OneDrive e Teams", "onde": "OneDrive, Teams, SharePoint, OneNote", "inc": 0.0052, "h": 2, "kw": "onedrive teams microsoft 365", "eq": 0.0468}, {"id": 72, "disc": "Direito Constitucional", "tema": "CF – Teoria geral dos direitos fundamentais", "onde": "CF Título II – noções gerais", "inc": 0.0044, "h": 2, "kw": "direitos fundamentais teoria geral", "eq": 0.022}, {"id": 73, "disc": "Raciocínio Lógico", "tema": "RL – Princípio da casa dos pombos", "onde": "Casa dos pombos", "inc": 0.0017, "h": 2, "kw": "princípio da casa dos pombos", "eq": 0.0119}]''')
DISC_W = json.loads(r'''{"Língua Portuguesa": 16, "Direito Penal": 5, "Direito Processual Penal": 5, "Direito Processual Civil": 5, "Direito Constitucional": 5, "Direito Administrativo": 5, "Legislação Interna e CGJ": 5, "Matemática": 4, "Informática": 9, "Raciocínio Lógico": 7, "Atualidades": 4}''')

HTML = r'''<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Missão Aprovação · TJ-SP Escrevente</title>
<style>
:root{--bg:#0b1020;--card:#151c33;--card2:#1b2442;--line:#2a3558;--tx:#e8ecff;--mut:#8f9bc4;
--a:#7c5cff;--b:#22d3ee;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;--gold:#fcd34d}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 600px at 10% -10%,#26205a 0,transparent 60%),radial-gradient(900px 500px at 100% 0,#0e3a4a 0,transparent 55%),var(--bg);
color:var(--tx);font:15px/1.45 "Segoe UI",system-ui,Arial,sans-serif;min-height:100vh}
.wrap{max-width:1100px;margin:0 auto;padding:14px 14px 90px}
header{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.logo{font-weight:800;font-size:20px;letter-spacing:.3px}.logo span{background:linear-gradient(90deg,var(--a),var(--b));-webkit-background-clip:text;background-clip:text;color:transparent}
.hud{flex:1;min-width:260px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:10px 14px}
.hudtop{display:flex;justify-content:space-between;font-size:13px;color:var(--mut)}.hudtop b{color:var(--tx)}
.xpbar{height:12px;background:#0d1328;border-radius:99px;overflow:hidden;margin-top:6px;border:1px solid var(--line)}
.xpbar i{display:block;height:100%;background:linear-gradient(90deg,var(--a),var(--b));box-shadow:0 0 14px var(--a);transition:width .6s}
.chips{display:flex;gap:8px;flex-wrap:wrap}.chip{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:6px 10px;font-size:13px}
.chip b{font-size:16px}
nav{position:fixed;bottom:0;left:0;right:0;background:rgba(11,16,32,.94);backdrop-filter:blur(8px);border-top:1px solid var(--line);display:flex;gap:2px;padding:6px;z-index:20;overflow-x:auto}nav button:first-child{margin-left:auto}nav button:last-child{margin-right:auto}
nav button{background:none;border:0;color:var(--mut);padding:8px 9px;border-radius:12px;font:600 12.5px inherit;cursor:pointer;white-space:nowrap}
nav button.on{background:linear-gradient(135deg,var(--a),#4f46e5);color:#fff;box-shadow:0 4px 18px rgba(124,92,255,.45)}
.grid{display:grid;gap:12px}.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.card{background:linear-gradient(180deg,var(--card2),var(--card));border:1px solid var(--line);border-radius:18px;padding:16px}
.card h3{margin:0 0 10px;font-size:15px;color:var(--mut);font-weight:700;text-transform:uppercase;letter-spacing:.8px}
.hero{border:1px solid #4a3ec2;background:linear-gradient(135deg,#2a2070 0,#143d57 100%);box-shadow:0 10px 40px rgba(76,61,200,.3)}
.hero .tag{display:inline-block;font-size:12px;font-weight:700;padding:3px 10px;border-radius:99px;background:rgba(255,255,255,.14);margin-right:6px}
.hero h2{margin:10px 0 4px;font-size:26px;line-height:1.15}.hero p{margin:0;color:#c8d0f5}
.btn{border:0;border-radius:12px;padding:10px 16px;font:700 14px inherit;cursor:pointer;color:#fff;background:linear-gradient(135deg,var(--a),#4f46e5);text-decoration:none;display:inline-block}
.btn.ok{background:linear-gradient(135deg,#10b981,#059669)}.btn.ghost{background:#1f2a4d;border:1px solid var(--line)}.btn.sm{padding:6px 10px;font-size:12px}
.btn:active{transform:scale(.97)}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.ring{position:relative;width:120px;height:120px}.ring span{position:absolute;inset:0;display:grid;place-items:center;text-align:center;font-weight:800;font-size:20px}
.ring small{display:block;font-size:11px;color:var(--mut);font-weight:600}
table{width:100%;border-collapse:collapse;font-size:13px}th{color:var(--mut);text-align:left;font-weight:600;padding:6px;position:sticky;top:0;background:var(--card)}
td{padding:7px 6px;border-top:1px solid var(--line);vertical-align:middle}tr.done td{opacity:.55}tr.next td{background:rgba(124,92,255,.16)}
.st{display:inline-block;min-width:92px;text-align:center;padding:4px 8px;border-radius:99px;font-weight:700;font-size:12px;cursor:pointer;user-select:none;border:1px solid var(--line)}
.st.P{background:#1f2a4d;color:var(--mut)}.st.E{background:#4a3a0a;color:var(--warn);border-color:#7a5f10}.st.C{background:#0b3d2e;color:var(--ok);border-color:#136b50}
.ph1{color:var(--gold)}.ph2{color:var(--mut)}
.bar{height:10px;background:#0d1328;border-radius:99px;position:relative;border:1px solid var(--line);overflow:visible}
.bar i{display:block;height:100%;border-radius:99px}.bar u{position:absolute;top:-4px;bottom:-4px;width:2px;background:var(--gold)}
input,select{background:#0d1328;border:1px solid var(--line);color:var(--tx);border-radius:10px;padding:9px;font:inherit;width:100%}
label{font-size:12px;color:var(--mut);display:block;margin:6px 0 3px}
.f3{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px}
.badge{display:flex;gap:10px;align-items:center;padding:10px;border-radius:14px;border:1px solid var(--line);background:#12193a}
.badge.off{filter:grayscale(1);opacity:.45}.badge .ic{font-size:28px}.badge b{display:block}.badge small{color:var(--mut)}
.muted{color:var(--mut)}.small{font-size:12px}.good{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}
#toast{position:fixed;left:50%;top:18px;transform:translateX(-50%) translateY(-90px);background:linear-gradient(135deg,var(--a),var(--b));color:#fff;padding:12px 20px;border-radius:14px;font-weight:800;z-index:50;transition:transform .35s;box-shadow:0 10px 30px rgba(0,0,0,.4)}
#toast.on{transform:translateX(-50%) translateY(0)}
canvas#fx{position:fixed;inset:0;pointer-events:none;z-index:40}
.scroll{max-height:560px;overflow:auto;border-radius:12px}
a.lk{color:var(--b);text-decoration:none;font-weight:700}
</style></head><body>
<canvas id="fx"></canvas><div id="toast"></div>
<div class="wrap">
<header><div class="logo">🎯 Missão <span>Aprovação</span><div class="muted small" style="font-weight:500">TJ-SP · Escrevente · Vunesp</div></div>
<div class="hud" id="hud"></div></header>
<div id="app"></div></div>
<nav id="nav"></nav>
<script>
const TOPICS=__TOPICS_JS__, DISCW=__DISCW_JS__;
const TABS=[["hoje","🏠 Hoje"],["plano","🗺️ Plano"],["pareto","📊 Pareto"],["questoes","✍️ Questões"],["redacao","📝 Redação"],["conq","🏆 Conquistas"]];
let S=null,tab="hoje",filt="Todas";
const $=s=>document.querySelector(s);
const todayStr=()=>new Date().toLocaleDateString("sv-SE");
const addDays=(d,n)=>{const x=new Date(d+"T12:00:00");x.setDate(x.getDate()+n);return x.toLocaleDateString("sv-SE")};
const fmtD=d=>d?d.split("-").reverse().slice(0,2).join("/"):"";
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const mondayOf=d=>{const x=new Date(d+"T12:00:00");const k=(x.getDay()+6)%7;x.setDate(x.getDate()-k);return x.toLocaleDateString("sv-SE")};
const pct=x=>Math.round(x*100)+"%";

// ---- Pareto: fase 1 = temas que somam 80% das questões esperadas
const TOTAL_EQ=TOPICS.reduce((a,t)=>a+t.eq,0);
let cum=0;TOPICS.forEach(t=>{cum+=t.eq;t.cum=cum/TOTAL_EQ;t.phase=(cum-t.eq)/TOTAL_EQ<0.8?1:2;});
const P1=TOPICS.filter(t=>t.phase==1),P1H=P1.reduce((a,t)=>a+t.h,0),ALLH=TOPICS.reduce((a,t)=>a+t.h,0);
const DISCS=Object.keys(DISCW);

async function load(){const r=await fetch("/api/state");S=await r.json();
 if(!S.start){S={start:todayStr(),set:{meta:85,hdia:4,minq:20},st:{},done:{},rev:{},log:[],ess:[]};save();}
 render();}
let tmr;function save(){clearTimeout(tmr);tmr=setTimeout(()=>fetch("/api/state",{method:"POST",body:JSON.stringify(S)}),150);}
const META=()=>S.set.meta/100;

// ---- cálculos
function tStats(id){let q=0,a=0;S.log.forEach(l=>{if(l.t===id){q+=l.q;a+=l.a}});return{q,a,acc:q?a/q:null}}
function dStats(d){let q=0,a=0;S.log.forEach(l=>{if(TOPICS[l.t]&&TOPICS[l.t].disc===d){q+=l.q;a+=l.a}});return{q,a,acc:q?a/q:null}}
const isDone=id=>S.st[id]==="C";
function topicXP(t){if(!isDone(t.id))return 0;const s=tStats(t.id);return 100+((s.q>=S.set.minq&&s.acc>=META())?100:0)}
function revCount(){let n=0;for(const k in S.rev)for(const d of ["d1","d7","d30"])if(S.rev[k][d])n++;return n}
function hoursTotal(){return S.log.reduce((a,l)=>a+(l.h||0),0)}
function xpTotal(){let x=0;TOPICS.forEach(t=>x+=topicXP(t));S.log.forEach(l=>{x+=l.q+l.a+Math.round((l.h||0)*20)});x+=revCount()*30+S.ess.length*80;return x}
const LEVELS=["Calouro","Aprendiz","Concurseiro","Veterano","Estrategista","Mestre da Lei Seca","Escrevente"];
function lvl(x){const L=Math.floor(x/500)+1;return{L,name:LEVELS[Math.min(L-1,LEVELS.length-1)],cur:x%500}}
function daysActive(){const s=new Set(S.log.map(l=>l.d));Object.values(S.done).forEach(d=>s.add(d));S.ess.forEach(e=>s.add(e.d));return s}
function streak(){const s=daysActive();let d=todayStr(),n=0;if(!s.has(d))d=addDays(d,-1);while(s.has(d)){n++;d=addDays(d,-1)}return n}
const hoursOn=d=>S.log.filter(l=>l.d===d).reduce((a,l)=>a+(l.h||0),0);
function nextTopics(n){return TOPICS.filter(t=>!isDone(t.id)).slice(0,n)}
function reviewsDue(){const out=[],td=todayStr();TOPICS.forEach(t=>{if(!isDone(t.id)||!S.done[t.id])return;[[1,"d1"],[7,"d7"],[30,"d30"]].forEach(([k,f])=>{const due=addDays(S.done[t.id],k);if(due<=td&&!(S.rev[t.id]&&S.rev[t.id][f]))out.push({t,k,f,due})})});return out.slice(0,8)}
function pareto80(){const dn=TOPICS.filter(t=>isDone(t.id)).reduce((a,t)=>a+t.eq,0)/TOTAL_EQ;return dn}
function projected(){let num=0,den=0;DISCS.forEach(d=>{const s=dStats(d);if(s.q){num+=DISCW[d]*s.acc;den+=DISCW[d]}});return den?num/den*10:null}
const qcLink=t=>"https://www.google.com/search?q="+encodeURIComponent("site:qconcursos.com vunesp "+t.disc+" "+t.kw);
function weekEnd(){return addDays(mondayOf(todayStr()),6)}

// ---- UI helpers
function toast(m){const t=$("#toast");t.textContent=m;t.classList.add("on");setTimeout(()=>t.classList.remove("on"),2400)}
const fx=$("#fx"),cx=fx.getContext("2d");let parts=[];
function boom(){fx.width=innerWidth;fx.height=innerHeight;for(let i=0;i<140;i++)parts.push({x:innerWidth/2,y:innerHeight/3,vx:(Math.random()-.5)*14,vy:Math.random()*-12-3,c:`hsl(${Math.random()*360},90%,60%)`,l:90,s:Math.random()*6+3});anim()}
function anim(){cx.clearRect(0,0,fx.width,fx.height);parts.forEach(p=>{p.x+=p.vx;p.y+=p.vy;p.vy+=.35;p.l--;cx.fillStyle=p.c;cx.fillRect(p.x,p.y,p.s,p.s)});parts=parts.filter(p=>p.l>0);if(parts.length)requestAnimationFrame(anim);else cx.clearRect(0,0,fx.width,fx.height)}
function ring(v,max,color){const r=50,c=2*Math.PI*r,f=Math.min(1,v/max);return `<svg viewBox="0 0 120 120" width="120" height="120"><circle cx="60" cy="60" r="${r}" stroke="#0d1328" stroke-width="12" fill="none"/><circle cx="60" cy="60" r="${r}" stroke="${color}" stroke-width="12" fill="none" stroke-linecap="round" stroke-dasharray="${c*f} ${c}" transform="rotate(-90 60 60)"/></svg>`}

function hud(){const x=xpTotal(),l=lvl(x);$("#hud").innerHTML=`<div class="hudtop"><span>Nível <b>${l.L}</b> · ${l.name}</span><span><b>${x}</b> XP · faltam ${500-l.cur} p/ subir</span></div><div class="xpbar"><i style="width:${l.cur/5}%"></i></div>
<div class="chips" style="margin-top:8px"><div class="chip">🔥 <b>${streak()}</b> dias seguidos</div><div class="chip">✅ <b>${TOPICS.filter(t=>isDone(t.id)).length}</b>/${TOPICS.length} temas</div><div class="chip">📈 Pareto <b>${pct(pareto80()/0.8>1?1:pareto80())}</b> da prova</div></div>`}

function setStatus(id,v){const was=S.st[id];S.st[id]=v;if(v==="C"&&was!=="C"){S.done[id]=todayStr();const t=TOPICS[id];boom();toast("🎉 Tema concluído! +100 XP");
 if(t.phase==1&&P1.every(p=>isDone(p.id)))setTimeout(()=>toast("🏆 NÚCLEO PARETO COMPLETO! 80% da prova coberta"),2600)}
 if(v!=="C"&&was==="C"){delete S.done[id]}save();render()}
function cycle(id){const o={P:"E",E:"C",C:"P"};setStatus(id,o[S.st[id]||"P"])}

// ---- views
function vHoje(){const n=nextTopics(5),t=n[0],h=hoursOn(todayStr()),dn=reviewsDue();
 const wkDone=S.ess.some(e=>e.d>=mondayOf(todayStr()));
 const hero=t?`<div class="card hero"><span class="tag">${t.phase==1?"⭐ NÚCLEO PARETO":"Cauda (20%)"}</span><span class="tag">${esc(t.disc)}</span><span class="tag">~${t.h}h</span>
 <h2>${esc(t.tema)}</h2><p>${esc(t.onde)}</p><p class="small" style="margin-top:6px">Vale ~${t.eq.toFixed(2)} questão(ões) esperada(s) na prova · acumulado Pareto: ${pct(t.cum)}</p>
 <div class="row" style="margin-top:14px"><button class="btn ok" onclick="setStatus(${t.id},'C')">✔ Concluir tema</button><button class="btn ghost" onclick="setStatus(${t.id},'E')">📖 Estou estudando</button>
 <a class="btn ghost" target="_blank" href="${qcLink(t)}">🔎 Questões Vunesp (QConcursos)</a></div></div>`:`<div class="card hero"><h2>🏁 Plano 100% concluído!</h2><p>Agora é revisão e simulados.</p></div>`;
 const r=dn.length?dn.map(d=>`<div class="row" style="justify-content:space-between;border-top:1px solid var(--line);padding:6px 0"><span>🔁 <b>R${d.k}d</b> · ${esc(d.t.tema)}</span><button class="btn sm ok" onclick="doRev(${d.t.id},'${d.f}')">Feita</button></div>`).join(""):`<div class="muted">Nenhuma revisão pendente. 👌</div>`;
 const q=n.slice(1).map(x=>`<tr><td class="${x.phase==1?"ph1":"ph2"}">${x.phase==1?"⭐":"•"}</td><td>${esc(x.tema)}<div class="small muted">${esc(x.disc)}</div></td><td>${x.h}h</td></tr>`).join("");
 return `<div class="grid">${hero}<div class="grid g2">
 <div class="card"><h3>Meta de hoje</h3><div class="row" style="gap:16px"><div class="ring">${ring(h,S.set.hdia,"var(--b)")}<span><div>${h.toFixed(1)}h<small>de ${S.set.hdia}h</small></div></span></div>
 <div style="flex:1;min-width:150px"><div class="muted small">Registrar tempo estudado</div><div class="row"><input id="hh" type="number" step="0.5" min="0" placeholder="horas" style="width:90px"><button class="btn sm" onclick="addH()">+ horas</button></div>
 <div class="row" style="margin-top:8px"><button class="btn sm ghost" id="pbtn" onclick="pomo()">⏱ Foco 50 min</button><span id="pt" class="muted small"></span></div></div></div></div>
 <div class="card"><h3>Redação da semana</h3>${wkDone?`<div class="good"><b>✔ Feita!</b> Boa. Próxima a partir de ${fmtD(addDays(mondayOf(todayStr()),7))}.</div>`:`<div class="warn"><b>Ainda não fez essa semana.</b></div><div class="muted small">Reserve ~${4}h. Vence ${fmtD(weekEnd())}.</div><button class="btn sm" style="margin-top:8px" onclick="go('redacao')">Registrar redação</button>`}</div>
 <div class="card"><h3>Revisões de hoje</h3>${r}</div>
 <div class="card"><h3>Fila</h3><table>${q||"<tr><td class=muted>Fila vazia</td></tr>"}</table></div></div></div>`}
function addH(){const v=parseFloat($("#hh").value);if(!(v>0))return;S.log.push({d:todayStr(),t:null,q:0,a:0,h:v});save();toast(`+${Math.round(v*20)} XP por foco!`);render()}
let pint=null,psec=0;function pomo(){if(pint){clearInterval(pint);pint=null;$("#pbtn").textContent="⏱ Foco 50 min";$("#pt").textContent="";return}
 psec=50*60;$("#pbtn").textContent="⏸ Parar";pint=setInterval(()=>{psec--;const el=$("#pt");if(el)el.textContent=String(Math.floor(psec/60)).padStart(2,"0")+":"+String(psec%60).padStart(2,"0");
 if(psec<=0){clearInterval(pint);pint=null;S.log.push({d:todayStr(),t:null,q:0,a:0,h:50/60});save();boom();toast("⏱ 50 min de foco! +17 XP");render()}},1000)}
function doRev(id,f){S.rev[id]=S.rev[id]||{};S.rev[id][f]=true;save();toast("🔁 Revisão feita! +30 XP");render()}

function vPlano(){const base=S.start,wk=S.set.hdia*7-4;
 const opts=["Todas",...DISCS].map(d=>`<option ${d===filt?"selected":""}>${esc(d)}</option>`).join("");let c=0;
 const rows=TOPICS.map(t=>{c+=t.h;const s=tStats(t.id),nx=nextTopics(1)[0];const due=addDays(base,Math.ceil(c/wk*7)-1);
 if(filt!=="Todas"&&t.disc!==filt)return"";const st=S.st[t.id]||"P";const m=s.q>=S.set.minq?(s.acc>=META()?'<span class="good">✔ meta</span>':'<span class="bad">abaixo</span>'):'<span class="muted">—</span>';
 return `<tr class="${st==="C"?"done":""} ${nx&&nx.id===t.id?"next":""}"><td class="${t.phase==1?"ph1":"ph2"}">${t.phase==1?"⭐":"•"}</td><td>${esc(t.tema)}<div class="small muted">${esc(t.disc)} · ${esc(t.onde)}</div></td><td>${t.h}h</td><td><span class="st ${st}" onclick="cycle(${t.id})">${{P:"Pendente",E:"Estudando",C:"✔ Concluído"}[st]}</span></td><td>${s.q?pct(s.acc)+" <span class=muted>("+s.q+")</span>":""} ${m}</td><td class="muted">${fmtD(due)}</td><td><a class="lk" target="_blank" href="${qcLink(t)}">🔎</a></td></tr>`}).join("");
 return `<div class="card"><div class="row" style="justify-content:space-between"><h3 style="margin:0">Plano completo</h3><select style="width:auto" onchange="filt=this.value;render()">${opts}</select></div>
 <p class="muted small">⭐ = núcleo Pareto (80% da prova, ${P1.length} temas, ~${P1H}h). Clique no status para avançar: Pendente → Estudando → Concluído. Datas previstas: ${S.set.hdia}h/dia, 1 sessão de redação por semana.</p>
 <div class="scroll"><table><tr><th></th><th>Tema</th><th>Horas</th><th>Status</th><th>Acerto</th><th>Previsto</th><th>QC</th></tr>${rows}</table></div></div>`}

function vPareto(){const W=1000,H=300,pl=40,pb=20,n=TOPICS.length,bw=(W-pl)/n,mx=Math.max(...TOPICS.map(t=>t.eq));let bars="",line="";
 TOPICS.forEach((t,i)=>{const x=pl+i*bw,h=(t.eq/mx)*(H-pb-20),col=isDone(t.id)?"#34d399":(t.phase==1?"#fcd34d":"#5b6794");
 bars+=`<rect x="${x+1}" y="${H-pb-h}" width="${bw-2}" height="${h}" fill="${col}" rx="2"><title>${esc(t.tema)} · ${t.eq.toFixed(2)} q. esperadas · acum. ${pct(t.cum)}</title></rect>`;
 line+=(i?"L":"M")+(x+bw/2)+","+(H-pb-t.cum*(H-pb-20))});
 const y80=H-pb-0.8*(H-pb-20);
 const svg=`<svg viewBox="0 0 ${W} ${H}" style="width:100%"><line x1="${pl}" x2="${W}" y1="${y80}" y2="${y80}" stroke="#f87171" stroke-dasharray="6 5"/><text x="${pl+4}" y="${y80-5}" fill="#f87171" font-size="12">80%</text>${bars}<path d="${line}" stroke="#22d3ee" stroke-width="2.5" fill="none"/></svg>`;
 const per=DISCS.map(d=>{const ts=TOPICS.filter(t=>t.disc===d),p1=ts.filter(t=>t.phase==1).length;const e=ts.reduce((a,t)=>a+t.eq,0);return `<tr><td>${esc(d)}</td><td>${DISCW[d]}</td><td>${ts.length}</td><td>${p1}</td><td>${(e/TOTAL_EQ*100).toFixed(0)}%</td></tr>`}).join("");
 return `<div class="grid"><div class="card"><h3>Curva de Pareto · onde estão os pontos</h3>${svg}
 <p class="small muted">Barras = questões esperadas por tema (peso da disciplina no edital × incidência Vunesp 2015–2024, E-book Estratégia). Linha azul = acumulado. <span style="color:#fcd34d">Amarelo</span> = núcleo Pareto · <span style="color:#34d399">verde</span> = concluído · cinza = cauda.</p></div>
 <div class="grid g2"><div class="card"><h3>Regra de ouro</h3><p><b>${P1.length} de ${TOPICS.length} temas</b> (~${P1H}h de ${ALLH}h) cobrem <b>80%</b> das questões esperadas.</p><p class="muted">Estratégia: (1) zere o núcleo ⭐ chegando a 85% de acerto em cada tema; (2) só então faça a cauda; (3) revise com as datas de 24h/7d/30d. Como a nota mínima é 5,0 e Português e Direito têm corte de 50%, o núcleo sozinho já te leva bem acima do corte.</p>
 <div class="bar" style="margin-top:10px"><i style="width:${Math.min(100,pareto80()/0.8*100)}%;background:linear-gradient(90deg,var(--a),var(--b))"></i></div><div class="small muted" style="margin-top:4px">Progresso do núcleo: ${Math.round(Math.min(1,pareto80()/0.8)*100)}%</div></div>
 <div class="card"><h3>Por disciplina</h3><table><tr><th>Disciplina</th><th>Qts prova</th><th>Temas</th><th>No núcleo</th><th>% pontos</th></tr>${per}</table></div></div></div>`}

function vQuest(){const opts=TOPICS.map(t=>`<option value="${t.id}">${esc(t.tema)}</option>`).join("");
 const bars=DISCS.map(d=>{const s=dStats(d),w=s.q?s.acc*100:0,col=!s.q?"#334":(s.acc>=META()?"var(--ok)":s.acc>=.7?"var(--warn)":"var(--bad)");
 return `<div style="margin:9px 0"><div class="row" style="justify-content:space-between"><span>${esc(d)}</span><span class="small muted">${s.q?pct(s.acc)+" · "+s.q+" q.":"sem dados"}</span></div><div class="bar"><i style="width:${w}%;background:${col}"></i><u style="left:${S.set.meta}%"></u></div></div>`}).join("");
 const pj=projected(),tq=S.log.reduce((a,l)=>a+l.q,0),ta=S.log.reduce((a,l)=>a+l.a,0);
 const last=S.log.filter(l=>l.q).slice(-8).reverse().map(l=>`<tr><td>${fmtD(l.d)}</td><td>${esc(TOPICS[l.t].tema)}</td><td>${l.a}/${l.q}</td><td>${pct(l.a/l.q)}</td></tr>`).join("");
 const weeks=[];for(let i=7;i>=0;i--){const a=addDays(mondayOf(todayStr()),-7*i),b=addDays(a,6);let q=0,k=0;S.log.forEach(l=>{if(l.d>=a&&l.d<=b){q+=l.q;k+=l.a}});weeks.push({a,q,acc:q?k/q:0})}
 const mq=Math.max(1,...weeks.map(w=>w.q)),wsv=weeks.map((w,i)=>`<rect x="${i*50+8}" y="${90-w.q/mq*80}" width="34" height="${w.q/mq*80}" fill="#7c5cff" rx="4"/><text x="${i*50+25}" y="104" fill="#8f9bc4" font-size="10" text-anchor="middle">${fmtD(w.a)}</text><text x="${i*50+25}" y="${86-w.q/mq*80}" fill="#e8ecff" font-size="10" text-anchor="middle">${w.q?pct(w.acc):""}</text>`).join("");
 return `<div class="grid g2"><div class="card"><h3>Registrar sessão</h3><label>Tema</label><select id="qt">${opts}</select><div class="f3"><div><label>Questões</label><input id="qq" type="number" min="0"></div><div><label>Acertos</label><input id="qa" type="number" min="0"></div><div><label>Horas</label><input id="qh" type="number" step="0.5" min="0"></div></div>
 <div class="row" style="margin-top:10px"><button class="btn" onclick="addQ()">Salvar (+XP)</button><a class="btn ghost" target="_blank" id="qlk" href="#" onclick="this.href=qcLink(TOPICS[+$('#qt').value])">🔎 Buscar questões</a></div></div>
 <div class="card"><h3>Acerto vs meta (${S.set.meta}%)</h3>${bars}<div class="small muted">Total: ${ta}/${tq} ${tq?"("+pct(ta/tq)+")":""} · Nota projetada: <b>${pj==null?"—":pj.toFixed(1)}</b>/10 (mín. 5,0)</div></div>
 <div class="card"><h3>Questões por semana (e % de acerto)</h3><svg viewBox="0 0 410 110" style="width:100%">${wsv}</svg></div>
 <div class="card"><h3>Últimas sessões</h3><table>${last||"<tr><td class=muted>Nada ainda</td></tr>"}</table></div></div>`}
function addQ(){const t=+$("#qt").value,q=+$("#qq").value||0,a=+$("#qa").value||0,h=+$("#qh").value||0;if(a>q){toast("Acertos > questões 🤔");return}
 if(!q&&!h)return;S.log.push({d:todayStr(),t,q,a,h});save();toast(`+${q+a+Math.round(h*20)} XP`);render()}

function vRed(){const hist=S.ess.slice().reverse().map(e=>`<tr><td>${fmtD(e.d)}</td><td>${esc(e.tema||"")}</td><td>${e.s.join(" / ")}</td><td><b>${e.tot}</b>/40</td><td>${e.tot>=0.85*40?'<span class="good">meta</span>':e.tot>=20?'<span class="warn">aprovada</span>':'<span class="bad">&lt;20</span>'}</td></tr>`).join("");
 const pts=S.ess.slice(-12),W=400,sv=pts.length?`<svg viewBox="0 0 ${W} 120" style="width:100%"><line x1="0" x2="${W}" y1="${120-34/40*110}" y2="${120-34/40*110}" stroke="#fcd34d" stroke-dasharray="5 4"/><line x1="0" x2="${W}" y1="${120-20/40*110}" y2="${120-20/40*110}" stroke="#f87171" stroke-dasharray="5 4"/><polyline fill="none" stroke="#22d3ee" stroke-width="3" points="${pts.map((e,i)=>(20+i*(W-40)/Math.max(1,pts.length-1))+","+(120-e.tot/40*110)).join(" ")}"/>${pts.map((e,i)=>`<circle cx="${20+i*(W-40)/Math.max(1,pts.length-1)}" cy="${120-e.tot/40*110}" r="4" fill="#7c5cff"/>`).join("")}</svg><div class="small muted">Linha amarela = meta ${Math.round(.85*40)} · vermelha = corte 20 (cotas 16)</div>`:`<div class="muted">Sem redações ainda.</div>`;
 return `<div class="grid g2"><div class="card"><h3>Nova redação (autoavaliação 0–10 por critério)</h3><label>Tema</label><input id="rt" placeholder="Tema da redação">
 <div class="f3"><div><label>Tema</label><input id="r0" type="number" min="0" max="10" step="0.5"></div><div><label>Estrutura</label><input id="r1" type="number" min="0" max="10" step="0.5"></div><div><label>Língua</label><input id="r2" type="number" min="0" max="10" step="0.5"></div><div><label>Coesão</label><input id="r3" type="number" min="0" max="10" step="0.5"></div></div>
 <p class="small muted">Edital: 0–40 pontos, aprovação ≥20. Dissertativo-argumentativo, mín. 8 linhas autorais, sem 1ª pessoa, sem copiar coletânea nem modelo pronto. Proposta de intervenção não é obrigatória.</p><button class="btn" onclick="addR()">Salvar (+80 XP)</button></div>
 <div class="card"><h3>Evolução</h3>${sv}</div><div class="card" style="grid-column:1/-1"><h3>Histórico</h3><table>${hist||"<tr><td class=muted>—</td></tr>"}</table></div></div>`}
function addR(){const s=[0,1,2,3].map(i=>Math.min(10,Math.max(0,+$("#r"+i).value||0)));const tot=s.reduce((a,b)=>a+b,0);if(!tot)return;S.ess.push({d:todayStr(),tema:$("#rt").value,s,tot});save();boom();toast("📝 Redação registrada! +80 XP");render()}

function badges(){const done=TOPICS.filter(t=>isDone(t.id)).length,q=S.log.reduce((a,l)=>a+l.q,0),p=pareto80()/0.8,st=streak(),mx=Math.max(0,...[...new Set(S.log.map(l=>l.d))].map(hoursOn));
 const accOk=DISCS.some(d=>{const s=dStats(d);return s.q>=50&&s.acc>=META()});
 return[["🚀","Primeiro passo","Conclua 1 tema",done>=1],["🧱","Construtor","10 temas concluídos",done>=10],["📚","Meio caminho","37 temas concluídos",done>=37],["🏁","Plano completo","Todos os temas",done>=TOPICS.length],
 ["⭐","Pareto 50%","Metade do núcleo",p>=.5],["💎","Pareto 80%","Núcleo completo",p>=1],["✍️","Centenário","100 questões",q>=100],["🎯","Mil e uma","500 questões",q>=500],["🏹","Sniper 85%","≥85% em uma disciplina (50+ q.)",accOk],
 ["🔥","3 dias seguidos","Streak 3",st>=3],["🌋","Semana de fogo","Streak 7",st>=7],["🛡️","Disciplina de ferro","Streak 30",st>=30],["⏳","Dia cheio","Estudar a meta de horas num dia",mx>=S.set.hdia],
 ["📝","Redator","1ª redação",S.ess.length>=1],["🏅","Redação nota alta","Redação ≥34/40",S.ess.some(e=>e.tot>=34)],["🔁","Memória de elefante","10 revisões",revCount()>=10],["👑","Nível 5","Chegue ao nível 5",lvl(xpTotal()).L>=5]]}
function vConq(){const b=badges(),n=b.filter(x=>x[3]).length;
 return `<div class="grid"><div class="card"><h3>Conquistas · ${n}/${b.length}</h3><div class="grid g2">${b.map(x=>`<div class="badge ${x[3]?"":"off"}"><div class="ic">${x[0]}</div><div><b>${x[1]}</b><small>${x[2]}</small></div></div>`).join("")}</div></div>
 <div class="card"><h3>Ajustes</h3><div class="f3"><div><label>Meta de acerto (%)</label><input id="sm" type="number" value="${S.set.meta}"></div><div><label>Horas por dia</label><input id="sh" type="number" step="0.5" value="${S.set.hdia}"></div><div><label>Mín. questões p/ meta</label><input id="sq" type="number" value="${S.set.minq}"></div></div>
 <div class="row" style="margin-top:10px"><button class="btn" onclick="saveSet()">Salvar ajustes</button><button class="btn ghost" onclick="dl()">⬇ Baixar backup</button></div>
 <p class="small muted">Início do plano: ${fmtD(S.start)}. Peso por disciplina e horas por tema são estimativas (editáveis no código). Dados em progresso_tjsp.json.</p></div></div>`}
function saveSet(){S.set.meta=+$("#sm").value||85;S.set.hdia=+$("#sh").value||4;S.set.minq=+$("#sq").value||20;save();toast("Ajustes salvos");render()}
function dl(){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(S,null,1)],{type:"application/json"}));a.download="backup_tjsp.json";a.click()}

function go(t){tab=t;render()}
function render(){hud();$("#nav").innerHTML=TABS.map(([k,l])=>`<button class="${k===tab?"on":""}" onclick="go('${k}')">${l}</button>`).join("");
 $("#app").innerHTML={hoje:vHoje,plano:vPlano,pareto:vPareto,questoes:vQuest,redacao:vRed,conq:vConq}[tab]()}
load();
</script></body></html>'''
HTML = HTML.replace("__TOPICS_JS__", json.dumps(TOPICS, ensure_ascii=False)).replace("__DISCW_JS__", json.dumps(DISC_W, ensure_ascii=False))
PAGE = HTML.encode("utf-8")


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/state"):
            data = b"{}"
            if os.path.exists(ARQ):
                with open(ARQ, "rb") as f:
                    data = f.read() or b"{}"
            self._send(200, data, "application/json")
        else:
            self._send(200, PAGE, "text/html; charset=utf-8")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        try:
            json.loads(body)
        except Exception:
            return self._send(400, b"{}", "application/json")
        tmp = ARQ + ".tmp"
        with open(tmp, "wb") as f:
            f.write(body)
        os.replace(tmp, ARQ)
        self._send(200, b"{}", "application/json")


def main():
    host = "0.0.0.0" if "--rede" in sys.argv else "127.0.0.1"
    for port in range(8765, 8785):
        try:
            srv = ThreadingHTTPServer((host, port), H)
            break
        except OSError:
            continue
    else:
        print("Não achei porta livre."); return
    url = f"http://127.0.0.1:{port}"
    print(f"🎯 Missão Aprovação rodando em {url}  (Ctrl+C para sair)")
    if host == "0.0.0.0":
        print("   No celular (mesmo Wi-Fi): abra http://IP-DO-SEU-PC:%d" % port)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nAté a próxima sessão!")


if __name__ == "__main__":
    main()

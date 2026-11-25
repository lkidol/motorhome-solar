# Levantamento Comercial de Materiais (BOM) — Motorhome Solar (v3)

Baseado no **Inventário de Massas — Motorhome Solar (v3)** (`4.469,7 kg` carregado / `3.956,2 kg` vazio / `PBT 5.000 kg`), este levantamento cobre todos os **85 itens construtivos** (6 subáreas técnicas) priorizando **componentes comerciais de fácil acesso no mercado brasileiro** e **melhor custo-benefício (tendendo à opção mais econômica viável)**.

> [!NOTE]
> **Premissas de preço:** Valores estimados em reais (R$) apenas de **materiais e componentes** (sem mão de obra especializada, ferramental, frete interestadual ou homologação/CAT/CCT). Itens de alta tensão (células LFP, powertrain EV, OBC/DC-DC) refletem importação direta da China (Alibaba/DDP) com dólar-referência e tributos inclusos; itens mecânicos/interiores refletem distribuidores nacionais, autopeças comerciais e marketplaces (Mercado Livre, Leroy Merlin, Leo Madeiras, lojas de RV).


> [!WARNING]
> **Atualização de 25/11/2026 (inventário térmico, itens 11 e 30 a 35):** algumas linhas deste levantamento ficaram desatualizadas e precisam ser recotadas. A bateria passou a NCM de **203,6 kWh** (764 células equivalentes à LG E65D) com 2 placas frias, no lugar das 128 células LFP (linha 38). O motor é o **Cascadia SS-320-180** com redutor **8:1** e o inversor é o **CM350SiC** (linha 40). O conversor solar passou a ser o **BrightLoop DCHV** (linha 43). A climatização usa **2 Dometic FreshWell 3000 + MaxxFan Deluxe** (linha 49) e o arrefecimento tem **radiador sob medida, 2 ventiladores SPAL VA18, bombas Pierburg CWA 150 e Rheinmetall CWP 50**, sem chiller (linha 50). Geladeira (Dometic RC 10.4M90), cooktop (Dometic CVI1525), vaso (Thetford C223-CS) e películas 3M Crystalline também foram definidos. Os preços abaixo ainda são os da versão anterior; a lista de modelos está em `plan/Inventario_de_Massas_Motorhome_Solar.xlsx`.

---

## 1. Resumo Executivo por Subárea

| Subárea | Itens | Massa (kg) | Faixa Estimada — Rota Custo-Benefício (R$) | % do Custo Médio | Principal Alavanca de Economia |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Mecânica** | 37 | 2.049,9 | R$ 76.700 – R$ 129.200 | 29,6% | Painel PRFV+PIR nacional, aço A572 nas longarinas, conjunto rodagem/suspensão de van doadora (Daily/Sprinter) |
| **Elétrica** | 11 | 1.193,8 | R$ 151.900 – R$ 246.200 | 57,3% | Compra direta de células LFP em lote (DDP), kit 3-em-1 ou powertrain EV de sucata, painéis rígidos nas gavetas |
| **Térmica** | 4 | 70,0 | R$ 6.200 – R$ 9.650 | 2,3% | Split Inverter 9.000 BTU residencial (via inversor) em vez de AC 12V dedicado; radiador automotivo |
| **Hidráulica** | 3 | 26,0 | R$ 1.700 – R$ 2.700 | 0,6% | Tanques PEAD rotomoldados de prateleira + PEX nacional |
| **Interiores** | 25 | 553,9 | R$ 17.950 – R$ 37.950 | 8,1% | Compensado Naval de Paricá (no lugar do choupo), frigobar 220V, Porta Potti, bancos de van usados + base giratória |
| **Acessórios externos** | 5 | 62,5 | R$ 3.850 – R$ 10.850 | 2,1% | Toldo nacional/saco, degrau manual/nacional, iluminação LED comercial universal |
| **Total Construtivo** | **85** | **3.956,2** | **R$ 258.300 – R$ 436.550** | **100%** | — |
| *Carga útil (operacional)* | *11* | *513,5* | *Fora da BOM construtiva* | — | *Ocupantes, água, bagagem, roupas, camping* |

> [!IMPORTANT]
> **Onde está o dinheiro:** **Elétrica (57%) + Mecânica (30%)** concentram ~87% do custo total. Só as **128 células LFP (128,6 kWh)** + **powertrain EV de 120–150 kW** representam cerca de metade do orçamento do veículo inteiro.

---

## 2. Mapa de Substituições Comerciais no Brasil ("De → Para")

Vários materiais especificados na planilha seguem catálogos europeus (caros ou indisponíveis em prateleira no Brasil). Abaixo estão os equivalentes comerciais mais baratos e fáceis de comprar localmente:

| Material na Planilha | Gargalo no Brasil | Substituto Comercial Econômico (BR) | Impacto Técnico / Massa |
| :--- | :--- | :--- | :--- |
| **Al 5754-H22 (3 mm)** (casca e caixas de roda) | Liga automotiva europeia, rara e cara no varejo | **Opção A (mais barata):** Painel sanduíche pronto **PRFV (fibra de vidro gelcoat 1,5–2 mm) + PIR 25–30 mm** (padrão baú frigorífico/motorhome)<br>**Opção B (metálica):** **Chapa Al 5052-H32** (naval, mesma família Al-Mg) | Opção A é **~40–50% mais barata**, não amassa fácil e pode reduzir ~80–120 kg na casca; Opção B mantém desempenho mecânico equivalente |
| **Compensado de choupo (poplar)** | Importado da Europa, preço proibitivo | **Compensado Naval de Paricá** (cola fenólica WBP) | Densidade quase idêntica (~450–500 kg/m³ vs 480 kg/m³ do choupo) custando **~1/3 do preço** |
| **Tubo Al 6061-T6 250×80×6 mm** (longarinas) | Perfil extrudado fora de catálogo de prateleira no Brasil | **Perfil U dobrado/enrijecido ou tubo retangular em Aço ASTM A572 Gr.50** (ou viga caixa soldada em chapa Al 5052/6061) | Aço A572 custa **~1/4 do alumínio** e qualquer serralheria solda; recalcular seção (chapa 3–4,75 mm) para compensar o peso (+40 a +70 kg) |
| **Aço S355** (subchassis) | Norma europeia EN 10025 | **Aço ASTM A572 Grau 50** (Gerdau/Usiminas) ou **ASTM A36** | A572 Gr.50 tem o mesmo escoamento (345–355 MPa) e é padrão industrial brasileiro |
| **Painel colmeia de Al 20 mm** (piso) | Importado/sob encomenda, muito caro | **Compensado Naval Paricá 15–18 mm** apoiado em grade de tubo Al 6063 | Economiza R$ 3.500–6.000; acréscimo pequeno (~12–18 kg em ~6 m²) |
| **PP-EPDM (TPO) 3 mm** (para-choques, saias, aerofólio) | Injeção exige moldes de centenas de milhares de reais | **PRFV (fibra de vidro laminada)** sobre molde em EPS/PU ou **ABS/PEAD termoformado** | Custo compatível com unidade única; fácil reparo em estrada |
| **Ar-condicionado compacto ~3 kW 12V** | Unidades RV 12V custam R$ 5.500–18.000 | **Split Inverter residencial 9.000–12.000 BTU Quente/Frio** alimentado pelo inversor 3 kVA | Custa **R$ 1.900–2.700** (economia de R$ 3.500–10.000) com maior eficiência (COP) |
| **Vaso cassete embutido** | R$ 3.400–4.350 | **Vaso portátil tipo Porta Potti 17–20 L** (Seaflo/Nautika) com trava de piso | Custa **R$ 450–850** (economia de ~R$ 3.000) e pesa menos |
| **Geladeira 12V 90 L** | R$ 4.100–4.500 (Elber/ResfriAr) | **Frigobar 80–90 L 220V Inverter/A+++** (Midea/Consul) ligado no inversor 3 kVA | Custa **R$ 1.100–1.400** (economia de ~R$ 3.000); exige apenas trava de porta e boa ventilação |
| **Suspensão, freios, direção e semieixos** | Fabricação customizada é inviável em custo | **Peças de utilitário comercial doador** (Iveco Daily 55C/70C, MB Sprinter 516/517, VW Delivery Express) | Peças de reposição baratas em qualquer autopeças do país e dimensionadas para 4,5–5,5 t |

---

## 3. Levantamento Detalhado Item a Item (85 Itens Construtivos)

### 3.1 Mecânica (37 itens — 2.049,9 kg)

#### A. Casca, Estrutura da Carroceria, Portas e Vidros

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | Casca: laterais | 19,23 m² / 221,9 kg | Sanduíche 30 mm (Al 5754 3 mm + PIR 23 mm + choupo 3 mm) | Painel sanduíche pronto PRFV 1,5–2 mm + PIR 25–30 mm **ou** montagem c/ chapa Al 5052 1,5–2 mm + PIR + Paricá 4 mm | Sulfibra, fabricantes de baú frigorífico, isolantes PIR + distribuidor Al | 4.200 – 6.200 |
| 2 | Casca: fundo | 13,89 m² / 160,3 kg | Mesmo sanduíche | Mesmo painel sanduíche (com face inferior em PRFV/Al 5052 resistente a pedriscos/umidade) | Idem acima | 3.100 – 4.400 |
| 3 | Casca: teto | 12,94 m² / 149,3 kg | Mesmo sanduíche *(nota: pele 1,5 mm = −52 kg)* | Painel PRFV 1,5 mm + PIR 25–30 mm (ou Al 5052 1,5 mm + PIR + Paricá 4 mm) | Idem acima | 2.800 – 4.100 |
| 4 | Casca: frente | 2,66 m² / 30,7 kg | Mesmo sanduíche | PRFV laminado sobre espuma PIR/PU moldada (ideal para curvas frontais) ou Al 5052 calandrado | Lojas de compósitos (resina + manta fibra) / funilaria | 600 – 850 |
| 5 | Casca: traseira | 2,25 m² / 26,0 kg | Mesmo sanduíche | Painel sanduíche PRFV + PIR ou Al 5052 + PIR | Idem item 1 | 500 – 750 |
| 6 | Quadro de perfis (cavernas e longitudinais) | 1 (~182 m) / 149,0 kg | Al 6063-T6 tubo 40×40×2 mm (~31 barras de 6 m) | Tubo quadrado Al 6063-T5/T6 40×40×2 mm (barras 6 m padrão serralheria) | Coppermetal, Shockmetais, distribuidores de alumínio | 3.400 – 4.700 |
| 7 | Caixas de roda dianteiras (2) | 2,254 m² / 18,3 kg | Al 5754 3 mm | 1 chapa Al 5052-H32 2–3 mm cortada/dobrada **ou** laminação PRFV c/ manta | Distribuidor de metais / compósitos | 600 – 1.000 |
| 8 | Caixas de roda traseiras (2) | 6,564 m² / 53,2 kg | Al 5754 3 mm | 2–3 chapas Al 5052-H32 2–3 mm dobradas **ou** PRFV laminado | Idem acima | 1.500 – 2.600 |
| 9 | Adesivos, selantes e rebites | 1 cj / 18,0 kg | PU / MS polímero | Adesivo estrutural PU40/PU55 (Tekbond/Wurth/Sika 221/252 em sachê 600 ml) + rebites pop Al/inox + primer | Leroy Merlin, lojas de ferragens/parafusos, Mercado Livre | 1.200 – 2.200 |
| 10 | Porta do motorista | 1 / 23,6 kg | Sanduíche + vidro temperado 4 mm (0,48 m²) + ferragens | Folha no mesmo sanduíche + perfil Al porta + vidro temperado plano 4 mm sob medida + fechadura/dobradiças de van/caminhão | Vidraçaria temperados + autopeças (Daily/Sprinter) | 1.500 – 2.500 |
| 11 | Porta do passageiro | 1 / 23,6 kg | Igual à do motorista | Mesmo conjunto do item 10 | Idem acima | 1.500 – 2.500 |
| 12 | Porta de entrada | 1 / 31,4 kg | Sanduíche + vidro 0,48 m² + ferragens 12 kg | Folha sanduíche + perfil Al + vidro temperado 4 mm + fechadura RV importada/nacional + dobradiça contínua inox | Lojas RV (Camper Soul / Top RV) + serralheria Al | 2.000 – 3.500 |
| 13 | Para-brisa | 1 (3,25 m²) / 40,6 kg | Vidro laminado 5 mm (2×2,1 + PVB), colado c/ PU | **Adaptar para-brisa comercial de micro-ônibus/ônibus** (Volare/Marcopolo/Agrale — muito mais barato que fabricar molde curvo exclusivo) ou laminado plano 6 mm | Distribuidores de vidros automotivos (Autoglass, Fanavid, Saint-Gobain) | 2.200 – 4.500 |
| 14 | Janela da sala (2 folhas) | 1 (0,91 m²) / 10,8 kg | Acrílico duplo PMMA + caixilho, basculante | **Econômica:** janela automotiva de vidro temperado corrediça sob medida (~R$ 1.400) **ou** janela RV basculante acrílico duplo nacional (~R$ 2.800–3.200) | Vidraçarias automotivas de vans / Top RV / Camper Soul | 1.400 – 3.200 |

#### B. Chassi, Subchassis e Piso Estrutural

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 15 | Longarinas do chassi (2) | 2 × 6,6 m / 136,0 kg | Al 6061-T6 tubo 250×80×6 mm | **Econômica:** Perfil U dobrado ou tubo retangular em **Aço ASTM A572 Gr.50 / LN-280** (250×80×4,75–6 mm) *(alternativa em Al 5052/6061 viga soldada sai R$ 9k–15k)* | Gerdau, Aço Cearense, distribuidores de aço/dobra CNC | 2.800 – 4.500 |
| 16 | Travessas do chassi (8) | 8 × 1,9 m / 46,6 kg | Al 6061-T6 tubo 100×50×4 mm | Tubo retangular 100×50×3 mm em aço A572/A36 (ou Al 6063-T6 100×50×3–4 mm) — 3 barras de 6 m | Distribuidores de aço/alumínio | 1.400 – 2.800 |
| 17 | Subchassi dianteiro | 1 / 60,0 kg | Aço S355 soldado (torres, direção) | Chapa e tubo **Aço ASTM A572 Gr.50** (ou A36) cortado a laser/plasma + suportes aproveitados de van doadora | Corte laser / serralheria estrutural + desmanche legalizado | 2.500 – 4.500 |
| 18 | Subchassi traseiro | 1 / 55,0 kg | Aço S355 soldado (motor, suspensão) | Chapa e tubo **Aço ASTM A572 Gr.50** cortado e soldado (com coxins automotivos padrão caminhão leve) | Idem acima | 2.200 – 4.000 |
| 19 | Berço e chapa de proteção da bateria | 1 / 47,0 kg | Al 5083 5 mm + quadro 6061 | Chapa **Al 5052-H32 4–5 mm** (1,6×1,4 m) + quadro em cantoneira/tubo aço A36 ou Al 6063 | Distribuidores de metais não ferrosos | 1.800 – 3.200 |
| 20 | Barra de impacto dianteira e suportes | 1 / 10,0 kg | Aço / Al | Perfil U / tubo aço A36 4,75 mm + suportes fusíveis (crash-box dobrado) | Distribuidor de aço / serralheria | 400 – 800 |
| 21 | Barra traseira, engate e suportes | 1 / 15,0 kg | Aço / Al | Para-choque traseiro tubular homologado (padrão VUC/van) + engate reboque reforçado aço A36 | Autopeças pesadas / implementadoras | 700 – 1.400 |
| 22 | Piso elevado estrutural | 1 (~6,1 m²) / 42,5 kg | Painel colmeia Al 20 mm + apoios | **2 chapas Compensado Naval Paricá 18 mm** + grade de apoio em tubo Al 6063 30×30 mm | Leo Madeiras / Gasômetro + distribuidor Al | 1.000 – 1.800 |

#### C. Rodagem, Freios, Suspensão e Direção *(Recomendado: peças de reposição de van/VUC 5 t — Iveco Daily 55C/70C, MB Sprinter 516/517 ou VW Delivery Express)*

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 23 | Rodas + pneus dianteiros (2) | 2 / 96,0 kg | Roda aço 17,5×6,75 + pneu 245/70 R17.5 (136/134) | 2× Roda aço Maxion/equivalente 17,5×6,75 6 furos (R$ 800–1.000/un) + 2× Pneu radial LT importado (Westlake/Triangle/Advance, R$ 1.000–1.400/un) | Truck Rodas, Mundo do Caminhão, PneuStore, atacadistas | 3.600 – 4.800 |
| 24 | Rodas + pneus traseiros (2) | 2 / 96,0 kg | Igual às dianteiras | Mesmo conjunto do item 23 (2 unidades) | Idem acima | 3.600 – 4.800 |
| 25 | Estepe | 1 / 48,0 kg | Mesma roda e pneu *(ou kit reparo)* | 1× conjunto roda + pneu (R$ 1.800–2.400). *Alternativa ultra-barata/leve: kit reparo + compressor 12V por ~R$ 350* | Idem acima | 1.800 – 2.400 |
| 26 | Freios dianteiros (2) | 2 / 32,0 kg | Cubo, disco ventilado Ø330–350 mm, pinça | Kit cubo + disco ventilado + pinça + pastilha de **Iveco Daily 55C/70C** ou **Sprinter 516** (reposição Fremax/Hipper Freios/TRW) | Autopeças linha pesada / Mercado Livre / desmanche legalizado | 2.800 – 4.800 |
| 27 | Freios traseiros (2) | 2 / 32,0 kg | Disco Ø330–350 mm, ferro fundido | Mesmo padrão comercial com pinça/tambor de freio de estacionamento integrado (Daily/Sprinter) | Idem acima | 2.800 – 4.800 |
| 28 | Suspensão diant.: não suspensa | 2 / 44,0 kg | Mangas, metade dos braços e amortecedores | Mangas de eixo + pivôs + terminais de **Iveco Daily 55C/70C** (ou Sprinter 516) | Autopeças comerciais / desmanche credenciado (CDV) | 2.500 – 4.500 |
| 29 | Suspensão diant.: suspensa | 1 / 46,0 kg | Braços sobrepostos ou McPherson reforçado, molas | Bandejas/braços + molas helicoidais/barra torção + amortecedores Cofap/Monroe linha pesada (Daily/Sprinter) | Idem acima | 3.000 – 5.000 |
| 30 | Suspensão tras.: não suspensa | 2 / 42,0 kg | Mangas, metade dos braços e amortecedores | Mangas/cubos traseiros independentes de utilitário pesado/SUV pesado (ou adaptação c/ rolamento blindado de van) | CDV / usinagem + autopeças | 2.800 – 4.800 |
| 31 | Suspensão tras.: suspensa | 1 / 58,0 kg | Independente, com o motor central | Braços tubulares em aço ASTM A572/SAE 1020 + buchas PU + conjunto mola helicoidal reforçada + amortecedores linha pesada | Metalúrgica + autopeças pesadas (molas Fabrini/Cindumel) | 3.200 – 5.700 |
| 32 | Semieixos (2) | 2 / 18,0 kg | Aço forjado, juntas homocinéticas | Par de semieixos homocinéticos reforçados de **Fiat Ducato / Renault Master / Ford Transit** (com comprimento ajustado em tornearia) | Autopeças (Nakata/Cofap/Ima) / CDV | 1.600 – 3.000 |
| 33 | Direção elétrica + coluna | 1 / 25,0 kg | Pinhão e cremalheira c/ assistência elétrica | Caixa mecânica/hidráulica de van + **coluna de direção elétrica (EPS)** de sucata (VW/Hyundai/Toyota/Ford) c/ módulo controlador PWM barato | CDV + Mercado Livre | 2.200 – 4.200 |

#### D. Acabamento Externo e Estruturas Solares

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 34 | Para-choques, alargadores, soleiras, saias, difusor e aerofólio | 1 cj / 60,0 kg | PP-EPDM (TPO) 3 mm + suportes | **Laminação artesanal em PRFV (fibra de vidro + resina poliéster + gelcoat/tinta PU)** sobre molde simples de EPS/madeira | Lojas de fibra/compósitos (Redelease, Barracuda) | 3.000 – 6.000 |
| 35 | Carenagem lateral do teto | 1 / 10,0 kg | Al 1,5 mm | Chapa **Al 5052 1,5 mm** dobrada ou **ACM 4 mm** frisado/dobrado | Distribuidor Al / lojas de comunicação visual (ACM) | 600 – 1.100 |
| 36 | Suporte do painel solar fixo | 1 / 17,6 kg | Perfis de Al (8,8 m², 8 cm acima do teto) | Perfis extrudados padrão fotovoltaico (40×40 mm) + grampos *end/mid clamp* + suportes L em inox | Distribuidoras solares (Aldo, Ecori, Minha Casa Solar, ML) | 700 – 1.300 |
| 37 | Quadros das gavetas solares + trilhos e atuadores | 1 / 56,5 kg | Al + 30 kg de trilhos e atuadores (curso 1,40 m) | Quadro em tubo Al 6063 25×25×2 mm + 4 corrediças telescópicas industriais carga pesada (1,4 m, 150–220 kg) + 2 atuadores lineares 12V. *Obs.: acionamento manual com trava cai para R$ 1.800–2.800* | Mercado Livre, lojas de ferragens industriais, AliExpress/Alibaba | 3.200 – 6.000 |

**Subtotal Mecânica (37 itens):** **R$ 76.700 – R$ 129.200**

---

### 3.2 Elétrica (11 itens — 1.193,8 kg)

> [!WARNING]
> **Atenção na arquitetura solar ↔ tração:** Os 3 controladores **MPPT 60A** baratos (R$ 500–950 cada) carregam bancos de **12V/24V/48V** (bateria auxiliar). Para injetar energia solar diretamente no pack de tração de **409,6 V**, é necessário um **MPPT Boost de alta tensão** dedicado (ou transferir via inversor AC → entrada AC do OBC, que é mais barato em protótipo porém menos eficiente).

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR / Import.) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 38 | Células da bateria de tração | 128 / 716,8 kg | LFP prismática 314 Ah (~5,6 kg), 128S1P = 409,6 V, 128,6 kWh | **128 × EVE MB31 (314 Ah) ou EVE LF280K (280 Ah) Grade A** importadas em lote fechado via DDP marítimo (~R$ 550–750/un nacionalizada; compra varejo ML sai ~R$ 900–1.200/un) | Alibaba (fornecedores verificados EVE: Docan, Basen, Xiho, Amy Wan) / importadores BR | 70.400 – 96.000 |
| 39 | Caixa do pack, placa fria, BMS e barramentos | 1 / 143,2 kg | Caixa Al + placa fria + BMS + barramentos | Caixa soldada em Al 5052 3 mm + placa fria serpentina Al importada + **BMS HV 128S Master-Slave** (Daly HV / ENNOID / JBD HV) + barramentos cobre flexível + cintas compressão | Serralheria Al + Alibaba (placa fria e BMS HV) | 12.000 – 22.000 |
| 40 | Motor + redução 15:1 + diferencial | 1 / 120,0 kg | PMSM 120–150 kW | **Opção A (nova):** Kit **3-em-1 PMSM 120–150 kW** (motor+redutor+diferencial, Alibaba US$ 3.300–5.500 FOB → ~R$ 32k–55k nacionalizado)<br>**Opção B (mais barata):** Conjunto usado de **BYD / Nissan Leaf / JAC / Tesla** de leilão/sucata (R$ 20k–38k) | Alibaba (Brogen, Shinegle, Golden Motor, Enpower) ou leilões/CDVs de EVs no Brasil | 28.000 – 55.000 |
| 41 | Inversor de tração | 1 / 12,0 kg | Carcaça Al fundido (400 V, 120–150 kW) | Controlador PMSM 400V 150kW compatível com o motor *(se comprado em combo com o item 40, reduz para ~R$ 0 adicional; avulso nacionalizado ~R$ 7,5k–14k)* | Mesmo fornecedor do motor (Alibaba / CDV) | 7.500 – 14.000 |
| 42 | Caixa de alta tensão (PDU) + chave de serviço | 1 / 15,0 kg | Contatores, fusíveis e pré-carga | Caixa metálica IP65 + 3 contatores HV DC (Hongfa/TE/Gigavac 400A) + fusível ultrarrápido aR 500V + resistor pré-carga + chave MSD (manual service disconnect) | Alibaba / AliExpress / distribuidores industriais (WEG/Bussmann/Littelfuse) | 3.500 – 6.500 |
| 43 | Baía técnica (OBC 11 kW, DC-DC 400/12 V, 3 MPPT, inv. 3 kVA) | 1 / 40,0 kg | Carregador 11 kW, DC-DC 400/12V, 3 MPPT, inv. 3 kVA | **OBC 6,6–11 kW + DC-DC 400→12V "2 em 1"** via Alibaba (R$ 8.500–16.000 nacionalizado) + **3× MPPT 60A** (PowMr/Epever, R$ 1.800–2.800) + **Inversor Senoidal Pura 3.000W** (Jinsi/Flach/Epever, R$ 1.000–1.800) | Alibaba (OBC+DCDC) + Mercado Livre / Minha Casa Solar (MPPT e Inversor) | 11.300 – 20.600 |
| 44 | Bateria auxiliar 12 V | 1 / 22,0 kg | LFP 200 Ah (2,6 kWh) | Bateria **LiFePO4 12V 200Ah** pronta (Enershare, FelicitySolar, Inohouse) **ou** 4× células 200Ah + BMS JK 200A | Mercado Livre / Minha Casa Solar | 3.000 – 4.200 |
| 45 | Chicotes AT (35–70 mm²) e BT | 1 / 60,0 kg | Cobre + isolação | Cabo laranja HV blindado 35–50 mm² (importado/nacional) + conectores HV (Amphenol/Degson) + cabos flexíveis cobre BT (4–35 mm²) + disjuntores DC/terminais | Alibaba (cabo/conectores HV) + lojas elétricas BR (Sil/Cobrecom) | 4.000 – 7.500 |
| 46 | Tomada de carga CCS2 + tampa | 1 / 3,0 kg | Entrada CCS2 c/ cabos até a baía | Inlet **CCS2 200A** automotivo com cabos 50–70 mm² + atuador trava 12V + tampa | Alibaba / AliExpress | 1.200 – 2.400 |
| 47 | Módulos solares do painel fixo | 8,83 m² / 30,9 kg | Módulos leves sem vidro, 3,5 kg/m² (~1,6–1,8 kWp) | **8–9 × Painéis semiflexíveis ETFE 200 W** (evitar PET barato que amarela; ETFE dura bem no sol) | Mercado Livre, Shopee, Alibaba (lote), lojas RV | 5.500 – 9.000 |
| 48 | Módulos solares das gavetas | 8,84 m² / 30,9 kg | Módulos leves sem vidro (2 gavetas 3,40×1,30 m) | **8–9 × Painéis semiflexíveis ETFE 200 W** (R$ 5.500–9.000). *Alternativa muito mais barata (como as gavetas são planas): 4× painéis rígidos convencionais 450–550 W por ~R$ 2.200–3.200 (porém +60 kg)* | Idem acima / distribuidoras solares BR | 5.500 – 9.000 |

**Subtotal Elétrica (11 itens):** **R$ 151.900 – R$ 246.200**

---

### 3.3 Térmica (4 itens — 70,0 kg)

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 49 | Ar-condicionado / bomba de calor | 1 / 30,0 kg | Unidade compacta ~3 kW sob o painel | **Split Inverter 9.000–12.000 BTU Quente/Frio** (Midea, Gree, Elgin, Philco) operando via inversor 3 kVA *(alternativa AC 12V universal/caminhão sai R$ 5.500–8.500)* | Magazine Luiza, Mercado Livre, Frigelar | 1.900 – 2.700 |
| 50 | Arrefecimento do motor e da bateria | 1 / 30,0 kg | Chiller, bomba, radiador 0,6×0,4 m, 8 L fluido | Radiador alumínio brasado automotivo ~600×400 mm (ex: Corsa/Gol/van) + eletroventilador Spal/universal + 2× bombas elétricas 12V (Bosch/Pierburg) + trocador a placas inox (chiller acoplado ao AC) + mangueiras EPDM + aditivo | Autopeças BR + Mercado Livre | 2.200 – 4.200 |
| 51 | Boiler 10 L + bomba d'água | 1 / 10,0 kg | Inox + Al, no gabinete da cozinha | **Boiler elétrico 10 L (12V/220V)** nacional (R$ 1.800–2.300) + **Bomba pressurizadora 12V Seaflo 3.0 GPM** (R$ 300–450) | Mercado Livre, lojas RV (Top RV, Casa do Motor Home) | 2.100 – 2.750 |
| 52 | Isolamento térmico | 1 / 0 kg | Núcleo PIR 23 mm (já na casca) | Já incluso na compra dos painéis/placas PIR da casca (itens 1–5) | — | 0 |

**Subtotal Térmica (4 itens):** **R$ 6.200 – R$ 9.650**

---

### 3.4 Hidráulica (3 itens — 26,0 kg)

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 53 | Tanque de água limpa (vazio) | 1 / 10,0 kg | 100 L, PEAD rotomoldado (0,50×0,90×0,24 m) | Reservatório retangular **PEAD rotomoldado atóxico 100 L** (ou PP soldado sob medida) | Mercado Livre, PPVille, Grupo Damek, lojas RV | 650 – 950 |
| 54 | Tanque de água cinza (vazio) | 1 / 8,0 kg | 80 L, PEAD (0,50×0,75×0,24 m) | Reservatório **PEAD rotomoldado 80 L** (ou PP soldado sob medida) | Idem acima | 550 – 850 |
| 55 | Tubulação, registros e ralos | 1 / 8,0 kg | PEX / PP | Tubo PEX 16 mm (água quente/fria) + conexões engate rápido (John Guest/genérico) + válvula guilhotina 50 mm esgoto + ralo inox + bocal abastecimento | Leroy Merlin, Mercado Livre, lojas hidráulicas | 500 – 900 |

**Subtotal Hidráulica (3 itens):** **R$ 1.700 – R$ 2.700**

---

### 3.5 Interiores (25 itens — 553,9 kg)

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 56 | Piso vinílico 2 mm + tapete | 1 (~7 m²) / 25,8 kg | PVC, 3,4 kg/m² | Piso vinílico em manta ou régua colada 2 mm (Tarkett/Kapazi/Eucafloor) + cola acrílica + tapete borracha cabine | Leroy Merlin, Telhanorte, Mercado Livre | 450 – 800 |
| 57 | Forro do teto em ripas | 1 (~11 m²) / 32,9 kg | Madeira 6 mm, ~11 m² | Ripas de **Pinus seco aparelhado 6–9 mm** c/ seladora/verniz **ou** forro PVC amadeirado leve | Madeireiras locais, Leroy Merlin | 600 – 1.200 |
| 58 | Revestimento das paredes | 1 (~22 m²) / 13,2 kg | Feltro automotivo 4 mm | Carpete/feltro automotivo de forração 4 mm (rolo 2 m largura) + cola de contato spray/lata | Casas de tapeçaria automotiva, Mercado Livre | 500 – 900 |
| 59 | Painel de instrumentos, telas e console | 1 / 45,0 kg | PP/ABS sobre aço, eletrônica | Estrutura em compensado + PRFV/courvin + **Multimídia Android 10" + tela 7–10" cluster digital via CAN-BUS** (ESP32/RealDash) + chaves basculantes | Mercado Livre, AliExpress, tapeçaria | 1.500 – 3.000 |
| 60 | Banco do motorista (giratório, c/ cinto) | 1 / 32,0 kg | Aço, espuma PU, tecido, cinto 3 pontos | **Banco usado de van** (Sprinter/Ducato/Master) em bom estado + **base giratória nacional aço 3 mm** + cinto 3 pontos | CDV/tapeçaria + Camper Soul / Maximus Bancos / ML | 1.500 – 2.400 |
| 61 | Banco do passageiro (giratório, c/ cinto) | 1 / 32,0 kg | Igual ao do motorista | Mesmo conjunto do item 60 | Idem acima | 1.500 – 2.400 |
| 62 | Volante, pedais e colunas | 1 / 10,0 kg | Aço / Al / PU | Volante automotivo padrão + conjunto pedais (freio + acelerador eletrônico Hall universal/van) + alavanca seletora PRND | Autopeças / CDV / Mercado Livre | 800 – 1.500 |
| 63 | Cooktop de indução 2 zonas | 1 / 8,0 kg | 2.000 W | Cooktop indução 2 bocas (Philco PCT20P / Mondial CTI-02 / Electrolux / Fischer) | Mercado Livre, Amazon, Magalu | 450 – 950 |
| 64 | Móveis da cozinha | 1 / 40,0 kg | Gabinete choupo 15 mm, bancada carvalho 35 mm, cuba inox | **Compensado Naval Paricá 15 mm** + bancada em **painel Pinus/Tauari/Muiracatiara** (ou compensado revestido em fórmica) + cuba inox Tramontina + torneira misturadora | Leo Madeiras, Leroy Merlin, Mercado Livre | 1.200 – 2.200 |
| 65 | Geladeira 90 L | 1 / 25,0 kg | Compressor 12 V, aço + PU | **Ultra-econômica:** Frigobar 80–90 L 220V (Midea/Consul, R$ 1.100–1.400) no inversor **ou** **Dedicada 12V:** Elber RVB90 / ResfriAr (~R$ 4.100–4.500) | Magalu/Amazon (220V) ou Mercado Livre/Elber (12V) | 1.200 – 4.500 |
| 66 | Armário aéreo da cozinha | 1 / 16,0 kg | Choupo 12 mm | Compensado Naval Paricá 12 mm + dobradiças + travas *push-lock* RV + pistão a gás | Leo Madeiras + Mercado Livre | 400 – 750 |
| 67 | Banheiro: paredes, piso do box e porta | 1 / 42,0 kg | GRP 4 mm + choupo; 0,9×0,9 m | Parede em **Compensado Naval 10 mm revestido c/ ACM 3 mm ou fibra PRFV 1,5 mm** + bandeja box de fibra pronta (90×90 cm) + porta sanfonada PVC/acrílico | Lojas de ACM/fibra + materiais de construção | 1.400 – 2.600 |
| 68 | Banheiro: vaso cassete, cuba, armário e chuveiro | 1 / 30,0 kg | ABS / cerâmica / inox | **Econômica:** Vaso **Porta Potti 20 L** Seaflo/Nautika (R$ 500–800) + cuba ABS/inox + ducha + misturador (~R$ 1.000–1.400 total) **ou** **Vaso Cassete 12V** Freucamp/Top RV (~R$ 3.400–4.200 + acessórios) | Mercado Livre, Mundo Camper, King 4x4 | 1.000 – 4.800 |
| 69 | Banco fixo da sala (frente) com baú | 1 / 22,0 kg | Choupo 15 mm + espuma D33 + cinto subabdominal | Compensado Naval Paricá 15 mm + estrutura reforço aço p/ cinto + espuma D33 8–10 cm + courvin/suede + cinto abdominal homologado | Madeireira + casa de espumas + autopeças | 600 – 1.100 |
| 70 | Banco fixo da sala (trás) | 1 / 22,0 kg | Choupo 15 mm + espuma + cinto | Mesmo conjunto do item 69 | Idem acima | 600 – 1.100 |
| 71 | Tablado da sala (15,5 cm) | 1 / 8,0 kg | Choupo 18 mm + vinílico + perfil Al | Sobra de Compensado Naval Paricá 18 mm + sobra vinílico + cantoneira Al de acabamento | Madeireira / Leroy Merlin | 250 – 450 |
| 72 | Mesa da sala | 1 / 14,0 kg | Tampo carvalho 30 mm + coluna inox | Tampo em **painel Pinus/Tauari 25–30 mm** + pedestal articulado/desmontável de alumínio/inox para RV | Madeireira + Mercado Livre | 400 – 750 |
| 73 | Guarda-roupa sobre a caixa de roda | 1 / 22,0 kg | Choupo 12 mm | Compensado Naval Paricá 12 mm + cabideiro Al + travas *push-lock* | Leo Madeiras + ferragens | 500 – 900 |
| 74 | Degraus e tampa do motor | 1 / 14,0 kg | Choupo 18 mm + carvalho | Compensado Naval Paricá 18 mm + manta termoacústica aluminizada (isolação do motor) + dobradiça piano | Madeireira + lojas som/tapeçaria | 350 – 650 |
| 75 | Estrado da cama | 1 / 26,0 kg | Choupo 18 mm (1,42×1,91 m) | 1 folha Compensado Naval Paricá 18 mm perfurada p/ ventilação (ou ripado de pinus estruturado) | Madeireira / Leo Madeiras | 400 – 700 |
| 76 | Colchão 1,4×1,9 m + roupa de cama | 1 / 22,0 kg | Espuma D28 140 mm + têxteis | Colchão de espuma D28/D33 138×188×14 cm (Ortobom, BF Colchões, Gazin) + jogo de cama simples | Mercado Livre, Magalu, lojas de colchões | 650 – 1.100 |
| 77 | Armários sobre o pé da cama | 1 / 14,0 kg | Choupo 12 mm, 3 portas | Compensado Naval Paricá 12 mm + 3 dobradiças/pistões + 3 *push-lock* | Leo Madeiras + ferragens | 450 – 800 |
| 78 | Fechamentos, soleiras e forros das caixas de roda | 1 / 22,0 kg | Choupo / ABS + soleiras Al | Sobras de Paricá 10–12 mm + carpete/courvin + cantoneira/soleira Al xadrez | Madeireira + ferragens | 500 – 900 |
| 79 | Fitas de LED, luminárias e fiação interna | 1 / 8,0 kg | Al + cobre | Fitas LED 12V SMD2835/COB + perfis Al difusor + 6 spots LED 12V embutir + cabos 1,5–2,5 mm² + painel interruptores 12V | Mercado Livre, Santa Ifigênia/lojas elétricas | 350 – 700 |
| 80 | Cortinas e persianas | 1 / 8,0 kg | Têxtil / plissado | Tecido blackout cortado sob medida + trilho suíço Al + isolante térmico refletivo com ventosas no para-brisa | Casas de tecido, Mercado Livre | 400 – 800 |

**Subtotal Interiores (25 itens):** **R$ 17.950 – R$ 37.950**

---

### 3.6 Acessórios Externos (5 itens — 62,5 kg)

| # | Item (Planilha) | Qtd / Massa | Especificação Original | Opção Comercial Econômica (BR) | Onde Comprar | Custo Est. (R$) |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| 81 | Toldo em cassete 3,1 m | 1 / 26,0 kg | Perfil Al anodizado + lona acrílica | **Ultra-econômica:** Toldo de bolsa/saco 3 m lona PVC (R$ 1.200–1.800) **ou** **Cassete manual nacional 3 m** (R$ 2.500–4.500) | Mercado Livre, Camper Soul, Top RV, toldarias | 1.200 – 4.500 |
| 82 | Degrau elétrico da porta de entrada | 1 / 15,0 kg | Al + motor 12 V | **Econômica:** Degrau retrátil manual de alumínio (R$ 600–900) **ou** **Degrau elétrico 12V** em alumínio (R$ 1.500–2.300) | Mercado Livre, Camper Soul, Open RV | 600 – 2.300 |
| 83 | Faróis, lanternas, retrovisores-câmera e limpadores | 1 / 16,0 kg | PC/PMMA + eletrônica (DRL, repetidores, laterais) | Blocos ópticos LED universais homologados (farol projetor 90 mm + lanternas traseiras LED caminhão/carreta + fita DRL) + **kit 2 câmeras AHD com monitor 7"** + motor/braços limpador de van | Autopeças linha pesada, Mercado Livre, AliExpress | 1.600 – 3.200 |
| 84 | Calhas de chuva e pingadeira | 1 (~10 m) / 4,0 kg | Perfil Al (~10 m) | Perfil J/pingadeira de alumínio (2 barras de 6 m) ou calha flexível automotiva autoadesiva | Distribuidores de Al / lojas RV | 250 – 500 |
| 85 | Placas dianteira e traseira + suportes | 2 / 1,5 kg | Mercosul 400×130 mm | Par de placas Mercosul estampadas + 2 suportes ABS | Estampadoras credenciadas DETRAN | 200 – 350 |

**Subtotal Acessórios Externos (5 itens):** **R$ 3.850 – R$ 10.850**

---

## 4. Top 6 Alavancas para Derrubar Ainda Mais o Orçamento

Se o objetivo do grupo for apresentar o **menor custo viável** (ou construir um protótipo enxuto), estas 6 decisões geram a maior economia:

1. **Redimensionar ou escalonar a bateria de tração:** O pack de `128,6 kWh` custa sozinho **R$ 82k–118k** (células + caixa + BMS). Se a autonomia-alvo permitir `~64–80 kWh` (ex.: 128S1P de células `150–200 Ah`), economiza-se **R$ 30.000–50.000** e **~320 kg** de massa.
2. **Powertrain EV de sucata legalizada (CDV/leilão):** Aproveitar conjunto completo (motor + inversor + redutor + OBC + DC-DC + chicotes + arrefecimento) de um EV sinistrado no Brasil (ex.: BYD Dolphin/Yuan, JAC, Nissan Leaf) costuma sair **R$ 25.000–45.000** no total — metade do preço de importar cada módulo separado novo.
3. **Casca em painel sanduíche PRFV + PIR de fabricante de baú frigorífico:** Substitui Al 5754 + choupo + colagem artesanal, economiza **R$ 12.000–20.000**, reduz peso e já sai com ótimo acabamento externo branco.
4. **Painéis rígidos convencionais nas 2 gavetas planas:** Como as gavetas são planas, usar 4 módulos rígidos comuns (~450–550 W, ~R$ 550–750 cada) em vez de ETFE flexíveis economiza **R$ 3.000–6.000** e entrega mais vida útil (verificar apenas o acréscimo de ~50–60 kg nos trilhos/teto).
5. **Aparelhos residenciais via inversor 3 kVA:** Trocar AC 12V + Geladeira 12V + Vaso Cassete por **Split Inverter 9.000 BTU + Frigobar 220V + Porta Potti** economiza de uma vez **R$ 9.000–14.000**.
6. **Chassi/Rodagem de utilitário 5 t doador (Iveco Daily 55C/70C ou Sprinter 516):** Em vez de fabricar subchassis, suspensões e freios do zero, comprar eixo/suspensão/freios/direção prontos de um único doador reduz custo de peças e elimina meses de usinagem.

---

## 5. Decisões em Aberto da Planilha (Olhar de Custo-Benefício)

| Pendência da Planilha | Recomendação Mais Econômica | Motivo |
| :--- | :--- | :--- |
| **Célula 314 Ah (MB31) vs 280 Ah (LF280K)** | **EVE LF280K (280 Ah)** ou **MB31 (314 Ah)** — cotar ambos em R$/kWh | A LF280K tem mais estoque global e costuma ter o menor R$/kWh em lote; a MB31 ganha +13% de energia no mesmo volume. |
| **Barramento auxiliar 12 V (22 kg) vs 48 V (89 kg)** | **12 V (ou 24 V) com LFP 200 Ah** | Muito mais barato (~R$ 3,5k vs ~R$ 12k+ no banco de 15 kWh em 48 V) e compatível com bombas, LEDs e acessórios automotivos sem conversores extras. |
| **Boiler 10 L + inv. 3 kVA vs Chuveiro 5 kW + inv. 9,6 kW** | **Boiler 10 L + Inversor 3 kVA** | Um inversor 3 kVA custa ~R$ 1.000–1.800; já um inversor ≥ 9,6 kW + fiação/banco compatível custaria R$ 7.000–15.000+. O boiler 10 L (R$ 1.800–2.300) sai muito mais barato no sistema total. |
| **Pneus 245/70 R17.5 (136/134)** | **Manter 245/70 R17.5 (rodas aço 17,5×6,75)** | É o pneu comercial de carga mais barato e fácil de achar no Brasil para suportar `4.470–5.000 kg` com folga de segurança (2.240 kg/roda). |

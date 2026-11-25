# Estado do projeto

Última atualização: 25/11/2026.

## Site 3D do esquemático

- Versão atual: `site/configurador.html` (portal em `site/index.html`), com o interior da **v11.3** ("altura da sala e banheiro reorganizado"): modelos GLB, tablado da sala e banheiro reorganizado, mais os objetos Poly Haven (frutas, almofadas, cesta etc.).
- Transições de câmera em arco em volta do carro; bancos giratórios recolhem a coluna de direção antes de girar; todos os volumes do interior, inclusive portas abertas e bancos girados, foram conferidos contra a carcaça.
- Motor: three.js r160. O configurador (`site/configurador.html`) carrega os modelos GLB de `site/modelos/` (compressão meshopt). O `site/modelos.json` (os mesmos GLB em base64) só serve às versões antigas em `versoes-anteriores/`.
- Coordenadas do projeto: `s` é a distância da frente (0 a 7 m), `x` a lateral (positivo à esquerda) e `h` a altura a partir do fundo. `W(s,x,h)` converte para o mundo, com VAO de 0,19 m.

### Interior

- **Cabine:** banco do passageiro (`banco_cab`, base giratória), volante e poltronas do motorista e do passageiro.
- **Sala:** banquetas booth fixas e estofadas (não são as poltronas dos bancos da frente). Tablado de 15,5 cm na sala. Assentos a 0,42 m do tablado e tampo a 0,71 m.
- **Banheiro:** chuveiro reposicionado na parede de trás (barra e ducha), vaso ajustado (`modo: livre`, escala Y de 1,17), cortina em trilho no teto e argola de toalha na parede da frente.

### Térmica e fluidos no 3D (itens 11, 30 a 35)

- **Radiador sob medida** (`rad`): módulo de 880 × 175 × 420 mm atrás da tomada de ar, núcleo de 800 × 400 × 66 mm e 2 ventiladores SPAL VA18 de 16″. Substitui a caixa "radiador/chiller".
- **Climatização** (`ac`): 2 Dometic FreshWell 3000 lado a lado sob o painel (no lugar da caixa 71), com os dutos subindo até o painel e 4 grelhas do condensador no fundo (`grelhaCond`). MaxxFan Deluxe no teto traseiro (`maxxfan`, s = 6,37–6,79 m) e grelha de entrada de ar na lateral direita (`grelhaAr`).
- **Bateria** (`bat`): bloco de 1,60 × 1,30 × 0,26 m renomeado para NCM de 203,6 kWh, com as duas camadas de células e as 2 placas frias de 1250 × 1560 × 6 mm.
- **Motor** e **inversor**: Cascadia SS-320-180 com redutor 8:1 (mesmo volume do STL) e CM350SiC. Cabos de fase laranja (`cabosFase`) afastados por presilhas.
- **Películas**: CR 70 nas portas da cabine e CR 30 (vidro mais escuro) na porta de entrada e na janela da sala.
- Posições tiradas da montagem atualizada da pasta Térmica e Fluidos (coordenadas Y = s − 3,5 e Z = h − 1,1). Tudo conferido contra a carcaça e contra as outras peças.

### Pendências

- No STL: renomear o bloco da bateria e incluir as placas frias; atualizar motor e redutor quando o redutor comercial for definido; aumentar a altura da tomada de ar do radiador; abrir o furo de 356 × 356 mm do MaxxFan; traçar cabos de fase e mangueiras e posicionar bombas, válvula de 3 vias e reservatório (no 3D do site eles ainda não aparecem).
- Elétrica: com o cooktop ligado junto com os 2 FreshWell, a demanda passa de 4,3 kW, acima do inversor de 3 kVA. Conferir a contagem de células na K5 da Planilha Geral.
- Vídeo do HyperFrames (projeto `5dc46289-e875-4bce-8ca8-197d01d23a26`) não será refeito.

## Massa e planilha

Fonte: planilha do Google "Inventário de Massas — Motorhome Solar" (exportada em `plan/Inventario_de_Massas_Motorhome_Solar.xlsx`). `mec/massa.py` lê a exportação e chega aos mesmos números da aba Resumo.

| Cenário | Massa | CG do solo | Eixo dianteiro / traseiro |
|---|---|---|---|
| Vazio | 4.225 kg | 0,854 m | 1.783 / 2.442 kg |
| Em ordem de marcha | 4.320 kg | 0,855 m | 1.843 / 2.477 kg |
| Carregado de projeto | 4.738 kg | 0,850 m | 1.921 / 2.817 kg |
| PBT proposto | 5.000 kg | | margem de 262 kg |

- Por subárea: Mecânica 2.080 kg, Elétrica 1.354 kg, Térmica 154 kg, Hidráulica 26 kg, Interiores 548 kg, Acessórios externos 63 kg e Carga útil 514 kg.
- A Térmica foi detalhada conforme o inventário térmico (itens 11 e 30 a 35): 2 FreshWell, radiador, ventiladores, bombas, placas frias, gap filler, fluido, mangueiras, MaxxFan e óleos. As caixas de roda passaram para a parede sanduíche.
- Ainda a acertar (aba Pendências): a linha do motor continua com 202 kg do conjunto anterior, e a caixa do pack (143,2 kg) ainda é a do pack LFP, que incluía uma placa fria.
- `mec/estrut.py`: com o pack de 883 kg (células, caixa, placas frias e gap filler), a longarina chega a 31 MPa (77 MPa com fator 2,5) e 5,4 mm de flecha.
- Isolamento térmico está zerado na planilha porque entra na casca (≈41 kg).
- Ocupantes: 2 × 75 kg no cenário carregado.
- Boiler de 10 L fica no site, não na planilha.

## Próximos passos

1. Fazer no STL os ajustes pendentes da Térmica (lista acima). Depois de mudar a planilha do Google, exportar o xlsx para `plan/` e rodar `python3 mec/massa.py`.
2. Renderização final em Cycles (ver `docs/RENDER_BLENDER.md`), se o vídeo for refeito no Blender.

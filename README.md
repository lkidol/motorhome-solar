# Motorhome elétrico solar

Projeto em grupo da disciplina de Sistemas Térmicos e Fluídicos: um motorhome elétrico com energia solar. Este repositório reúne o site 3D do esquemático, os modelos, os cálculos de massa, a planilha de inventário e os scripts de apoio.

Entrega: 02/12/2026.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/` | Estado do projeto, decisões e roteiro de render no Blender |
| `site/` | Portal do produto e configurador 3D (`index.html`, `configurador.html`, `img/`, `tex/`, `props/`, `modelos/`, JSONs de malha), além de ferramentas de build (`build.py`, `main.js`, `debug.js`, `modelos.json`) e versões anteriores |
| `site/video/` | Vídeo do topo da página (`heroi.webm`, `heroi.mp4` e o pôster `heroi.jpg`) |
| `site/props/` | Objetos decorativos do interior (Poly Haven, CC0) em GLB com malha comprimida (meshopt) e texturas de 512 px embutidas. Só baixam quando alguém olha o interior |
| `site/modelos/` | Modelos GLB do interior (banco da cabine, banqueta da sala, volante, vaso, barra e ducha do chuveiro), carregados pelo configurador |
| `modelos/scripts/` | Scripts de otimização dos GLB (gltf-transform/meshopt) |
| `mec/` | Cálculo de massa e estrutura (`massa.json`, `massa.txt`, `estrut.*`, `casca.*`) |
| `plan/` | `Inventario_de_Massas_Motorhome_Solar.xlsx`: exportação da planilha oficial do Google (Inventário de Massas — Motorhome Solar). `atualiza.py` só gera a versão antiga, com outro nome |
| `geo/` | Geometria da carroceria e do traçado do LED (scripts e dados) |
| `teste/` | Scripts de teste visual e de verificação do interior (Playwright) |
| `ferramentas/` | Patches usados nas versões do site, geração de relevos e o vídeo do topo do site (`filme.js`, `filme.sh`) |
| `dados/` | Dados de referência: `malha.json`, `detalhes.json`, `relevos.json` e `ph_models.json` |

## Como rodar

**Site (local e deploy):** a pasta `site/` é um site estático autocontido. Para rodar localmente, execute `python -m http.server` dentro de `site/` e acesse `http://localhost:8000/`. O deploy em produção publica `./site` automaticamente no Cloudflare Workers Static Assets conforme configurado em `wrangler.jsonc` (e `site/.assetsignore`). Para gerar o build offline legado do esquemático, confira os scripts e históricos em `site/`.

**Desempenho:** a página inicial abre com cerca de 2 MB (vídeo, pôster e fotos visíveis). O 3D embutido só começa a baixar quando a seção dele se aproxima da tela, os objetos do interior só quando alguém entra no carro, e o 3D só redesenha quando algo muda. Ao trocar texturas, mantenha as de `site/tex/` em até 1024 px e as dos objetos em 512 px.

**Planilha:** a fonte é a planilha do Google. Depois de mudá-la, baixe como .xlsx (Arquivo → Fazer download → Microsoft Excel) e substitua `plan/Inventario_de_Massas_Motorhome_Solar.xlsx`.

**Imagens e vídeo do site:** as fotos de `site/img/` saem do próprio configurador. Com o site servido, `configurador.html?shot=<nome>` monta cada cena (lista em `SHOTS`, no fim do arquivo) e o título da página vira `PRONTO` quando a imagem pode ser capturada em 2400 × 1350. O vídeo do topo usa `configurador.html?filme`: o carro fica parado e a estrada corre por baixo, em três tomadas. Para refazê-lo:
```bash
node ferramentas/filme.js /tmp/quadros
```
```bash
ferramentas/filme.sh /tmp/quadros
```
O primeiro grava os quadros (1280 × 720, 30 fps, cerca de uma hora sem GPU); o segundo junta as tomadas com fusões e gera `site/video/heroi.mp4`, `heroi.webm` e o pôster.

**Massas:** `python3 mec/massa.py` lê a aba Materiais do xlsx e refaz os cenários da aba Resumo em `mec/massa.json`; `python3 mec/estrut.py` usa esse arquivo para as longarinas.

## Créditos dos modelos 3D

- NVIDIA SimReady (modelos de interior): licença da NVIDIA.
- Sketchfab: modelos sob CC BY, com autor citado no site.
- 3dassets.dev: CC0.
- DCINTERIOR "BOOTH DOBLE": CC BY.

Confira os autores e licenças de cada modelo na seção "Modelos 3D reais no interior" do site antes de reutilizar os arquivos.

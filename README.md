# Motorhome elétrico solar

Projeto em grupo da disciplina de Sistemas Térmicos e Fluídicos: um motorhome elétrico com energia solar. Este repositório reúne o site 3D do esquemático, os modelos, os cálculos de massa, a planilha de inventário e os scripts de apoio.

Entrega: 02/12/2026.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/` | Estado do projeto, decisões e roteiro de render no Blender |
| `site/` | Código do site 3D publicado (`index.html`, `modelos.json`), fonte do build offline (`build.py`, `main.js`, `debug.js`) e versões anteriores |
| `modelos/` | Modelos GLB do interior (banco, banqueta, volante, vaso, chuveiros) e scripts de otimização (`scripts/`) |
| `mec/` | Cálculo de massa e estrutura (`massa.json`, `massa.txt`, `estrut.*`, `casca.*`) |
| `plan/` | Planilha `Inventario_de_Massas_Motorhome_Solar.xlsx` e o script `atualiza.py` que a regenera |
| `geo/` | Geometria da carroceria e do traçado do LED (scripts e dados) |
| `teste/` | Scripts de teste visual e de verificação do interior (Playwright) |
| `ferramentas/` | Patches usados nas versões do site e geração de relevos |
| `dados/` | Dados de referência: `malha.json`, `detalhes.json`, `relevos.json` e `ph_models.json` |

## Como rodar

**Site offline / local:** dentro de `site/`, `npm install` e depois `python3 build.py` gera `motorhome_solar_3d.html` com os modelos embutidos. `site/index.html` também pode ser servido localmente a partir da raiz do repo (ex.: `python -m http.server`, abrindo `/site/`).

**Planilha:** `python3 plan/atualiza.py` reconstrói a aba Materiais a partir de `plan/original.xlsx`.

**Massas:** `mec/massa.py` gera `mec/massa.json` a partir de `mec/casca.json`.

## Créditos dos modelos 3D

- NVIDIA SimReady (modelos de interior): licença da NVIDIA.
- Sketchfab: modelos sob CC BY, com autor citado no site.
- 3dassets.dev: CC0.
- DCINTERIOR "BOOTH DOBLE": CC BY.

Confira os autores e licenças de cada modelo na seção "Modelos 3D reais no interior" do site antes de reutilizar os arquivos.

# Roteiro de render no Blender (Cycles)

## 1. Preparar
- Blender 4.x ou mais recente.
- Edit > Preferences > System > Cycles Render Devices: ativar a GPU (CUDA, OptiX, HIP ou Metal). Sem GPU, o render roda na CPU, mais lento.
- Salvar o projeto em uma pasta própria, com texturas e modelos junto.

## 2. Importar
- File > Import > glTF 2.0 para cada GLB da pasta `modelos/`.
- Conferir a escala (projeto em metros). Ajustar com N > Item > Scale e aplicar com Ctrl+A > Scale.
- Coleções: `Carroceria`, `Interior`, `Eletrica`, `Solar`, `Luz`, `Camera`.

## 3. Materiais
- Principled BSDF para cada material. Rugosidade e cor base conforme o original.
- Estofado: rugosidade alta e Sheen para aspecto de tecido.
- Fitas de LED e placas solares: Emission com força baixa nas fitas, para não estourar o bloom.

## 4. Iluminação
- HDRI em World > Environment Texture para luz natural e reflexos.
- Sun Light com ângulo baixo para cenas externas.
- Area Lights no teto do interior, cor entre 3000 e 4000 K. Portal em janelas, se houver.
- Evitar luzes pontuais fortes na cabine (reflexos duros nos vidros).

## 5. Câmera e animação
- Lente de 24 a 35 mm no interior e de 35 a 50 mm no exterior.
- Track To apontando para um Empty no centro de interesse.
- Keyframes com interpolação Bezier; Constant Velocity para movimentos lineares.
- Intervalo em Output Properties > Frame Range (ex.: 1 a 600 para 20 s em 30 fps).

## 6. Cycles
- Render Properties: Cycles, Device GPU Compute, Feature Set Supported.
- Sampling: 256 amostras como ponto de partida; 32 ou 64 para teste. Denoise com OpenImageDenoise e Denoising Data ativo.
- Light Paths: Max Bounces 12, Transparent 8 (interiores com vidro); 6 em cenas simples.
- Film > Transparent desativado, salvo se houver composição com fundo.
- Output: 3840 × 2160, 30 fps. Formato PNG de 16 bits em sequência (mais seguro) ou FFmpeg MP4 H.264/H.265 com Quality High e 30 a 50 Mbps.

## 7. Teste antes do final
1. Um frame do meio com 32 amostras.
2. Border Render (Ctrl+B) em áreas específicas (banheiro, sala).
3. Três ou quatro frames de pontos diferentes da animação.
4. Só então aumentar as amostras.

## 8. Render final pela linha de comando
```bash
blender -b motorhome.blend -E CYCLES -s 1 -e 600 -a
```
Para dividir em partes: `-s 1 -e 300` e depois `-s 301 -e 600`.

## 9. Pós-produção
- Sequência PNG: montar no Video Sequence Editor do Blender ou no DaVinci Resolve, a 30 fps.
- Exportar em H.264/H.265 com alta bitrate, ou ProRes para edição.

# Estado do projeto

Última atualização: 19/11/2026.

## Site 3D do esquemático

- Versão atual: **v11.3** ("altura da sala e banheiro reorganizado"), publicada como artefato.
- Motor: three.js r160, com modelos GLB embutidos em base64. Na publicação, os modelos vão em `site/modelos.json`, porque o publicador recusa `.glb`.
- Coordenadas do projeto: `s` é a distância da frente (0 a 7 m), `x` a lateral (positivo à esquerda) e `h` a altura a partir do fundo. `W(s,x,h)` converte para o mundo, com VAO de 0,19 m.

### Interior

- **Cabine:** banco do passageiro (`banco_cab`, base giratória), volante e poltronas do motorista e do passageiro.
- **Sala:** banquetas booth fixas e estofadas (não são as poltronas dos bancos da frente). Tablado de 15,5 cm na sala. Assentos a 0,42 m do tablado e tampo a 0,71 m.
- **Banheiro:** chuveiro reposicionado na parede de trás (barra e ducha), vaso ajustado (`modo: livre`, escala Y de 1,17), cortina em trilho no teto e argola de toalha na parede da frente.

### Pendências

- Itens de cozinha e mesa (frutas etc.) que apareciam em uma versão anterior não estão no código atual. Confirmar em qual versão estavam para restaurar.
- Vídeo do HyperFrames (projeto `5dc46289-e875-4bce-8ca8-197d01d23a26`) não será refeito.

## Massa e planilha

| Cenário | Massa |
|---|---|
| Vazio | 3.940 kg |
| Em ordem de marcha | 4.035 kg |
| Carregado (2 pessoas, bagagem) | 4.454 kg |
| PBT proposto | 5.000 kg |

- Mecânica só estrutural: **1.948 kg**. Na planilha, a subárea Mecânica soma **2.090 kg** (inclui redutor 40, semieixos 18, estrutura das gavetas 74 e carenagem 10).
- **3.080 kg** é o carregado sem bateria, motor, eletrônica e placas solares. Os itens da Elétrica que ficaram fora dessa conta somam cerca de 224 kg. Há uma decisão em aberto sobre realocá-los para Elétrica ou para uma subárea "A definir".
- Isolamento térmico está zerado na planilha porque entra na casca (≈41 kg).
- Ocupantes: 2 × 75 kg no cenário carregado.
- Boiler de 10 L fica no site, não na planilha.

## Próximos passos

1. Decidir o destino dos itens de Elétrica na planilha e regenerar com `plan/scripts/atualiza.py`.
2. Confirmar a versão das frutas e itens de cozinha.
3. Renderização final em Cycles (ver `docs/RENDER_BLENDER.md`), se o vídeo for refeito no Blender.

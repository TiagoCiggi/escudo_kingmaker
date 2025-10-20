# Changelog

## [1.0.0] - 2025-10-14

### Adicionado
- Sistema de encontros aleatórios por zona com base em rolagem de dados.
- Redirecionamento entre tabelas via campo `encontro` numérico.
- Suporte a rolagem especial `1d12+8` para zonas específicas (ex: Colinas Sellen → Fronteiras Nodosas).
- Função `rolar_func` para permitir rolagens personalizadas em chamadas encadeadas.

### Corrigido
- Fluxo de rolagem ajustado para aplicar funções personalizadas corretamente.
- JSON `zona_encontros.json` revisado e padronizado:
  - Campos `quantidade = -1` indicam redirecionamento com rolagem especial.
  - Estrutura de tabelas uniformizada entre zonas.

### Testado
- Simulação completa de encontros na zona "Colinas Sellen" com rolagem 1.
- Verificação de redirecionamento e aplicação correta da rolagem `1d12+8`.


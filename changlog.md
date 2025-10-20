# Changelog

## [1.1.0] - 2025-10-20

### ✨ Adicionado
- Arquivo `encontros.json` com estrutura padronizada:
  - Campo `obs` para observações narrativas.
  - Campo `qtd` para múltiplas quantidades.
  - Campo `inimigo` para nomes reais das criaturas envolvidas.
- Função `confere_obs(criatura, quantidade)` para buscar observações e redefinir inimigos e quantidades com base no JSON.
- Suporte a múltiplos inimigos por encontro, com exibição formatada.
- Atualização da função `teste(zn)` para integrar `confere_obs` e exibir resultados completos.

### 🛠️ Corrigido
- Lógica de `confere_obs` reestruturada para evitar falhas de desempacotamento e garantir retorno consistente.
- Ajuste na função `teste()` para suportar listas de inimigos e quantidades com `zip()`.

### ✅ Testado
- Encontros simulados nas zonas "Correnterra", "Zonaverde" e "Aquadente" com observações narrativas e múltiplos inimigos.
- Validação da integração entre `zona_encontros.json`, `encontros.json` e o sistema de rolagem.

---

## [1.0.0] - 2025-10-14

### ✨ Adicionado
- Sistema de encontros aleatórios por zona com base em rolagem de dados.
- Redirecionamento entre tabelas via campo `encontro` numérico.
- Suporte a rolagem especial `1d12+8` para zonas específicas (ex: Colinas Sellen → Fronteiras Nodosas).
- Função `rolar_func` para permitir rolagens personalizadas em chamadas encadeadas.

### 🛠️ Corrigido
- Fluxo de rolagem ajustado para aplicar funções personalizadas corretamente.
- JSON `zona_encontros.json` revisado e padronizado:
  - Campos `quantidade = -1` indicam redirecionamento com rolagem especial.
  - Estrutura de tabelas uniformizada entre zonas.

### ✅ Testado
- Simulação completa de encontros na zona "Colinas Sellen" com rolagem 1.
- Verificação de redirecionamento e aplicação correta da rolagem `1d12+8`.



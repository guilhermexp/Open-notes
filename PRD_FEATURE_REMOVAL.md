# PRD - Remoção de Funcionalidades do Open WebUI

## 1. VISÃO GERAL

### 1.1 Objetivo
Remover completamente as seguintes funcionalidades do Open WebUI:
- **Workspace** (Espaço de trabalho)
- **Playground** (Área de testes)
- **Evaluations/Arena** (Avaliação de modelos)
- **Ollama Integration** (Toda integração com Ollama)
- **Local AI Models** (Modelos de IA locais armazenados em diretórios)

### 1.2 Escopo
- Remoção completa de todos os arquivos, pastas, componentes e referências
- Garantia de que o funcionamento das demais funcionalidades não seja afetado
- **PRESERVAÇÃO TOTAL da funcionalidade de NOTAS**
- Testes contínuos para validar a integridade do sistema

### 1.3 Princípios de Remoção
1. **Remoção Completa**: Eliminar 100% dos rastros das funcionalidades listadas
2. **Preservação de Integridade**: Não afetar funcionalidades restantes
3. **Proteção de Notas**: Garantir que toda a página e funcionalidade de notas permaneça intacta
4. **Testes Incrementais**: Validar após cada grande remoção
5. **Documentação**: Manter registro de todas as alterações

## 2. ANÁLISE DE IMPACTO

### 2.1 Funcionalidades a Serem PRESERVADAS
- ✅ **NOTAS** (Página completa, editor, salvamento, toda funcionalidade)
- ✅ Chat principal com IA (via OpenAI apenas)
- ✅ Integração com OpenAI
- ✅ Sistema de autenticação
- ✅ Configurações de usuário
- ✅ Admin panel (exceto evaluations)
- ✅ Upload e processamento de documentos
- ✅ Sistema de mensagens e histórico

### 2.2 Riscos Identificados
| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Quebra de rotas | Média | Alto | Testes após cada remoção |
| Imports órfãos | Alta | Médio | Busca e remoção sistemática |
| Estado inconsistente | Baixa | Alto | Limpeza de stores |
| Erro de build | Média | Alto | Build incremental |

## 3. PLANO DE EXECUÇÃO

### 3.1 Fase 1: Backend - Remoção de APIs e Modelos
**Objetivo**: Remover toda lógica de backend relacionada

#### Ações:
1. **Rollback de Migrações**
   ```bash
   cd backend
   alembic downgrade af906e964978  # Remove feedback table
   ```

2. **Remoção de Arquivos - Workspace/Playground/Evaluations**
   ```bash
   rm backend/open_webui/routers/evaluations.py
   rm backend/open_webui/routers/models.py
   rm backend/open_webui/routers/knowledge.py
   rm backend/open_webui/routers/prompts.py
   rm backend/open_webui/routers/tools.py
   rm backend/open_webui/models/feedbacks.py
   ```

3. **Remoção de Arquivos - Ollama**
   ```bash
   rm backend/open_webui/routers/ollama.py  # 1,846 linhas de integração
   rm update_ollama_models.sh
   ```

4. **Limpeza de Configurações**
   - Arquivo: `/backend/open_webui/config.py`
   - Remover: Variáveis de workspace e evaluation
   - Remover: ENABLE_OLLAMA_API, OLLAMA_API_BASE_URL, OLLAMA_BASE_URL, OLLAMA_BASE_URLS, OLLAMA_API_CONFIGS
   - Remover: RAG_OLLAMA_BASE_URL, RAG_OLLAMA_API_KEY

5. **Atualização de Rotas Principais**
   - Arquivo: `/backend/open_webui/main.py`
   - Remover: Import ollama (linha 66)
   - Remover: app.include_router(ollama.router) (linha 1201)
   - Remover: Referências RAG embedding ollama (linhas 941, 950)

6. **IMPORTANTE - Arquivos a PRESERVAR**
   ```
   ✅ MANTER: backend/open_webui/routers/notes.py
   ✅ MANTER: backend/open_webui/models/notes.py
   ✅ MANTER: backend/open_webui/migrations/versions/9f0c9cd09105_add_note_table.py
   ```

**Teste**: Reiniciar backend e verificar logs

### 3.2 Fase 2: Frontend - Remoção de Rotas
**Objetivo**: Eliminar todas as páginas relacionadas

#### Ações:
1. **Deletar Diretórios de Rotas**
   ```bash
   rm -rf src/routes/\(app\)/workspace/
   rm -rf src/routes/\(app\)/playground/
   rm -rf src/routes/\(app\)/admin/evaluations/
   ```

2. **IMPORTANTE - Rotas a PRESERVAR**
   ```
   ✅ MANTER: src/routes/(app)/notes/
   ✅ MANTER: src/routes/(app)/notes/+layout.svelte
   ✅ MANTER: src/routes/(app)/notes/+page.svelte
   ✅ MANTER: src/routes/(app)/notes/[id]/+page.svelte
   ```

**Teste**: `npm run build` deve passar sem erros

### 3.3 Fase 3: Frontend - Remoção de Componentes
**Objetivo**: Eliminar componentes UI relacionados

#### Ações:
1. **Deletar Diretórios de Componentes - Workspace/Playground/Evaluations**
   ```bash
   rm -rf src/lib/components/workspace/
   rm -rf src/lib/components/playground/
   rm src/lib/components/admin/Evaluations.svelte
   rm -rf src/lib/components/admin/Evaluations/
   rm -rf src/lib/components/admin/Settings/Evaluations/
   ```

2. **Deletar APIs do Frontend**
   ```bash
   rm -rf src/lib/apis/evaluations/
   rm -rf src/lib/apis/ollama/  # Remover toda API do Ollama
   ```

3. **IMPORTANTE - Componentes a PRESERVAR**
   ```
   ✅ MANTER: src/lib/components/notes/
   ✅ MANTER: src/lib/components/notes/Notes.svelte
   ✅ MANTER: src/lib/components/notes/NotePanel.svelte
   ✅ MANTER: src/lib/components/notes/NoteEditor.svelte
   ✅ MANTER: src/lib/components/notes/NoteEditor/*
   ✅ MANTER: src/lib/apis/notes/
   ```

**Teste**: Verificar console por erros de import

### 3.4 Fase 4: Limpeza de Navegação
**Objetivo**: Remover links e menus

#### Ações:
1. **Sidebar Principal**
   - Arquivo: `/src/lib/components/layout/Sidebar.svelte`
   - Remover: Links de workspace (linhas 609-643)
   - Remover: Verificações de permissão (linhas 792-822)

2. **Menu de Usuário**
   - Arquivo: `/src/lib/components/layout/Sidebar/UserMenu.svelte`
   - Remover: Link do playground

**Teste**: Navegação deve funcionar sem erros 404

### 3.5 Fase 5: Limpeza de Estado
**Objetivo**: Limpar stores e tipos

#### Ações:
1. **Store Principal**
   - Arquivo: `/src/lib/stores/index.ts`
   - Remover: Variáveis de prompts, knowledge, tools
   - Remover: Tipos Prompt e Document
   - Atualizar: Tipo owned_by para remover 'arena'

**Teste**: Estado da aplicação deve funcionar corretamente

### 3.6 Fase 6: Busca e Limpeza Final
**Objetivo**: Garantir remoção completa

#### Ações:
1. **Buscar Referências Restantes**
   ```bash
   # Frontend
   grep -r "workspace" src/ --exclude-dir=node_modules
   grep -r "playground" src/ --exclude-dir=node_modules
   grep -r "evaluation" src/ --exclude-dir=node_modules
   grep -r "arena" src/ --exclude-dir=node_modules
   grep -r "feedback" src/ --exclude-dir=node_modules
   grep -r "ollama" src/ --exclude-dir=node_modules
   
   # Backend
   grep -r "workspace" backend/ --exclude-dir=__pycache__
   grep -r "playground" backend/ --exclude-dir=__pycache__
   grep -r "evaluation" backend/ --exclude-dir=__pycache__
   grep -r "feedback" backend/ --exclude-dir=__pycache__
   grep -r "ollama" backend/ --exclude-dir=__pycache__
   ```

2. **Verificar que NOTAS está funcionando**
   ```bash
   # Verificar arquivos de notas existem
   ls -la src/routes/\(app\)/notes/
   ls -la src/lib/components/notes/
   ls -la src/lib/apis/notes/
   ls -la backend/open_webui/routers/notes.py
   ls -la backend/open_webui/models/notes.py
   ```

2. **Corrigir Imports Quebrados**
   - Remover ou comentar imports órfãos
   - Atualizar referências necessárias

**Teste**: Build completo e execução

## 4. CRITÉRIOS DE ACEITAÇÃO

### 4.1 Funcionalidades Removidas
- [ ] Nenhuma rota `/workspace/*` acessível
- [ ] Nenhuma rota `/playground/*` acessível
- [ ] Nenhuma rota `/admin/evaluations/*` acessível
- [ ] Nenhuma integração com Ollama presente
- [ ] Nenhum menu ou link para funcionalidades removidas
- [ ] Nenhum componente relacionado presente no código

### 4.2 Integridade do Sistema - DEVE FUNCIONAR
- [ ] **NOTAS funcionando perfeitamente** (criar, editar, salvar, deletar)
- [ ] Chat principal funcionando normalmente (via OpenAI)
- [ ] Upload de documentos funcionando
- [ ] Integração com OpenAI funcionando
- [ ] Sistema de autenticação funcionando
- [ ] Configurações de admin funcionando (exceto evaluations)

### 4.3 Qualidade do Código
- [ ] Build do frontend sem erros
- [ ] Backend iniciando sem erros
- [ ] Nenhum erro no console do navegador
- [ ] Nenhum import quebrado
- [ ] Nenhuma referência órfã

## 5. TESTES DE VALIDAÇÃO

### 5.1 Testes Unitários
```bash
# Frontend
npm run build
npm run check

# Backend
cd backend
python -m pytest
```

### 5.2 Testes de Integração
1. **TESTE CRÍTICO - NOTAS**
   - Acessar /notes
   - Criar nova nota
   - Editar conteúdo da nota
   - Salvar nota
   - Listar notas existentes
   - Deletar nota
   - Verificar persistência

2. **Teste de Chat**
   - Criar nova conversa
   - Enviar mensagem (via OpenAI)
   - Receber resposta
   - Salvar histórico

3. **Teste de Upload**
   - Upload de documento
   - Processamento
   - Busca no documento

4. **Teste de Configurações**
   - Acessar configurações de usuário
   - Modificar configurações
   - Salvar alterações

### 5.3 Testes de Regressão
- Verificar todas as funcionalidades principais
- Confirmar que nada foi quebrado inadvertidamente

## 6. ROLLBACK

### 6.1 Estratégia de Rollback
Em caso de problemas críticos:
1. Git revert dos commits de remoção
2. Restaurar backup do banco de dados
3. Rebuild da aplicação

### 6.2 Pontos de Checkpoint
- Criar branch antes de iniciar: `git checkout -b feature-removal-backup`
- Commit após cada fase concluída
- Tag de versão antes da remoção: `git tag pre-removal-v1.0`

## 7. MÉTRICAS DE SUCESSO

### 7.1 Métricas Técnicas
- ✅ 100% das funcionalidades alvo removidas
- ✅ 0 erros de build
- ✅ 0 erros de runtime relacionados
- ✅ Redução no tamanho do bundle (estimado: 15-20%)

### 7.2 Métricas de Performance
- Tempo de build reduzido
- Menor uso de memória
- Inicialização mais rápida

## 8. DOCUMENTAÇÃO FINAL

### 8.1 Documentos a Atualizar
- README.md - remover menções às funcionalidades
- Documentação de API - remover endpoints deletados
- Guia de usuário - atualizar screenshots e instruções

### 8.2 Changelog
Criar entrada no CHANGELOG.md:
```markdown
## [Version] - [Date]
### Removed
- Workspace functionality (models, knowledge, prompts, tools)
- Playground testing interface
- Model evaluation and arena features
- Related API endpoints and database models
```

## 9. APROVAÇÃO

### Stakeholders
- [ ] Desenvolvedor Principal
- [ ] QA/Testes
- [ ] DevOps

### Sign-off
- Data de Início: ___________
- Data de Conclusão: ___________
- Aprovado por: ___________

---

**Documento criado em**: [Data]
**Última atualização**: [Data]
**Status**: Em Execução
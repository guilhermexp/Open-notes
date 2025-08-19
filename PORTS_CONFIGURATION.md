# Configuração de Portas - Open Notes

## Portas Padronizadas

### Produção/Desenvolvimento
- **Frontend (Vite/SvelteKit)**: `8357`
- **Backend (FastAPI/Uvicorn)**: `36950`

### URLs de Acesso
- **Frontend**: http://localhost:8357
- **Backend API**: http://localhost:36950
- **Health Check**: http://localhost:36950/health
- **API Docs**: http://localhost:36950/docs

## Arquivos de Configuração

### 1. `.env` (raiz do projeto)
```env
PUBLIC_API_BASE_URL=http://localhost:36950
PUBLIC_APP_URL=http://localhost:8357
```

### 2. `backend/.env`
```env
PORT=36950
HOST=0.0.0.0
CORS_ALLOW_ORIGIN=http://localhost:8357
```

### 3. `vite.config.ts`
- Porta do frontend: `8357`
- Proxy para backend: `http://localhost:36950`

### 4. `start.sh`
- Kill de processos nas portas: `8357` e `36950`
- Backend inicia em: `36950`
- Frontend inicia em: `8357`

### 5. `src/lib/constants.ts`
- Importa `PUBLIC_API_BASE_URL` do ambiente
- Fallback para porta `36950` em desenvolvimento

## Comandos de Verificação

```bash
# Verificar se as portas estão em uso
lsof -i:8357   # Frontend
lsof -i:36950  # Backend

# Matar processos nas portas (se necessário)
kill -9 $(lsof -ti:8357)
kill -9 $(lsof -ti:36950)

# Iniciar aplicação
npm run dev
```

## Troubleshooting

### Erro: "Backend Open WebUI necessário"
- Verifique se `PUBLIC_API_BASE_URL` está configurado no `.env`
- Confirme que o backend está rodando na porta `36950`
- Recarregue a página após mudanças no `.env`

### Erro: "Connection Refused"
- Backend não está rodando
- Execute `npm run dev` para iniciar ambos os servidores
- Verifique os logs do backend no terminal

### Portas em Conflito
- Use `lsof -i:PORTA` para identificar processos
- Mate processos antigos antes de reiniciar
- O `start.sh` já faz isso automaticamente

## Histórico de Portas (para referência)

### Portas Antigas (não usar mais)
- ~~8000~~ → Mudado para 36950 (backend)
- ~~8080~~ → Mudado para 8357 (frontend)
- ~~3000~~ → Mudado para 8357 (frontend)
- ~~5173~~ → Mudado para 8357 (frontend/Vite padrão)

## Notas Importantes

1. **Sempre use as portas padronizadas** para evitar conflitos
2. **Não commitar** arquivos `.env` com dados sensíveis
3. **Reinicie o servidor** após mudanças no `.env`
4. **Vite HMR** funciona automaticamente com mudanças no código
5. **Backend** recarrega automaticamente com `--reload` flag

---
*Última atualização: 2025-08-18*
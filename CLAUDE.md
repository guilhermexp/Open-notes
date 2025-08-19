[byterover-mcp]

# important 
always use byterover-retrive-knowledge tool to get the related context before any tasks 
always use byterover-store-knowledge to store all the critical informations after sucessful tasks
# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

# CLAUDE.md - Open Notes Project Context

## 🎯 Project Overview

Open Notes is a fork of Open WebUI focused on notes and documentation, with dual-server architecture (SvelteKit frontend + FastAPI backend).

## 🏗️ Architecture

### Dual-Server Setup
- **Frontend**: Vite/SvelteKit on port 8357
- **Backend**: FastAPI/Uvicorn on port 36950
- **Startup**: Unified via `start.sh` script

### Key Technologies
- **Frontend**: SvelteKit 2.0, TypeScript, TailwindCSS, TipTap editor
- **Backend**: FastAPI, Python 3.12, SQLite, SQLAlchemy
- **Authentication**: JWT tokens with WEBUI_AUTH=true

## 🚀 Common Commands

```bash
# Start both servers (recommended)
npm run dev

# Frontend only
npm run dev:frontend-only

# Backend only
cd backend && uvicorn open_webui.main:app --reload --port 36950

# Build for production
npm run build

# Run tests
npm run test:frontend

# Lint and format
npm run lint
npm run format
```

## 🔧 Key Configuration Files

### backend/.env
```env
PORT=36950
WEBUI_AUTH=true
ENABLE_OPENAI_API=true
OPENAI_API_KEY=sk-proj-...
```

### start.sh
- Manages both servers
- Auto-detects Python version
- Handles port conflicts
- Line 103: `export WEBUI_AUTH=true`

## 🐛 Known Issues & Fixes

### 1. Authentication Issues
**Problem**: "Can't turn off authentication" error
**Solution**: Ensure `WEBUI_AUTH=true` in:
- `backend/.env`
- `start.sh` line 103

### 2. TipTap Extension Conflicts
**Problem**: Duplicate extension errors
**File**: `src/lib/components/common/RichTextInput.svelte`
**Solution**: Disable conflicting extensions in StarterKit:
```javascript
StarterKit.configure({
    bulletList: false,
    orderedList: false,
    listItem: false,
    listKeymap: false,
    codeBlock: false
})
```

### 3. Component Destruction Errors
**Problem**: "fn is not a function" during cleanup
**Files**: 
- `src/app.html` - Global error suppressor
- Components with proper cleanup handlers

### 4. Chat Rendering Issue (Critical)
**Problem**: Blank screen after sending first message
**File**: `src/lib/components/chat/Chat.svelte`
**Solution**: Use SvelteKit's goto() instead of window.history.replaceState:
```javascript
// Replace this:
window.history.replaceState(history.state, '', `/c/${_chatId}`);

// With this:
await goto(`/c/${_chatId}`, { 
    replaceState: true,
    invalidateAll: true 
});
```

## 📁 Important Files

### Frontend Components
- `src/lib/components/chat/Chat.svelte` - Main chat component
- `src/lib/components/chat/MessageInput.svelte` - Message input handler
- `src/lib/components/common/RichTextInput.svelte` - TipTap editor
- `src/lib/components/notes/Notes.svelte` - Notes functionality

### Backend Core
- `backend/open_webui/main.py` - FastAPI application
- `backend/open_webui/routers/` - API endpoints
- `backend/open_webui/models/` - Database models

### Configuration
- `start.sh` - Startup orchestration
- `backend/.env` - Environment variables
- `package.json` - npm scripts and dependencies

## 🔍 Debugging Tips

### Check Server Status
```bash
# Frontend port
lsof -i:8357

# Backend port
lsof -i:36950

# Backend logs
tail -f backend/logs/*.log
```

### Common Debug Points
1. **Chat navigation**: Check `goto()` calls in Chat.svelte
2. **Authentication**: Verify token in localStorage
3. **API calls**: Check network tab for 401/403 errors
4. **Component errors**: Check browser console for destruction errors

## ⚠️ Critical Areas

1. **Navigation System**: Chat routing uses SvelteKit's `goto()` with `invalidateAll`
2. **Authentication Flow**: JWT tokens stored in localStorage
3. **Error Suppression**: Global handlers in app.html
4. **Port Management**: Fixed ports to avoid conflicts

## 📝 Development Workflow

1. **Start Development**:
   ```bash
   npm run dev
   ```

2. **Access Applications**:
   - Frontend: http://localhost:8357
   - Backend API: http://localhost:36950

3. **Monitor Logs**:
   - Frontend: Browser console
   - Backend: Terminal output

4. **Hot Reload**:
   - Frontend: Automatic (Vite)
   - Backend: Automatic (Uvicorn --reload)

## 🚨 Troubleshooting Checklist

- [ ] WEBUI_AUTH=true in both .env and start.sh?
- [ ] Ports 8357 and 36950 available?
- [ ] Python 3.12 installed and active?
- [ ] Node.js >= 18 installed?
- [ ] All npm dependencies installed?
- [ ] Backend virtual environment activated?
- [ ] Database migrations applied?

## 📚 Additional Documentation

- `QUICK_START.md` - 5-minute setup guide
- `DEVELOPMENT_GUIDE.md` - Comprehensive development guide
- `FIXES_DOCUMENTATION.md` - Technical documentation of all fixes
- `README.md` - Project overview and installation

## 🔗 Key Dependencies

### Frontend
- svelte: ^4.2.18
- @sveltejs/kit: ^2.5.20
- @tiptap/starter-kit: ^3.0.7
- vite: ^5.4.14

### Backend
- fastapi
- uvicorn
- sqlalchemy
- python-jose[cryptography]
- passlib[bcrypt]

## 💡 Tips for Future Development

1. **Always test chat creation** - Most critical user flow
2. **Use SvelteKit navigation** - Never use window.history directly
3. **Check error suppressors** - May hide real issues
4. **Monitor both servers** - Frontend and backend must be in sync
5. **Respect authentication** - WEBUI_AUTH=true is required

---

*Last updated: 2025-08-16*
*Open Notes Version: 1.0.1*
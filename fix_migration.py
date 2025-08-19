#!/usr/bin/env python3
"""
Script para corrigir a migração das notas do open-notesUI.
Reprocessa as notas para garantir que o conteúdo seja migrado corretamente.
"""

import sqlite3
import json
from datetime import datetime

def fix_migration():
    print("=" * 70)
    print("🔧 CORREÇÃO DA MIGRAÇÃO DE NOTAS")
    print("=" * 70)
    
    # Paths
    source_db = "/Users/guilhermevarela/Documents/Repositorios/open-notesUI/backend/data/webui.db"
    target_db = "backend/data/webui.db"
    
    # Conectar aos bancos
    source_conn = sqlite3.connect(source_db)
    source_cursor = source_conn.cursor()
    
    target_conn = sqlite3.connect(target_db)
    target_cursor = target_conn.cursor()
    
    # Pegar o user_id correto
    target_cursor.execute("SELECT id FROM user WHERE email LIKE '%guilherme%' LIMIT 1")
    user_result = target_cursor.fetchone()
    if not user_result:
        print("❌ Usuário não encontrado!")
        return
    
    user_id = user_result[0]
    print(f"👤 Usuário: {user_id}")
    
    # Buscar notas do banco de origem que tenham conteúdo
    source_cursor.execute("""
        SELECT id, title, data, meta, created_at, updated_at 
        FROM note 
        WHERE data IS NOT NULL AND data != ''
    """)
    source_notes = source_cursor.fetchall()
    
    print(f"\n📚 {len(source_notes)} notas com conteúdo encontradas no banco origem")
    
    updated = 0
    errors = 0
    
    for note_id, title, data_str, meta_str, created_at, updated_at in source_notes:
        try:
            # Parse do data original
            if data_str:
                data = json.loads(data_str)
                
                # Verificar se tem conteúdo
                has_content = False
                content_data = {}
                
                # Extrair conteúdo do formato antigo
                if 'content' in data:
                    # Se já tem content estruturado
                    content = data['content']
                    if isinstance(content, dict):
                        content_data = content
                        has_content = bool(content.get('md') or content.get('html') or content.get('json'))
                    elif isinstance(content, str):
                        # Se content é uma string simples
                        content_data = {'md': content}
                        has_content = True
                elif 'md' in data or 'html' in data or 'json' in data:
                    # Se o conteúdo está direto no data
                    if 'md' in data:
                        content_data['md'] = data['md']
                    if 'html' in data:
                        content_data['html'] = data['html']
                    if 'json' in data:
                        content_data['json'] = data['json']
                    has_content = True
                
                if has_content:
                    # Estrutura correta para o Open Notes
                    new_data = {
                        'content': content_data,
                        'tags': data.get('tags', [])
                    }
                    
                    # Verificar se a nota já existe no destino
                    target_cursor.execute("SELECT id FROM note WHERE id = ?", (note_id,))
                    exists = target_cursor.fetchone()
                    
                    if exists:
                        # Atualizar nota existente
                        target_cursor.execute("""
                            UPDATE note 
                            SET data = ?, user_id = ?
                            WHERE id = ?
                        """, (json.dumps(new_data), user_id, note_id))
                    else:
                        # Inserir nova nota
                        meta = json.loads(meta_str) if meta_str else {}
                        target_cursor.execute("""
                            INSERT INTO note (id, user_id, title, data, meta, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            note_id,
                            user_id,
                            title,
                            json.dumps(new_data),
                            json.dumps(meta),
                            created_at,
                            updated_at
                        ))
                    
                    updated += 1
                    print(f"  ✅ {title[:50]}...")
                    
        except Exception as e:
            errors += 1
            print(f"  ❌ Erro em '{title}': {e}")
    
    target_conn.commit()
    
    # Verificar o resultado
    print(f"\n📊 Resumo:")
    print(f"  ✅ {updated} notas atualizadas/criadas")
    print(f"  ❌ {errors} erros")
    
    # Teste específico
    target_cursor.execute("""
        SELECT title, json_extract(data, '$.content.md') 
        FROM note 
        WHERE title LIKE '%Variáveis%' 
        LIMIT 1
    """)
    test = target_cursor.fetchone()
    if test:
        print(f"\n🔍 Teste - '{test[0]}':")
        content = test[1]
        if content:
            print(f"  ✅ Conteúdo encontrado: {len(content)} caracteres")
            print(f"  📝 Início: {content[:100]}...")
        else:
            print(f"  ❌ Sem conteúdo!")
    
    source_conn.close()
    target_conn.close()
    print("\n✅ Correção concluída!")

if __name__ == "__main__":
    fix_migration()
#!/usr/bin/env python3
"""
Script para corrigir o conteúdo das notas migradas.
As notas foram migradas mas o conteúdo não está sendo exibido corretamente.
"""

import sqlite3
import json
from datetime import datetime

def fix_notes_content():
    # Conectar ao banco de dados do Open Notes
    db_path = "backend/data/webui.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Corrigindo conteúdo das notas...")
    
    # Buscar todas as notas
    cursor.execute("SELECT id, title, data FROM note")
    notes = cursor.fetchall()
    
    fixed_count = 0
    
    for note_id, title, data_str in notes:
        try:
            # Parse do JSON atual
            if data_str:
                data = json.loads(data_str)
                
                # Se já tem o campo content estruturado corretamente, pular
                if 'content' in data and isinstance(data['content'], dict):
                    if 'md' in data['content'] or 'html' in data['content'] or 'json' in data['content']:
                        # Já está no formato correto
                        continue
                
                # Se o data tem diretamente md, html ou json, reestruturar
                if 'md' in data or 'html' in data or 'json' in data:
                    # Criar estrutura content correta
                    content = {}
                    if 'md' in data:
                        content['md'] = data['md']
                    if 'html' in data:
                        content['html'] = data['html']
                    if 'json' in data:
                        content['json'] = data['json']
                    
                    # Atualizar a estrutura data
                    new_data = {
                        'content': content,
                        'tags': data.get('tags', [])
                    }
                    
                    # Atualizar no banco
                    cursor.execute(
                        "UPDATE note SET data = ? WHERE id = ?",
                        (json.dumps(new_data), note_id)
                    )
                    fixed_count += 1
                    print(f"  ✅ Corrigido: {title[:50]}...")
                
        except Exception as e:
            print(f"  ❌ Erro ao processar nota {title}: {e}")
    
    conn.commit()
    print(f"\n✅ {fixed_count} notas corrigidas!")
    
    # Verificar uma nota específica
    cursor.execute("SELECT data FROM note WHERE title = 'Variáveis de Ambiente'")
    result = cursor.fetchone()
    if result:
        data = json.loads(result[0])
        if 'content' in data:
            print("\n📝 Estrutura da nota 'Variáveis de Ambiente' após correção:")
            print(f"  - Tem content: {'content' in data}")
            if 'content' in data:
                print(f"  - Tem content.md: {'md' in data['content']}")
                print(f"  - Tamanho do content.md: {len(data['content'].get('md', ''))} caracteres")
    
    conn.close()

if __name__ == "__main__":
    fix_notes_content()
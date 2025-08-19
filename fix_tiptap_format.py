#!/usr/bin/env python3
"""
Script para converter o conteúdo das notas para o formato exato do TipTap.
Ao invés de criar JSON manualmente, vamos deixar o conteúdo HTML/MD 
e deixar o TipTap processar quando carregar.
"""

import sqlite3
import json
from datetime import datetime

def fix_tiptap_format():
    print("=" * 70)
    print("🔧 AJUSTANDO FORMATO PARA TIPTAP")
    print("=" * 70)
    
    # Conectar ao banco
    db_path = "backend/data/webui.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar todas as notas com conteúdo
    cursor.execute("""
        SELECT id, title, data 
        FROM note 
        WHERE data IS NOT NULL
    """)
    notes = cursor.fetchall()
    
    print(f"\n📚 {len(notes)} notas encontradas")
    
    updated = 0
    errors = 0
    
    for note_id, title, data_str in notes:
        try:
            data = json.loads(data_str)
            
            # Verificar se tem conteúdo
            if 'content' in data and isinstance(data['content'], dict):
                content = data['content']
                needs_update = False
                
                # Se tem MD mas não tem HTML, criar HTML básico
                if content.get('md') and not content.get('html'):
                    # Converter markdown para HTML básico
                    md_text = content['md']
                    # Escapar HTML e preservar quebras de linha
                    html_text = md_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html_text = html_text.replace('\n\n', '</p><p>').replace('\n', '<br>')
                    content['html'] = f'<p>{html_text}</p>'
                    needs_update = True
                
                # Para o TipTap, vamos definir json como null inicialmente
                # O editor vai processar o HTML quando carregar
                if content.get('html') or content.get('md'):
                    # Definir json como null para forçar o TipTap a processar o HTML
                    content['json'] = None
                    needs_update = True
                
                if needs_update:
                    data['content'] = content
                    
                    # Atualizar no banco
                    cursor.execute(
                        "UPDATE note SET data = ? WHERE id = ?",
                        (json.dumps(data), note_id)
                    )
                    updated += 1
                    print(f"  ✅ {title[:50]}...")
                    
        except Exception as e:
            errors += 1
            print(f"  ❌ Erro em '{title}': {e}")
    
    conn.commit()
    
    print(f"\n📊 Resumo:")
    print(f"  ✅ {updated} notas ajustadas")
    print(f"  ❌ {errors} erros")
    
    # Verificar a nota de teste
    cursor.execute("""
        SELECT title, data
        FROM note 
        WHERE title LIKE '%Variáveis%' 
        LIMIT 1
    """)
    test = cursor.fetchone()
    if test:
        title, data_str = test
        data = json.loads(data_str)
        print(f"\n🔍 Teste - '{title}':")
        if 'content' in data:
            content = data['content']
            print(f"  JSON: {content.get('json')}")
            print(f"  MD: {len(content.get('md', ''))} caracteres")
            print(f"  HTML: {len(content.get('html', ''))} caracteres")
            if content.get('html'):
                print(f"  HTML preview: {content['html'][:200]}...")
    
    conn.close()
    print("\n✅ Ajuste concluído!")

if __name__ == "__main__":
    fix_tiptap_format()
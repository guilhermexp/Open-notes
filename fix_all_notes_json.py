#!/usr/bin/env python3
"""
Script completo para garantir que TODAS as notas tenham o campo JSON.
"""

import sqlite3
import json
from datetime import datetime
import re

def markdown_to_html(md_content):
    """Converte markdown básico para HTML"""
    if not md_content:
        return ""
    
    # Converter quebras de linha em parágrafos
    html = md_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
    html = f'<p>{html}</p>'
    
    # Converter headers básicos
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    return html

def create_tiptap_json_from_md(md_content):
    """
    Cria uma estrutura JSON do TipTap a partir do conteúdo markdown.
    """
    if not md_content:
        return {
            "type": "doc",
            "content": []
        }
    
    lines = md_content.split('\n')
    content = []
    
    for line in lines:
        if not line.strip():
            continue
            
        # Headers
        if line.startswith('### '):
            content.append({
                "type": "heading",
                "attrs": {"level": 3},
                "content": [{"type": "text", "text": line[4:].strip()}]
            })
        elif line.startswith('## '):
            content.append({
                "type": "heading",
                "attrs": {"level": 2},
                "content": [{"type": "text", "text": line[3:].strip()}]
            })
        elif line.startswith('# '):
            content.append({
                "type": "heading",
                "attrs": {"level": 1},
                "content": [{"type": "text", "text": line[2:].strip()}]
            })
        # Lists
        elif line.startswith('- '):
            content.append({
                "type": "bulletList",
                "content": [{
                    "type": "listItem",
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": line[2:].strip()}]
                    }]
                }]
            })
        # Regular paragraphs
        else:
            content.append({
                "type": "paragraph",
                "content": [{"type": "text", "text": line}]
            })
    
    if not content:
        content = [{
            "type": "paragraph",
            "content": []
        }]
    
    return {
        "type": "doc",
        "content": content
    }

def fix_all_notes():
    print("=" * 70)
    print("🔧 GARANTINDO JSON PARA TODAS AS NOTAS")
    print("=" * 70)
    
    # Conectar ao banco
    db_path = "backend/data/webui.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar TODAS as notas
    cursor.execute("""
        SELECT id, title, data 
        FROM note
    """)
    notes = cursor.fetchall()
    
    print(f"\n📚 {len(notes)} notas encontradas no total")
    
    updated = 0
    already_ok = 0
    errors = 0
    
    for note_id, title, data_str in notes:
        try:
            if not data_str:
                # Criar estrutura vazia
                data = {
                    'content': {
                        'json': {"type": "doc", "content": []},
                        'html': '',
                        'md': ''
                    },
                    'tags': []
                }
                cursor.execute(
                    "UPDATE note SET data = ? WHERE id = ?",
                    (json.dumps(data), note_id)
                )
                updated += 1
                print(f"  ✅ {title[:50]}... - Estrutura criada do zero")
                continue
            
            data = json.loads(data_str)
            
            # Garantir que tem a estrutura content
            if 'content' not in data:
                data['content'] = {}
            
            # Se não é um dicionário, converter
            if not isinstance(data['content'], dict):
                data['content'] = {}
            
            content = data['content']
            needs_update = False
            
            # Garantir que tem md
            if 'md' not in content:
                content['md'] = ''
                needs_update = True
            
            # Garantir que tem html
            if 'html' not in content or not content['html']:
                if content.get('md'):
                    content['html'] = markdown_to_html(content['md'])
                else:
                    content['html'] = ''
                needs_update = True
            
            # Garantir que tem json
            if 'json' not in content or not content['json']:
                if content.get('md'):
                    content['json'] = create_tiptap_json_from_md(content['md'])
                else:
                    content['json'] = {"type": "doc", "content": []}
                needs_update = True
            
            if needs_update:
                # Garantir estrutura completa
                data['content'] = content
                if 'tags' not in data:
                    data['tags'] = []
                
                # Atualizar no banco
                cursor.execute(
                    "UPDATE note SET data = ? WHERE id = ?",
                    (json.dumps(data), note_id)
                )
                updated += 1
                print(f"  ✅ {title[:50]}... - Atualizado")
            else:
                already_ok += 1
                    
        except Exception as e:
            errors += 1
            print(f"  ❌ Erro em '{title}': {e}")
    
    conn.commit()
    
    # Resumo final
    print(f"\n📊 Resumo Final:")
    print(f"  ✅ {updated} notas atualizadas")
    print(f"  ✓  {already_ok} notas já estavam OK")
    print(f"  ❌ {errors} erros")
    print(f"  📝 Total processado: {updated + already_ok + errors}/{len(notes)}")
    
    # Verificar algumas notas específicas
    print(f"\n🔍 Verificação de amostras:")
    cursor.execute("""
        SELECT title, 
               json_extract(data, '$.content.json') as json_content,
               json_extract(data, '$.content.md') as md_content,
               json_extract(data, '$.content.html') as html_content
        FROM note 
        WHERE json_extract(data, '$.content.md') IS NOT NULL 
           AND json_extract(data, '$.content.md') != ''
        LIMIT 5
    """)
    samples = cursor.fetchall()
    
    for title, json_c, md_c, html_c in samples:
        has_json = "✅" if json_c else "❌"
        has_md = "✅" if md_c else "❌"
        has_html = "✅" if html_c else "❌"
        
        md_len = len(md_c) if md_c else 0
        html_len = len(html_c) if html_c else 0
        json_len = len(json.dumps(json_c)) if json_c else 0
        
        print(f"  📄 {title[:30]:30} | JSON:{has_json}({json_len:5}) | MD:{has_md}({md_len:5}) | HTML:{has_html}({html_len:5})")
    
    conn.close()
    print("\n✅ Processamento concluído!")

if __name__ == "__main__":
    fix_all_notes()
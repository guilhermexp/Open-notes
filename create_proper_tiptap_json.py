#!/usr/bin/env python3
"""
Script para criar JSON válido do TipTap baseado no conteúdo HTML existente.
"""

import sqlite3
import json
from datetime import datetime
import re

def html_to_tiptap_json(html_content):
    """
    Converte HTML em JSON do TipTap de forma mais completa.
    """
    if not html_content:
        return {
            "type": "doc",
            "content": []
        }
    
    # Para simplificar, vamos criar um documento básico
    # O TipTap vai processar melhor quando o editor carregar
    doc = {
        "type": "doc",
        "content": []
    }
    
    # Se tem conteúdo HTML, adicionar como um único bloco por enquanto
    # O editor vai reformatar quando processar
    if html_content.strip():
        # Remover tags HTML básicas para extrair texto
        text = re.sub(r'<[^>]+>', '', html_content)
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        
        # Dividir em parágrafos
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            if para.strip():
                doc["content"].append({
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": para.strip()
                        }
                    ]
                })
    
    # Se ainda não tem conteúdo, adicionar parágrafo vazio
    if not doc["content"]:
        doc["content"].append({
            "type": "paragraph",
            "content": []
        })
    
    return doc

def create_proper_json():
    print("=" * 70)
    print("🔧 CRIANDO JSON VÁLIDO DO TIPTAP")
    print("=" * 70)
    
    # Conectar ao banco
    db_path = "backend/data/webui.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar notas que têm conteúdo mas JSON é null ou inválido
    cursor.execute("""
        SELECT id, title, data 
        FROM note 
        WHERE data IS NOT NULL
    """)
    notes = cursor.fetchall()
    
    print(f"\n📚 {len(notes)} notas encontradas")
    
    updated = 0
    already_ok = 0
    errors = 0
    
    for note_id, title, data_str in notes:
        try:
            data = json.loads(data_str)
            
            if 'content' in data and isinstance(data['content'], dict):
                content = data['content']
                
                # Verificar se precisa atualizar JSON
                needs_update = False
                
                # Se JSON é None, null ou vazio, criar um novo
                if not content.get('json') or content['json'] is None:
                    # Tentar criar JSON a partir do HTML ou MD
                    if content.get('html'):
                        content['json'] = html_to_tiptap_json(content['html'])
                        needs_update = True
                    elif content.get('md'):
                        # Converter MD para texto simples primeiro
                        text = content['md']
                        content['json'] = {
                            "type": "doc",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": text[:1000] if len(text) > 1000 else text
                                        }
                                    ]
                                }
                            ]
                        }
                        needs_update = True
                    else:
                        # Criar JSON vazio válido
                        content['json'] = {
                            "type": "doc",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": []
                                }
                            ]
                        }
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
                else:
                    already_ok += 1
                    
        except Exception as e:
            errors += 1
            print(f"  ❌ Erro em '{title}': {e}")
    
    conn.commit()
    
    print(f"\n📊 Resumo:")
    print(f"  ✅ {updated} notas atualizadas com JSON válido")
    print(f"  ✓  {already_ok} notas já tinham JSON válido")
    print(f"  ❌ {errors} erros")
    
    # Verificar algumas notas
    cursor.execute("""
        SELECT title, 
               json_extract(data, '$.content.json') as json_content,
               length(json_extract(data, '$.content.md')) as md_len
        FROM note 
        WHERE json_extract(data, '$.content.md') IS NOT NULL 
           AND json_extract(data, '$.content.md') != ''
        ORDER BY md_len DESC
        LIMIT 3
    """)
    samples = cursor.fetchall()
    
    print(f"\n🔍 Verificação de amostras (maiores notas):")
    for title, json_c, md_len in samples:
        if json_c:
            try:
                json_obj = json.loads(json_c) if isinstance(json_c, str) else json_c
                print(f"\n  📄 {title[:40]}...")
                print(f"     MD: {md_len} caracteres")
                print(f"     JSON válido: ✅")
                print(f"     JSON preview: {json.dumps(json_obj, indent=2)[:300]}...")
            except:
                print(f"  📄 {title[:40]}... - JSON inválido ❌")
    
    conn.close()
    print("\n✅ JSON criado com sucesso!")

if __name__ == "__main__":
    create_proper_json()
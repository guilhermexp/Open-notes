#!/usr/bin/env python3
"""
Script para adicionar o campo JSON às notas migradas.
O RichTextInput precisa do campo JSON para exibir o conteúdo.
"""

import sqlite3
import json
from datetime import datetime

def html_to_tiptap_json(html_content):
    """
    Converte HTML em um formato JSON básico do TipTap.
    Esta é uma conversão simplificada - idealmente seria feito no frontend.
    """
    # Estrutura básica do TipTap
    tiptap_doc = {
        "type": "doc",
        "content": []
    }
    
    if html_content:
        # Para simplificar, vamos criar um único parágrafo com o conteúdo
        # O TipTap vai processar o HTML quando carregar
        tiptap_doc["content"].append({
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": html_content[:500] if len(html_content) > 500 else html_content  # Limitando para teste
                }
            ]
        })
    
    return tiptap_doc

def fix_json_content():
    print("=" * 70)
    print("🔧 ADICIONANDO CAMPO JSON ÀS NOTAS")
    print("=" * 70)
    
    # Conectar ao banco
    db_path = "backend/data/webui.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar todas as notas
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
            # Parse do JSON atual
            if data_str:
                data = json.loads(data_str)
                
                # Verificar se já tem JSON válido
                if 'content' in data and isinstance(data['content'], dict):
                    if 'json' in data['content'] and data['content']['json']:
                        # Já tem JSON, pular
                        continue
                    
                    # Adicionar campo JSON baseado no conteúdo existente
                    if 'html' in data['content'] and data['content']['html']:
                        # Converter HTML para JSON do TipTap
                        data['content']['json'] = html_to_tiptap_json(data['content']['html'])
                    elif 'md' in data['content'] and data['content']['md']:
                        # Criar JSON básico com o markdown como texto
                        data['content']['json'] = {
                            "type": "doc",
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": data['content']['md'][:500] if len(data['content']['md']) > 500 else data['content']['md']
                                        }
                                    ]
                                }
                            ]
                        }
                    else:
                        # Criar JSON vazio
                        data['content']['json'] = {
                            "type": "doc",
                            "content": []
                        }
                    
                    # Atualizar no banco
                    cursor.execute(
                        "UPDATE note SET data = ? WHERE id = ?",
                        (json.dumps(data), note_id)
                    )
                    updated += 1
                    print(f"  ✅ {title[:50]}... - JSON adicionado")
                    
        except Exception as e:
            errors += 1
            print(f"  ❌ Erro em '{title}': {e}")
    
    conn.commit()
    
    # Verificar o resultado
    print(f"\n📊 Resumo:")
    print(f"  ✅ {updated} notas atualizadas com JSON")
    print(f"  ❌ {errors} erros")
    
    # Teste específico
    cursor.execute("""
        SELECT title, 
               json_extract(data, '$.content.json'),
               json_extract(data, '$.content.md'),
               json_extract(data, '$.content.html')
        FROM note 
        WHERE title LIKE '%Variáveis%' 
        LIMIT 1
    """)
    test = cursor.fetchone()
    if test:
        print(f"\n🔍 Teste - '{test[0]}':")
        if test[1]:
            json_content = json.loads(test[1]) if isinstance(test[1], str) else test[1]
            print(f"  ✅ JSON encontrado: {json.dumps(json_content, indent=2)[:200]}...")
        else:
            print(f"  ❌ Sem JSON!")
        
        if test[2]:
            print(f"  📝 MD: {len(test[2])} caracteres")
        if test[3]:
            print(f"  📄 HTML: {len(test[3])} caracteres")
    
    conn.close()
    print("\n✅ Correção concluída!")

if __name__ == "__main__":
    fix_json_content()
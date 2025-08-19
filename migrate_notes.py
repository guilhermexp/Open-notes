#!/usr/bin/env python3
"""
Migração de Notas do open-notesUI para Open Notes
Este script migra todas as notas do banco de dados SQLite do open-notesUI
para o banco de dados do Open Notes atual.
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuração dos caminhos dos bancos de dados
SOURCE_DB = "/Users/guilhermevarela/Documents/Repositorios/open-notesUI/backend/data/webui.db"
TARGET_DB = "/Users/guilhermevarela/Documents/open-notes/backend/data/webui.db"

def backup_database(db_path):
    """Cria um backup do banco de dados antes da migração"""
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📦 Criando backup em: {backup_path}")
    
    source = sqlite3.connect(db_path)
    backup = sqlite3.connect(backup_path)
    source.backup(backup)
    backup.close()
    source.close()
    
    return backup_path

def get_notes_from_source():
    """Recupera todas as notas do banco de dados fonte"""
    print(f"📖 Lendo notas de: {SOURCE_DB}")
    
    conn = sqlite3.connect(SOURCE_DB)
    cursor = conn.cursor()
    
    # Busca todas as notas
    cursor.execute("""
        SELECT id, user_id, title, data, meta, access_control, created_at, updated_at
        FROM note
        ORDER BY created_at DESC
    """)
    
    notes = []
    for row in cursor.fetchall():
        note = {
            'id': row[0],
            'user_id': row[1],
            'title': row[2],
            'data': json.loads(row[3]) if row[3] else None,
            'meta': json.loads(row[4]) if row[4] else None,
            'access_control': json.loads(row[5]) if row[5] else None,
            'created_at': row[6],
            'updated_at': row[7]
        }
        notes.append(note)
    
    conn.close()
    print(f"✅ {len(notes)} notas encontradas")
    return notes

def get_note_folders_from_source():
    """Recupera todas as pastas de notas do banco de dados fonte"""
    print(f"📁 Lendo pastas de notas de: {SOURCE_DB}")
    
    conn = sqlite3.connect(SOURCE_DB)
    cursor = conn.cursor()
    
    # Verifica se a tabela note_folder existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='note_folder'
    """)
    
    if not cursor.fetchone():
        print("ℹ️ Tabela note_folder não encontrada no banco fonte")
        conn.close()
        return []
    
    # Busca todas as pastas
    cursor.execute("""
        SELECT id, parent_id, user_id, name, items, meta, data, is_expanded, created_at, updated_at
        FROM note_folder
        ORDER BY created_at DESC
    """)
    
    folders = []
    for row in cursor.fetchall():
        folder = {
            'id': row[0],
            'parent_id': row[1],
            'user_id': row[2],
            'name': row[3],
            'items': json.loads(row[4]) if row[4] else None,
            'meta': json.loads(row[5]) if row[5] else None,
            'data': json.loads(row[6]) if row[6] else None,
            'is_expanded': row[7],
            'created_at': row[8],
            'updated_at': row[9]
        }
        folders.append(folder)
    
    conn.close()
    print(f"✅ {len(folders)} pastas encontradas")
    return folders

def check_existing_notes(target_conn, note_ids):
    """Verifica quais notas já existem no banco de destino"""
    cursor = target_conn.cursor()
    existing_ids = set()
    
    for note_id in note_ids:
        cursor.execute("SELECT id FROM note WHERE id = ?", (note_id,))
        if cursor.fetchone():
            existing_ids.add(note_id)
    
    return existing_ids

def migrate_notes(notes, skip_existing=True):
    """Migra as notas para o banco de dados destino"""
    print(f"\n📝 Iniciando migração para: {TARGET_DB}")
    
    conn = sqlite3.connect(TARGET_DB)
    cursor = conn.cursor()
    
    # Verifica notas existentes
    note_ids = [note['id'] for note in notes]
    existing_ids = check_existing_notes(conn, note_ids) if skip_existing else set()
    
    if existing_ids:
        print(f"⚠️ {len(existing_ids)} notas já existem e serão puladas")
    
    # Migra as notas
    migrated = 0
    skipped = 0
    errors = 0
    
    for note in notes:
        if note['id'] in existing_ids:
            skipped += 1
            continue
        
        try:
            cursor.execute("""
                INSERT INTO note (id, user_id, title, data, meta, access_control, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                note['id'],
                note['user_id'],
                note['title'],
                json.dumps(note['data']) if note['data'] else None,
                json.dumps(note['meta']) if note['meta'] else None,
                json.dumps(note['access_control']) if note['access_control'] else None,
                note['created_at'],
                note['updated_at']
            ))
            migrated += 1
            print(f"  ✓ Migrada: {note['title'][:50]}...")
        except Exception as e:
            errors += 1
            print(f"  ✗ Erro ao migrar '{note['title']}': {str(e)}")
    
    conn.commit()
    conn.close()
    
    print(f"\n📊 Resumo da migração:")
    print(f"  • Notas migradas: {migrated}")
    print(f"  • Notas puladas (já existentes): {skipped}")
    print(f"  • Erros: {errors}")
    
    return migrated, skipped, errors

def migrate_folders(folders, skip_existing=True):
    """Migra as pastas de notas para o banco de dados destino"""
    if not folders:
        return 0, 0, 0
    
    print(f"\n📁 Iniciando migração de pastas para: {TARGET_DB}")
    
    conn = sqlite3.connect(TARGET_DB)
    cursor = conn.cursor()
    
    # Verifica se a tabela note_folder existe no destino
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='note_folder'
    """)
    
    if not cursor.fetchone():
        print("⚠️ Tabela note_folder não existe no banco destino")
        print("  Criando tabela note_folder...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS note_folder (
                id TEXT PRIMARY KEY,
                parent_id TEXT,
                user_id TEXT,
                name TEXT,
                items TEXT,
                meta TEXT,
                data TEXT,
                is_expanded INTEGER DEFAULT 0,
                created_at INTEGER,
                updated_at INTEGER
            )
        """)
        conn.commit()
    
    # Migra as pastas
    migrated = 0
    skipped = 0
    errors = 0
    
    for folder in folders:
        try:
            # Verifica se já existe
            if skip_existing:
                cursor.execute("SELECT id FROM note_folder WHERE id = ?", (folder['id'],))
                if cursor.fetchone():
                    skipped += 1
                    continue
            
            cursor.execute("""
                INSERT INTO note_folder (id, parent_id, user_id, name, items, meta, data, is_expanded, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                folder['id'],
                folder['parent_id'],
                folder['user_id'],
                folder['name'],
                json.dumps(folder['items']) if folder['items'] else None,
                json.dumps(folder['meta']) if folder['meta'] else None,
                json.dumps(folder['data']) if folder['data'] else None,
                folder['is_expanded'],
                folder['created_at'],
                folder['updated_at']
            ))
            migrated += 1
            print(f"  ✓ Pasta migrada: {folder['name']}")
        except Exception as e:
            errors += 1
            print(f"  ✗ Erro ao migrar pasta '{folder['name']}': {str(e)}")
    
    conn.commit()
    conn.close()
    
    if folders:
        print(f"\n📊 Resumo da migração de pastas:")
        print(f"  • Pastas migradas: {migrated}")
        print(f"  • Pastas puladas (já existentes): {skipped}")
        print(f"  • Erros: {errors}")
    
    return migrated, skipped, errors

def main():
    """Função principal do script de migração"""
    print("=" * 60)
    print("🚀 MIGRAÇÃO DE NOTAS - open-notesUI → Open Notes")
    print("=" * 60)
    
    # Verifica se os arquivos existem
    if not Path(SOURCE_DB).exists():
        print(f"❌ Erro: Banco de dados fonte não encontrado: {SOURCE_DB}")
        sys.exit(1)
    
    if not Path(TARGET_DB).exists():
        print(f"❌ Erro: Banco de dados destino não encontrado: {TARGET_DB}")
        sys.exit(1)
    
    # Cria backup do banco destino
    backup_path = backup_database(TARGET_DB)
    print(f"✅ Backup criado com sucesso!")
    
    try:
        # Recupera as notas do banco fonte
        notes = get_notes_from_source()
        
        if not notes:
            print("⚠️ Nenhuma nota encontrada para migrar")
            return
        
        # Recupera as pastas do banco fonte
        folders = get_note_folders_from_source()
        
        # Pergunta ao usuário se deseja continuar
        print(f"\n🔍 Encontradas {len(notes)} notas e {len(folders)} pastas para migrar")
        response = input("Deseja continuar com a migração? (s/n): ").lower()
        
        if response != 's':
            print("❌ Migração cancelada pelo usuário")
            return
        
        # Migra as pastas primeiro (se houver)
        if folders:
            migrate_folders(folders)
        
        # Migra as notas
        migrated, skipped, errors = migrate_notes(notes)
        
        if errors > 0:
            print(f"\n⚠️ Migração concluída com {errors} erros")
            print(f"   Backup disponível em: {backup_path}")
        else:
            print(f"\n✅ Migração concluída com sucesso!")
            
        print(f"\n💡 Dica: Reinicie o Open Notes para ver as notas migradas")
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {str(e)}")
        print(f"   Backup disponível em: {backup_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
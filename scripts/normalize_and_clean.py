#!/usr/bin/env python3
"""
Normaliza nombres de archivos Markdown en `pentesting/` a un formato humano legible:
 - minúsculas
 - eliminar acentos
 - reemplazar espacios y caracteres no alfanuméricos por '-'
 - truncar a 60 caracteres

Luego elimina los archivos temporales y scripts (INDEX.md, RENAME_SUGGESTIONS.md, y los scripts .py creados) con git.

USO: python3 scripts/normalize_and_clean.py
"""
import re
import subprocess
from pathlib import Path
import unicodedata
import sys

ROOT = Path(__file__).resolve().parents[1]
PENTEST = ROOT / 'pentesting'

def slugify(s: str, limit=60) -> str:
    s = s.strip()
    # normalize unicode (remove accents)
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # replace non alnum with dash
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    if len(s) > limit:
        s = s[:limit].rstrip('-')
    if not s:
        s = 'untitled'
    return s

def find_md_files():
    return sorted([p for p in PENTEST.rglob('*.md') if p.is_file()])

def get_title(path: Path) -> str:
    try:
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^#\s+(.*)', line)
            if m:
                return m.group(1).strip()
            return line
    except Exception:
        return ''

def git_mv(old: Path, new: Path):
    new.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'mv', str(old), str(new)], check=True)

def main():
    files = find_md_files()
    actions = []
    seen = set()
    for f in files:
        rel = f.relative_to(ROOT)
        title = get_title(f)
        base = title or f.stem
        slug = slugify(base, limit=60)
        new_name = f'{slug}.md'
        new_path = f.parent / new_name
        # avoid duplicates
        i = 1
        candidate = new_path
        while candidate.exists() or str(candidate) in seen:
            i += 1
            candidate = f.parent / f"{slug}-{i}.md"
        if f.name != candidate.name:
            actions.append((f, candidate))
            seen.add(str(candidate))

    if not actions:
        print('No changes needed')
        return

    print(f'Applying {len(actions)} normalized renames...')
    for old, new in actions:
        print(f'git mv {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}')
        git_mv(old, new)

    # Remove helper files and scripts
    helpers = ['INDEX.md', 'RENAME_SUGGESTIONS.md']
    # Only include scripts that are tracked by git
    tracked = subprocess.run(['git', 'ls-files', 'scripts'], capture_output=True, text=True, check=True).stdout.splitlines()
    helpers += [p for p in tracked]
    to_remove = [ROOT / h for h in helpers if (ROOT / h).exists()]
    if to_remove:
        print('Removing helpers (tracked):', ', '.join(str(p.relative_to(ROOT)) for p in to_remove))
        subprocess.run(['git', 'rm', '-f'] + [str(p) for p in to_remove], check=True)

    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Normalize filenames to human-readable slugs and remove helpers'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print('Done and pushed.')

if __name__ == '__main__':
    main()

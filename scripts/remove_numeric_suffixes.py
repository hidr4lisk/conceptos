#!/usr/bin/env python3
"""
Quitar sufijos numéricos tipo '-2', '-3' antes de la extensión .md en archivos bajo `pentesting/`.

Reglas:
 - Para cada archivo que coincida con `*(?:-\d+)\.md`, intenta renombrar a la versión sin `-N` si
   el destino no existe.
 - Si existe el destino, deja el archivo como está y lo reporta.
 - Aplica `git mv` para los cambios, luego commit y push.

Uso: python3 scripts/remove_numeric_suffixes.py
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PENTEST = ROOT / 'pentesting'

def find_numbered_md():
    return sorted([p for p in PENTEST.rglob('*.md') if re.search(r'-\d+\.md$', str(p))])

def target_for(p: Path) -> Path:
    # remove trailing -N before .md
    stem = p.stem
    m = re.sub(r'-\d+$', '', stem)
    return p.parent / (m + '.md')

def git_mv(old: Path, new: Path):
    new.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'mv', str(old), str(new)], check=True)

def main():
    files = find_numbered_md()
    if not files:
        print('No numbered suffix files found.')
        return
    actions = []
    skipped = []
    for f in files:
        tgt = target_for(f)
        if tgt.exists():
            skipped.append((f, tgt))
            continue
        actions.append((f, tgt))

    if not actions:
        print('No safe renames to apply; some targets exist. Skipped:', len(skipped))
        for s,t in skipped:
            print(f'- {s} -> {t} (target exists)')
        return

    print(f'Applying {len(actions)} renames (removing numeric suffixes)...')
    for old, new in actions:
        print(f'git mv {old.relative_to(ROOT)} -> {new.relative_to(ROOT)}')
        git_mv(old, new)

    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Remove numeric suffixes from filenames where safe'], check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print('Done and pushed.')

if __name__ == '__main__':
    main()

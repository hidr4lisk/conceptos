#!/usr/bin/env python3
"""
Aplica renombrados sugeridos limpiando lo que sobra en los títulos.

Lee `RENAME_SUGGESTIONS.md` (formato: `- `path` -> `title` -> `prop``) y genera un nombre limpio
basado en el título extraído. Luego ejecuta `git mv` para cambiar el nombre dentro de la misma carpeta.

Uso: python3 scripts/apply_rename_suggestions.py

IMPORTANTE: Revisa `RENAME_SUGGESTIONS.md` antes de ejecutar. El script hará many renames y los
ejecutará con `git mv` (staging). Al finalizar imprime resumen. Luego commit + push.
"""
import re
import subprocess
from pathlib import Path
import unicodedata
import sys

ROOT = Path(__file__).resolve().parents[1]
RS_FILE = ROOT / 'RENAME_SUGGESTIONS.md'

def clean_title(title: str) -> str:
    if not title:
        return 'untitled'
    s = title
    # remove markdown backticks and header markers
    s = s.replace('`', '')
    s = re.sub(r'^#{1,6}\s*', '', s)
    # remove common words that add noise
    s = re.sub(r'(?i)flashcard[s]?:?', '', s)
    s = re.sub(r'(?i)resumen(\s+tecnico)?[:\-]?', '', s)
    s = s.replace('►', ' ')
    s = s.replace('■', ' ')
    s = s.replace('—', ' - ')
    s = s.replace('–', ' - ')
    # remove URLs
    s = re.sub(r'https?://\S+', '', s)
    # remove punctuation not allowed in filenames
    s = re.sub(r'[\\/:*?"<>|]', '', s)
    # remove control chars
    s = ''.join(ch for ch in s if unicodedata.category(ch)[0] != 'C')
    # collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    # limit length
    if len(s) > 80:
        s = s[:77].rstrip() + '...'
    # replace slashes and commas with ' - '
    s = s.replace(',', ' - ')
    # finalize: replace spaces with ' - ' for readability
    s = s.strip()
    s = s.replace(' / ', ' - ')
    # keep accents but normalize weird combining marks
    s = unicodedata.normalize('NFKC', s)
    # ensure no leading/trailing punctuation
    s = s.strip(' -_.')
    if not s:
        s = 'untitled'
    return s

def parse_rs() -> list:
    lines = RS_FILE.read_text(encoding='utf-8').splitlines()
    entries = []
    for line in lines:
        m = re.match(r"^-\s+`([^`]+)`\s+->\s+`([^`]*)`\s+->\s+`([^`]*)`", line)
        if m:
            src = m.group(1)
            title = m.group(2)
            entries.append((src, title))
    return entries

def git_mv(old: Path, new: Path):
    new.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'mv', str(old), str(new)], check=True)

def main():
    if not RS_FILE.exists():
        print('RENAME_SUGGESTIONS.md not found. Generate it first.')
        sys.exit(1)
    entries = parse_rs()
    proposed = {}
    actions = []
    for src_rel, title in entries:
        src_path = ROOT / src_rel
        if not src_path.exists():
            print(f'WARN: source not found: {src_rel} (skipping)')
            continue
        dirp = src_path.parent
        clean = clean_title(title)
        fname = f"{clean}.md"
        # avoid duplicates
        attempt = fname
        i = 1
        while attempt in proposed.values():
            i += 1
            attempt = f"{clean} ({i}).md"
        target = dirp / attempt
        if src_path.name == target.name:
            # nothing to do
            continue
        actions.append((src_path, target))
        proposed[str(src_path)] = str(target)

    if not actions:
        print('No renames to apply.')
        return

    print(f'Applying {len(actions)} renames...')
    failed = []
    for old, new in actions:
        # ensure unique destination if file already exists
        final_new = new
        if final_new.exists():
            base = final_new.stem
            ext = final_new.suffix
            parent = final_new.parent
            i = 2
            while True:
                candidate = parent / f"{base} ({i}){ext}"
                if not candidate.exists():
                    final_new = candidate
                    break
                i += 1
        print(f'git mv "{old.relative_to(ROOT)}" "{final_new.relative_to(ROOT)}"')
        try:
            git_mv(old, final_new)
        except subprocess.CalledProcessError as e:
            print(f'ERROR moving {old} -> {final_new}: {e}')
            failed.append((old, final_new, str(e)))

    if failed:
        print('\nSome renames failed:')
        for old, new, err in failed:
            print(f'- {old} -> {new}: {err}')

    print('All git mv done. Now commit changes.')
    subprocess.run(['git', 'add', '-A'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Apply cleaned rename suggestions'], check=True)
    print('Committed renames. Now push to origin main.')
    subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    print('Push complete.')

if __name__ == '__main__':
    main()

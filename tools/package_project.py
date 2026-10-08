from pathlib import Path
import zipfile, sys
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'output/proyecto-i-base.zip'
out.parent.mkdir(exist_ok=True)
files=[]
for p in ROOT.rglob('*'):
    rel=p.relative_to(ROOT)
    if not p.is_file() or any(part in {'.godot','.git','tmp','__pycache__'} for part in rel.parts): continue
    if rel.parts[0]=='output' and rel.as_posix()!='output/pdf/informe-tarea-1.pdf': continue
    if p.suffix in {'.avi','.import'}: continue
    files.append(p)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in files: archive.write(p,p.relative_to(ROOT))
print(f'{len(files)} files; {out.stat().st_size} bytes; archive: {out}')
if '--no-extract' not in sys.argv:
    copy=ROOT/'tmp/clean-copy'
    copy.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out) as archive: archive.extractall(copy)
    print(f'Clean copy: {copy}')

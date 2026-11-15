#!/usr/bin/env python3
"""Recreate page images and page-level OCR from the unaltered archival PDF.
Use python scripts/build_archive.py '/path/to/original.pdf' ; requires PyMuPDF, Pillow, Tesseract.
"""
from __future__ import annotations
import csv, io, json, os, subprocess, sys, time, concurrent.futures, pathlib, statistics, unicodedata
import fitz
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'assets'/'peter-obi-anambra-original.pdf'
OUT = ROOT/'assets'/'pages';OUT.mkdir(parents=True,exist_ok=True)
INDEX = ROOT/'data'/'ocr-index.json'
D = fitz.open(PDF)
COUNT = len(D)
D.close()

def worker(n):
    doc = fitz.open(PDF)
    page = doc.load_page(n-1)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.47,1.47), alpha=False)
    im = Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    target = OUT / f'{n:04d}.webp'
    im.save(target,format='WEBP',quality=80,method=3)
    # Tesseract OCR on the actual scanned page, not on fictional/generated text.
    raw = io.BytesIO(); im.save(raw, format='PNG', optimize=False)
    env = dict(os.environ,OMP_THREAD_LIMIT='1')
    cp = subprocess.run(['tesseract','stdin','stdout','-l','eng','--psm','11','tsv'],
        input=raw.getvalue(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    groups = {}; confs = []
    if cp.returncode==0:
        for row in csv.DictReader(io.StringIO(cp.stdout.decode('utf8',errors='replace')),delimiter='\t'):
            word=(row.get('text') or '').strip()
            if not word: continue
            try: cf=float(row['conf'])
            except (ValueError,KeyError): cf=-1
            if cf >=0: confs.append(cf)
            ky=tuple(row.get(c,'') for c in ('block_num','par_num','line_num'))
            groups.setdefault(ky,[]).append(word)
    text='\n'.join(' '.join(w) for w in groups.values())
    return {'page':n,'text':text,'confidence':round(statistics.mean(confs),1) if confs else 0,
            'word_count':len(confs),'orientation':'landscape' if page.rect.width>page.rect.height else 'portrait',
            'image':f'assets/pages/{n:04d}.webp', 'image_bytes':target.stat().st_size}

if __name__=='__main__':
    start=time.time()
    futures={}; rows=[]
    workers = min(8, max(2,(os.cpu_count() or 4)//2))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
        for n in range(1,COUNT+1): futures[ex.submit(worker,n)]=n
        for f in concurrent.futures.as_completed(futures):
            n=futures[f]
            try: rows.append(f.result())
            except Exception as e: print('ERROR',n,repr(e),flush=True); rows.append({'page':n,'text':'','confidence':0,'word_count':0,'image':f'assets/pages/{n:04d}.webp','image_bytes':0})
            if len(rows)%25==0: print('OCR pages',len(rows),'/',COUNT,'elapsed',round(time.time()-start,1),'sec',flush=True)
    rows.sort(key=lambda r:r['page'])
    INDEX.write_text(json.dumps({'source':'Original supplied PDF; automated Tesseract OCR, unverified',
                                'pages':COUNT,'items':rows},ensure_ascii=False,separators=(',',':')),encoding='utf8')
    print('COMPLETE',COUNT,'elapsed',round(time.time()-start,1),'sec','index bytes',INDEX.stat().st_size,
          'image MB',round(sum(x['image_bytes'] for x in rows)/1e6,2),flush=True)

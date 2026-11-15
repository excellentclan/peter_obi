#!/usr/bin/env python3
"""Compile the single-file UI and optional fully embedded standalone HTML.
The production index.html contains all UI and the OCR index inline, but ships
page images and the unmodified PDF as optimised relative static assets.
"""
import base64, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
CHAPTERS=[
 {'page':1,'name':'Original cover and vision'},
 {'page':4,'name':'State institutions and the judiciary'},
 {'page':20,'name':'Security and public safety'},
 {'page':28,'name':'Education and school facilities'},
 {'page':142,'name':'Healthcare and medical infrastructure'},
 {'page':207,'name':'Road infrastructure and bridges'},
 {'page':247,'name':'Emergency management'},
 {'page':256,'name':'Public utilities and water'},
 {'page':270,'name':'Housing and land administration'},
 {'page':274,'name':'Agriculture and poverty alleviation'},
 {'page':296,'name':'Sports and recreation'},
 {'page':302,'name':'Commerce and industry'},
 {'page':326,'name':'Transport and mobility'},
 {'page':332,'name':'Financial and supporting records'},
 {'page':338,'name':'Commentary and appendices'}
]
FEATURES=[
 {'name':'State institutions','page':4,'image':6,'alt':'state secretariat buildings in Awka','text':'Photographs and descriptions of the state secretariat, local government facilities and judicial infrastructure.'},
 {'name':'Public safety','page':20,'image':25,'alt':'vehicles described as provided for security','text':'Source accounts of coordination and support to security agencies, including vehicles and related facilities.'},
 {'name':'Education','page':28,'image':80,'alt':'before-and-after photographs of a secondary school','text':'Schools, tertiary institutions, ICT equipment, teaching facilities and documented school rehabilitation.'},
 {'name':'Healthcare','page':142,'image':145,'alt':'university teaching hospital facilities','text':'Teaching hospitals, community healthcare facilities, maternal health and equipment featured in the publication.'},
 {'name':'Roads and bridges','page':207,'image':220,'alt':'road infrastructure shown in the publication','text':'Scanned project photographs and descriptions of roads, drainage, bridges and road maintenance.'},
 {'name':'Emergency response','page':247,'image':250,'alt':'emergency or erosion management works','text':'Historical images and descriptions of erosion-control, flood-related and emergency-management measures.'},
 {'name':'Public utilities','page':256,'image':265,'alt':'water supply and utility works','text':'Source material relating to potable water, water schemes and supporting public utility infrastructure.'},
 {'name':'Housing and land','page':270,'image':271,'alt':'housing development illustrated in the source','text':'Developments and interventions grouped by the publication under lands and housing.'},
 {'name':'Agriculture and livelihoods','page':274,'image':281,'alt':'agriculture infrastructure and college facilities','text':'Agricultural institutions, rural projects and programmes described under poverty alleviation.'},
 {'name':'Sports and recreation','page':296,'image':298,'alt':'sports and stadium infrastructure','text':'Facilities, local competitions and support for sporting activities pictured in the source.'},
 {'name':'Commerce and industry','page':302,'image':303,'alt':'industry and manufacturing project photographs','text':'Photographic records of industrial activity, manufacturing enterprises and commercial investment.'},
 {'name':'Transport and mobility','page':326,'image':330,'alt':'transport vehicles and mobility initiatives','text':'Interventions described by the publication under transport, mobility and public-service transport support.'}
]
for f in FEATURES:assert f['page']<=340
logo='data:image/png;base64,'+base64.b64encode((ROOT/'assets/ndc-logo.png').read_bytes()).decode()
raw=(ROOT/'index.template.html').read_text(encoding='utf8')
data=json.loads((ROOT/'data/ocr-index.json').read_text(encoding='utf8'))
assert data['pages']==340 and len(data['items'])==340
# Preserve all OCR output verbatim but escape potential HTML script terminators.
jsdata=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def html(embed=False):
    x=raw.replace('__LOGO_DATA__',logo).replace('__OCR_JSON__',jsdata)
    x=x.replace('__CHAPTERS_JSON__',json.dumps(CHAPTERS,ensure_ascii=False,separators=(',',':')))
    x=x.replace('__FEATURES_JSON__',json.dumps(FEATURES,ensure_ascii=False,separators=(',',':')))
    if embed:
        blocks=[]
        for n in range(1,341):
            p=ROOT/'assets'/'pages'/f'{n:04d}.webp'
            blocks.append(f'<script type="application/octet-stream" id="asset-page-{n}">{base64.b64encode(p.read_bytes()).decode()}</script>')
        pdf=ROOT/'assets'/'peter-obi-anambra-original.pdf'
        blocks.append('<script type="application/octet-stream" id="embedded-original-pdf">'+base64.b64encode(pdf.read_bytes()).decode()+'</script>')
        x=x.replace('__EMBEDDED_ASSETS__','\n'.join(blocks))
        x=x.replace('<meta property="og:image" content="assets/social-preview.jpg">','')
    else:
        x=x.replace('__EMBEDDED_ASSETS__','')
    assert '__LOGO_DATA__' not in x and '__OCR_JSON__' not in x and '__EMBEDDED_ASSETS__' not in x
    return x
(ROOT/'index.html').write_text(html(False),encoding='utf8')
if len(sys.argv)>1 and sys.argv[1]=='--standalone':
    (ROOT.parent/'anambra-standalone-index.html').write_text(html(True),encoding='utf8')
print('Assembled index.html',round((ROOT/'index.html').stat().st_size/1e3),'KB')
if len(sys.argv)>1 and sys.argv[1]=='--standalone':print('Assembled standalone',round((ROOT.parent/'anambra-standalone-index.html').stat().st_size/1e6,2),'MB')

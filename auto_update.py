import requests, re

TOKEN = "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"
GIST_ID = "719873c53714a5f38f60348e7fecc814"

FUENTES = {
    "España iptv-org": "https://iptv-org.github.io/iptv/countries/es.m3u",
    "España TDT": "https://raw.githubusercontent.com/LaQuay/TDTChannels/master/m3u/TDTChannels.m3u8",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Deportes": "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/sports.m3u",
    "Cine": "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/movies.m3u",
}

def descargar(url):
    try:
        r = requests.get(url, timeout=20)
        return r.text if r.status_code == 200 else ""
    except: return ""

def es_espanol(b):
    b=b.lower()
    return any(x in b for x in ['tvg-country="es"','group-title="es','spain','españa','|es|'])

todo="#EXTM3U\n"
for n,u in FUENTES.items():
    todo+=descargar(u)+"\n"

canales=re.findall(r'(#EXTINF.*?)\n(.*?)\n',todo,re.DOTALL)
vistos=set(); esp="#EXTM3U\n"; inter="#EXTM3U\n"
for i,l in canales:
    if l in vistos: continue
    vistos.add(l)
    bloque=i+"\n"+l
    (esp if es_espanol(bloque) else inter)+=bloque+"\n"

requests.patch(f"https://api.github.com/gists/{GIST_ID}",
 headers={"Authorization":f"token {TOKEN}"},
 json={"files":{"mi_lista_españa.m3u8":{"content":esp},"mi_lista_internacional.m3u8":{"content":inter}}})

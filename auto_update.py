import requests, re, os

TOKEN = "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"
GIST_ID = "719873c53714a5f38f60348e7fecc814"
FILENAME = "mi_lista_final.m3u8"

FUENTES = {
    "TDT": "https://www.tdtchannels.com/lists/tv.m3u8",
    "ES": "https://iptv-org.github.io/iptv/countries/es.m3u",
    "PlutoES": "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pluto_es.m3u"
}

ORDEN = ["Deportes","Cine","Series","VOD","Música","Documentales"]

def clasificar(nombre, grupo=""):
    n = (nombre + " " + grupo).lower()
    if any(k in n for k in ['deporte','laliga','dazn','eurosport','golf','nba','futbol','sport','f1','motogp']): return "Deportes"
    if any(k in n for k in ['cine','pelicula','film','movie','tcm','somos']): return "Cine"
    if any(k in n for k in ['serie','fox','axn','amc','comedy','syfy']): return "Series"
    if any(k in n for k in ['pluto','vod','plex']): return "VOD"
    if any(k in n for k in ['music','mtv','hits','kiss','rock','los 40']): return "Música"
    if any(k in n for k in ['documental','historia','discovery','nat geo','odisea']): return "Documentales"
    return None

canales = []
for fuente, url in FUENTES.items():
    r = requests.get(url, timeout=25, headers={"User-Agent":"Mozilla/5.0"})
    lineas = r.text.splitlines()
    for i,l in enumerate(lineas):
        if l.startswith("#EXTINF"):
            nombre = l.split(",")[-1].strip()
            if re.search('[\u0400-\u04FF\u4e00-\u9fff\u0600-\u06FF\u3040-\u30FF]', nombre): continue
            g = re.search('group-title="([^"]+)"', l)
            grupo = g.group(1) if g else ""
            url_c = lineas[i+1] if i+1 < len(lineas) else ""
            if url_c.startswith("http"):
                cat = clasificar(nombre, grupo)
                if cat:
                    # mantiene logo y todo, solo cambia el grupo
                    if 'group-title=' in l:
                        l = re.sub('group-title="[^"]*"', f'group-title="{cat}"', l)
                    else:
                        l = l.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{cat}"')
                    canales.append((cat, nombre.lower(), l, url_c))

vistos=set(); unicos=[]
for cat in ORDEN:
    for c in sorted([x for x in canales if x[0]==cat], key=lambda x: x[1]):
        if c[3] not in vistos: vistos.add(c[3]); unicos.append(c)

contenido = "#EXTM3U\n"
for _,_,inf,url in unicos:
    contenido += inf + "\n#EXTVLCOPT:network-caching=3000\n" + url + "\n"

requests.patch(f"https://api.github.com/gists/{GIST_ID}",
    headers={"Authorization": f"token {TOKEN}"},
    json={"files":{FILENAME:{"content":contenido}}})

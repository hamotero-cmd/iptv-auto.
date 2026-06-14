import requests

# Listas de España que sí funcionan en 2026
URLS = [
    "https://raw.githubusercontent.com/Ignac16/Iptv-spain-m3u-1416/main/playlist_spain.m3u8",
    "https://raw.githubusercontent.com/Ignac16/Iptv-spain-m3u-1416/main/Pruebas/playlist_spaintv.m3u8",
]

def descargar(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

def unir(textos):
    salida = ["#EXTM3U"]
    for t in textos:
        for linea in t.splitlines():
            if linea.strip():
                salida.append(linea)
    return "\n".join(salida)

if __name__ == "__main__":
    textos = [descargar(u) for u in URLS]
    lista = unir(textos)
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(lista)
    print("lista.m3u creada")

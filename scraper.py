import requests
import urllib.parse
import logging

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def buscar_cepe_api(termo):
    """Busca no CEPE usando a API Oficial (JSON)"""
    url = "[https://api.portal-open-api.sdoe.com.br/api/materias/pesquisa](https://api.portal-open-api.sdoe.com.br/api/materias/pesquisa)"
    params = {'termo': termo}
    headers_api = HEADERS.copy()
    headers_api['Accept'] = 'application/json'
    
    try:
        response = requests.get(url, params=params, headers=headers_api, timeout=15)
        response.raise_for_status()
        dados = response.json()
        resultados = dados.get("data", []) if isinstance(dados, dict) else dados
        
        if resultados and len(resultados) > 0:
            return "[https://diariooficial.pe.gov.br/](https://diariooficial.pe.gov.br/)"
    except Exception as e:
        logging.error(f"Erro na API SDOE (CEPE) para '{termo}': {e}")
    return None

def buscar_amupe(termo):
    """Busca no Diário dos Municípios de Pernambuco (AMUPE)"""
    termo_url = urllib.parse.quote(termo)
    url = f"[http://www.diariomunicipal.com.br/amupe/pesquisar?q=](http://www.diariomunicipal.com.br/amupe/pesquisar?q=){termo_url}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        texto_pagina = response.text.lower()
        
        if termo.lower() in texto_pagina and "não foram encontrados" not in texto_pagina:
            return url
    except Exception as e:
        logging.error(f"Erro na AMUPE para '{termo}': {e}")
    return None

def iniciar_varredura(termos_cepe, termos_amupe):
    encontrados = []
    
    for termo in termos_cepe:
        logging.info(f"Analisando CEPE (API) para: {termo}")
        link_cepe = buscar_cepe_api(termo)
        if link_cepe:
            encontrados.append({'origem': 'CEPE (Estadual)', 'termo': termo, 'link': link_cepe})
            
    for termo in termos_amupe:
        logging.info(f"Analisando AMUPE para: {termo}")
        link_amupe = buscar_amupe(termo)
        if link_amupe:
            encontrados.append({'origem': 'AMUPE (Municipal)', 'termo': termo, 'link': link_amupe})
            
    return encontrados
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

base_url = 'https://sigaa.unb.br'

initial_url = '/sigaa/public/turmas/listar.jsf'

url = 'https://sigaa.unb.br/sigaa/public/turmas/listar.jsf'

session = requests.Session()
response = session.get(url)
#html = response.text

soup = BeautifulSoup(response.text, 'html.parser')

# Extrair o ViewState (necessário para envios JSF)
view_state = soup.find('input', {'name': 'javax.faces.ViewState'})['value']

# Dados que você quer selecionar
dados = {
    'formTurma': 'formTurma',
    'formTurma:inputNivel': 'G',  # Graduação
    'formTurma:inputDepto': '673',  # DEPTO ADMINISTRAÇÃO
    'formTurma:inputAno': '2025',  # Ano
    'formTurma:inputPeriodo': '1',  # Período 1
    'formTurma:j_id_jsp_1370969402_11': 'Buscar',  # Botão de submit
    'javax.faces.ViewState': view_state
}

# Enviar o formulário via POST
response = session.post(url, data=dados)


# Verificar o resultado
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup)

#achando 'table'
link_especifico = soup.find('table',{'class': 'listagem'})
#print(len(link_especifico))
#print(link_especifico)

#aqui pegamos todos os 'tr' que aparecem
primeira_linha = link_especifico.find_all('tr')  # Encontra a primeira linha

#disciplina = link_especifico.find('span',{'class': 'titutloDisciplina'})
#print(primeira_linha[1])
'''
for row in primeira_linha:
    
    a_achado = row.find('a', onclick=True)

    if a_achado:
        onclick = a_achado['onclick']
        id_match = re.search(r"'id':'(\d+)'", onclick)
        if id_match:
            params = re.search(r"\{([^}]+)\}", onclick).group(1)
            params_dict = dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", params))
            title_span = a_achado.find("span", {"class": "tituloDisciplina"})
            current_component_name = title_span.text.strip()
            #print(current_component_name)

'''  


#aqui, personalizamos para pegar o 'tr'[1], que equivale a disciplina de Inteligencia Artificial'
link_js = primeira_linha[1].find('a', onclick=True)
#print(link_js)
if link_js:
    # Extrai os parâmetros do JavaScript
    onclick = link_js['onclick']
    import re
    id_match = re.search(r"'id':'(\d+)'", onclick)
    params = re.search(r"\{([^}]+)\}", onclick).group(1)
    params_dict = dict(re.findall(r"'([^']+)'\s*:\s*'([^']+)'", params))
    
    # Prepara os dados do formulário
    form_data = {
        'javax.faces.ViewState': soup.find('input', {'name': 'javax.faces.ViewState'})['value'],
        'formTurma': 'formTurma'
    }
    print(params_dict)
    form_data.update(params_dict)

    # Faz a requisição
    response = session.post(
        urljoin(base_url, initial_url),
        data=form_data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': urljoin(base_url, initial_url)
        }
    )

    # Processa a resposta
    nova_pagina = BeautifulSoup(response.text, 'html.parser')
    #print(nova_pagina)
    table_nova_pagina = nova_pagina.find('table',{'class': 'visualizacao'})
    #print(table_nova_pagina)

    pre_requisitos_tr  = table_nova_pagina.find('th', string='Pré-Requisitos:').find_parent('tr')

    acronyms = pre_requisitos_tr.find_all('acronym')

    pre_requisitos = []

    for acronym in acronyms:
        pre_requisitos.append({
            'codigo': acronym.get_text(strip=True),
            'nome': acronym['title']
        })

    #print(pre_requisitos)


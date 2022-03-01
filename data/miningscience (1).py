def download_pubmed (keyword):
    """
    Función que pide un parametro tipo str y como output da una lista de los id de la busqueda realizada en pubmed 
    """
    from Bio import Entrez
    from Bio import SeqIO
    from Bio import GenBank 
    Entrez.email = 'lizbeth.rojas@est.ikiam.edu.ec'
    handle = Entrez.esearch(db='pubmed',
                        sort='relevance',
                        retmax='1000',
                        retmode='xml',
                        term=keyword)
    resultado = Entrez.read(handle)
    id_lista = resultado["IdList"]
    ids = ','.join(id_lista)
    Entrez.email = 'lizbeth.rojas@est.ikiam.edu.ec'
    handle = Entrez.efetch(db='pubmed',
                       retmode='xml',
                       id=ids)
    id_total = ids.split(",")
    return (id_total) 

##funcion mining_pubs 
import csv 
import re
import pandas as pd 
from collections import Counter

def mining_pubs(tipo):
    """
    Función que pide un parametro tipo str que pude ser "DP", "AU" y "AD" y como output un data frame 
    """
    with open("pubmed-EcuadorGen-set.txt", errors="ignore") as f: 
        texto = f.read() 
    if tipo == "DP":
        ## DF de PMID y año de publicación
        PMID = re.findall("PMID- (\d*)", texto) 
        año = re.findall("DP\s{2}-\s(\d{4})", texto) 
        PMID_año = pd.DataFrame()
        PMID_año["PMID"] = PMID
        PMID_año ["Año de publicación"] = año
        return (PMID_año)
    ## DF de PMID y año de publicación 
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", texto) 
        autores = texto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        PMID_autor = pd.DataFrame()
        PMID_autor["PMID"] = PMID 
        PMID_autor["Numero de autores"] = num_autores
        return (PMID_autor)
    elif tipo == "AD": 
        texto = re.sub(r"Av\.","", texto)
        AD = texto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        veces_pais = pd.DataFrame()
        veces_pais["pais"] = resultado.keys()
        veces_pais["numero de autores"] = resultado.values()
        return (veces_pais)
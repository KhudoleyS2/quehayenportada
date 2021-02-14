# Dependencias
import requests
from bs4 import BeautifulSoup
import json

# Imports files
import urls, functions

datos_export = []

print ('\n__________________EJECUTANDO SCRAPER________________\n')

#Iterar URLs
for url in urls.urls:
    
    datos = {}

    print (url)
    datos['url_base'] = url

    request_data = requests.get(url).content
    soup = BeautifulSoup(request_data, 'html.parser')

    titulo_pagina = soup.title.text.strip()
    print('TITULO: ',titulo_pagina)
    datos['titulo'] = titulo_pagina








    #ESPECIALES !!!!!!!!!!!!!!!!!!!!!!!!!

    # La Razon
    if url == 'https://www.larazon.es/':
        a_tag = soup.body.main.find('div',class_='opening').h3.a
        a_tag.find('span').extract()
        url = a_tag['href']
        print ('URL: ',url)
        print ('TEXTO: ',a_tag.text.strip())
        print ('\n\n')

        datos['url'] = url
        datos['texto'] = texto
        datos_export.append(datos)
        continue

    #FIN ESPECIALES !!!!!!!!!!!!!!!!!!!!!












    # Comprobar si tiene ACRTICLE
    if soup.body.article:
        # Buscando los URLS de la noticia
        tags_a = soup.body.article.find_all('a',href=True)
        for a in tags_a:
            path = a['href']
            # Iterar y sacar el primero que no sea una imagen
            if not functions.comprobar_path_is_img(path):
                # Comprobar si es una ruta absoluta o relativa (si lleva https:// delante )
                if functions.comprobar_path(path):
                    url = path
                    print ('URL: ',url)
                    datos['url'] = url
                    break
                else:
                    url = url+path
                    print ('URL: ',url)
                    datos['url'] = url
                    break

        # Buscar la imagen dentro de la URL de de la noticia
        img = functions.buscar_imagenes_path(url)

            

        # Buscar el TEXTO

        #<h1>
        if soup.body.article.h1:
            print ('encontrado por article.h1')
            texto = soup.body.article.h1.get_text().strip()
            print ('TEXTO: ',texto)
            datos['texto'] = texto
            print ('\n\n')
            datos_export.append(datos)
            continue

        #<h2>
        if soup.body.article.h2:
            print ('encontrado por article.h2')
            texto = soup.body.article.h2.get_text().strip()
            print ('TEXTO: ',soup.body.article.h2.get_text().strip())
            datos['texto'] = texto
            print ('\n\n')
            datos_export.append(datos)
            continue
        
        #<h3>
        if soup.body.article.h3:
            texto = soup.body.article.h3.get_text().strip()
            if soup.body.article.h3:
                print ('encontrado por article.h3')
                texto = soup.body.article.h3.get_text().strip()
                print ('TEXTO: ',soup.body.article.h3.get_text().strip())
                datos['texto'] = texto
                print ('\n\n')
                datos_export.append(datos)
                continue
            #<h3><a>
            else:
                print ('encontrado por article.h3.a')
                texto = soup.body.article.h3.get_text().strip()
                print('TEXTO: ',soup.body.acrticle.h3.a.get_text().strip())
                datos['texto'] = texto
                print ('\n\n')
                datos_export.append(datos)
                continue


        #<a>
        if soup.body.article.a:

            # Comprobar si hay varios as.
            lista_a = soup.body.article.find_all('a')
            for a in lista_a:
                if a.text.strip():
                    texto = a.text.strip()
                    break
            print ('encontrado por article.a')
            print ('TEXTO: ',texto)
            datos['texto'] = texto
            print ('\n\n')
            datos_export.append(datos)
            continue            


        print ('ARTICLE No se ha encontrado nada ******************')
        datos['texto'] = None
        print ('\n\n')
        datos_export.append(datos)
        continue



    # Si no tiene ARTICLE
    else:
        # Buscando los URLS de la noticia
        tags_a = soup.body.find_all('a',href=True)
        for a in tags_a:
            path = a['href']
            # Iterar y sacar el primero que no sea una imagen
            if not functions.comprobar_path_is_img(path):
                # Comprobar si es una ruta absoluta o relativa (si lleva https:// delante )
                if functions.comprobar_path(path):
                    url = path
                    print ('URL: ',url)
                    datos['url'] = url
                    break
                else:
                    url = url+path
                    print ('URL: ',url)
                    datos['url'] = url
                    break


        # Buscar la imagen dentro de la URL de de la noticia
        img = functions.buscar_imagenes_path(url)


        # Buscar el TEXTO

        # <h1>
        if soup.body.h1:


            lista_h1 = soup.body.find_all('h1')
            for h1 in lista_h1:
                if len(h1.text.strip())>10:
                    texto = h1.text.strip()
                    break
            print ('encontrado por h1')
            print ('TEXTO: ', texto)
            datos['texto'] = texto
            print('\n\n')
            datos_export.append(datos)
            continue
        # <h2>
        if soup.body.h2:
            # noticia_path = soup.body.h2.find('a',href=True)['href']
            # if functions.comprobar_path(noticia_path):
            #     url = noticia_path
            #     print ('URL: ',url)
            # else:
            #     url = url+noticia_path
            #     print ('URL: ',url)

            lista_h2 = soup.body.find_all('h2')
            for h2 in lista_h2:
                if len(h2.text.strip())>5:
                    texto = h2.text.strip()
                    break
            print ('encontrado por h2')
            print ('TEXTO: ', texto)
            datos['texto'] = texto
            print('\n\n')
            datos_export.append(datos)
            continue


        # Mensaje de que no se ha podido sacar informacion con el scraper
        print ('TEXTO: SIN ACRITUCLO no encontrado nada **************** ')
        datos['texto'] = None
        print ('\n\n')
        pass
    




for i in datos_export:
    print (i)


with open('datos.json','w') as fp:
    json.dump(datos_export,fp)
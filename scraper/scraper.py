# Dependencias
import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime

import functions

# Conexion a la base de datos.
cnx = sqlite3.connect('sqlite.db')
try:
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM periodicos')
    datos =  cursor.fetchall()
    # lista de todas las URLS
    urls = [d[1] for d in datos]

except Exception as err:
    print ('ERROR con la conexion: ',err)
finally:
    cnx.close()









print ('\n__________________EJECUTANDO SCRAPER________________\n')
datos_export = []
#Iterar URLs
for url in urls:
    datos = {
        'url':url,
        'url_noticia':None,
        'titulo':None,
        'texto':None,
        'external_img_path':None,
        'fecha':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Intentar hacer el scraping de la url
    try:
        # SOUP de la url
        request_data = requests.get(url).content
        soup = BeautifulSoup(request_data, 'html.parser')

        # Titulo de la pagina
        titulo_pagina = soup.title.text.strip()
        datos['titulo'] = titulo_pagina



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
                        url_noticia = path
                        datos['url_noticia'] = url_noticia
                        break
                    else:
                        url_noticia = url_noticia+path
                        datos['url_noticia'] = url_noticia
                        break

            # Buscar la imagen dentro de la URL de de la noticia
            img = functions.buscar_imagenes_path(url_noticia)
            datos['external_img_path'] = img
                

            # Buscar el TEXTO

            #<h1>
            if soup.body.article.h1:
                texto = soup.body.article.h1.get_text().strip()
                print ('TEXTO: ',texto)
                datos['texto'] = texto
                print ('\n\n')
                datos_export.append(datos)
                continue

            #<h2>
            if soup.body.article.h2:
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
                    texto = soup.body.article.h3.get_text().strip()
                    print ('TEXTO: ',soup.body.article.h3.get_text().strip())
                    datos['texto'] = texto
                    print ('\n\n')
                    datos_export.append(datos)
                    continue
                #<h3><a>
                else:
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
                print ('TEXTO: ',texto)
                datos['texto'] = texto
                print ('\n\n')
                datos_export.append(datos)
                continue            


            print ('ARTICLE No se ha encontrado nada ******************')
            print ('\n\n')
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
                        url_noticia = path
                        datos['url_noticia'] = url_noticia
                        break
                    else:
                        url_noticia = url_noticia+path
                        datos['url_noticia'] = url_noticia
                        break


            # Buscar la imagen dentro de la URL de de la noticia
            img = functions.buscar_imagenes_path(url_noticia)
            datos['external_img_path'] = img


            # Buscar el TEXTO

            # <h1>
            if soup.body.h1:

                lista_h1 = soup.body.find_all('h1')
                for h1 in lista_h1:
                    if len(h1.text.strip())>10:
                        texto = h1.text.strip()
                        break
                print ('TEXTO: ', texto)
                datos['texto'] = texto
                print('\n\n')
                datos_export.append(datos)
                continue
            # <h2>
            if soup.body.h2:

                lista_h2 = soup.body.find_all('h2')
                for h2 in lista_h2:
                    if len(h2.text.strip())>5:
                        texto = h2.text.strip()
                        break
                print ('TEXTO: ', texto)
                datos['texto'] = texto
                print('\n\n')
                datos_export.append(datos)
                continue

        
    except Exception as err:

        # Mensaje de que no se ha podido sacar informacion con el scraper
        print ('ERROR: ',err)
        pass


    

datos_insert_sql = []

 # Transformar diccionario a una tupla y agregar a la lista de datos para insertar por SQL
for i in datos_export:
    values = (i['url_noticia'],i['external_img_path'],i['titulo'],i['texto'],i['fecha'],i['url'])
    datos_insert_sql.append(values)



# Conexion a la base de datos.
cnx = sqlite3.connect('sqlite.db')
try:
    cursor = cnx.cursor()
    sql_query = 'UPDATE periodicos SET path_noticia = ?, external_img_path = ?, titulo = ?, texto = ?, fecha = ? WHERE path = ?'
    cursor.executemany(sql_query, datos_insert_sql)
    cnx.commit()

except Exception as err:
    print ('ERROR con la conexion: ',err)
finally:
    cnx.close()
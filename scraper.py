import requests
from bs4 import BeautifulSoup


# Datos URLs
import urls

datos = []

print ('\n__________________________________')

#Iterar URLs
for url in urls.urls:
    
    print (url)

    request_data = requests.get(url).content
    soup = BeautifulSoup(request_data, 'html.parser')

    titulo_pagina = soup.title.text.strip()
    print('TITULO: ',titulo_pagina)


    #ESPECIALES !!!!!!!!!!!!!!!!!!!!!!!!!

    # La Razon
    if url == 'https://www.larazon.es/':
        a_tag = soup.body.main.find('div',class_='opening').h3.a
        a_tag.find('span').extract()
        print ('TEXTO: ',a_tag.text)
        print ('\n\n')
        continue

    #FIN ESPECIALES !!!!!!!!!!!!!!!!!!!!!








    # Comprobar si tiene ACRTICLE
    if soup.body.article:
        #<h1>
        if soup.body.article.h1:
            print ('encontrado por article.h1')
            print ('TEXTO: ',soup.body.article.h1.get_text().strip())
            print ('\n\n')
            continue

        #<h2>
        if soup.body.article.h2:
            print ('encontrado por article.h2')
            print ('TEXTO: ',soup.body.article.h2.get_text().strip())
            print ('\n\n')
            continue
        
        #<h3>
        if soup.body.article.h3:
            if soup.body.article.h3.text:
                print ('encontrado por article.h3')
                print ('TEXTO: ',soup.body.article.h3.get_text().strip())
                print ('\n\n')
                continue
            #<h3><a>
            else:
                print ('encontrado por article.h3.a')
                print('TEXTO: ',soup.body.acrticle.h3.a.get_text().strip())
                print ('\n\n')
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
            print ('\n\n')
            continue            



        print ('ARTICLE No se ha encontrado nada ******************')
        print ('\n\n')
        continue



    # Si no tiene ARTICLE
    else:
        # <h1>
        if soup.body.h1:
            lista_h1 = soup.body.find_all('h1')
            for h1 in lista_h1:
                if len(h1.text.strip())>10:
                    texto = h1.text.strip()
                    break
            print ('encontrado por h1')
            print ('TEXTO: ', texto)
            print('\n\n')
            continue
        # <h2>
        if soup.body.h2:
            lista_h2 = soup.body.find_all('h2')
            for h2 in lista_h2:
                if len(h2.text.strip())>5:
                    texto = h2.text.strip()
                    break
            print ('encontrado por h2')
            print ('TEXTO: ', texto)
            print('\n\n')
            continue


        # Mensaje de que no se ha podido sacar informacion con el scraper
        print ('TEXTO: SIN ACRITUCLO no encontrado nada **************** ')
        print ('\n\n')
        pass
    


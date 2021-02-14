import requests
from bs4 import BeautifulSoup


# FUNCION para comprobar si un string de URL contiene http o es una ruta relativa (devuelve True o False)
def comprobar_path(string_url):
    return 'http' in string_url


# FUNCION para omprobar si alguna de las extensiones marcadas en la funcion estan incluidas en la URL
def comprobar_path_is_img(string_url):
    extensiones = ['.jpg','.gif','.jpge','.png']
    is_image = False
    for e in extensiones:
        if e in string_url:
            is_image = True
    return is_image


# FUNCION para sacar la imagen de la URL pasada
def buscar_imagenes_path(string_url):

    # Hacer la sopa de la pagina
    req = requests.get(string_url).content
    soup = BeautifulSoup(req, 'html.parser')

    lista_img = []

    if soup.figure:
        lista_img = soup.figure.find_all('img',src=True)

    if not lista_img:
        if soup.article:
            lista_img = soup.article.find_all('img',src=True)
    




    # # Filtrar y buscar las imagenes
    # # Si el html tiene <body>
    # if soup.body:

    #     # Si tiene <main>
    #     if soup.body.main:

    #         if soup.body.main.article:
    #             lista_img = soup.body.main.article.find_all('img',src=True)
    #         else:
    #             lista_img = soup.body.main.find_all('img',src=True)
                
    #     # Si NO tiene <main>
    #     else:
    #         if soup.body.article:
    #             lista_img = soup.body.article.find_all('img',src=True)
    #         else:
    #             lista_img = soup.body.find_all('img',src=True)

    # # Si el HTML no tiene <body>
    # else:
    #     lista_img = soup.find_all('img',src=True)





    # En la lista de imagenes sacar sus src
    img_path_returned = None
    if len(lista_img) == 0:
        print ('No se han encontrado imagenes')

    for i in lista_img:
        img_path = i['src']
        if comprobar_path(img_path):
            if comprobar_path_is_img(img_path):
                img_path_returned = img_path
                break
    
    print ('URL_IMG: ',img_path_returned)
    return img_path_returned




# Pruebas
if __name__ == "__main__":

    url = 'https://www.20minutos.es/noticia/4582776/0/madrid-prorroga-prohibicion-reunirse-convivientes-casa-marzo/'

    img = buscar_imagenes_path(url)


    print ('\nULR DEVULETO:')
    print (img)




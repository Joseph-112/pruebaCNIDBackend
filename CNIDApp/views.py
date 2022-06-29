from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Establecer la conexión con el proyecto y la base de datos en Firebase
# Stablish the conection with the project and database in Firebase
cred = credentials.Certificate("../pruebaCNID/CNIDApp/serviceAccount.json")
firebase_admin.initialize_app(cred) 

db = firestore.client()

@csrf_exempt
def moviesApi(request, idMovie=""):
    
    '''Método que encapsula las peticiones GET
    Method that encapsulates GET's petitions'''

    if request.method == 'GET':

        '''Impresión por consola para conocer el id de la película
        Print for console to know the movie's id'''
        print(idMovie)

        '''Si el id de la película es ditinto de null
        devuelve los detalles del id de la película,
        de lo contrario, devolverá la lista completa de películas'''

        '''If movie's id is distinct to null
        return the details of the movie's id,
        in contrast, returns the complete movie's list'''
        
        if idMovie!="null":            
            movieDetails = db.collection('Movies').document(idMovie).get()
            '''Convertir el resultado a formato JSON
            Convert the result to JSON format'''
            movieDetails = movieDetails.to_dict()
            '''Verificar la película encontrada
            Verify the found movie'''
            print(movieDetails)
            return JsonResponse(movieDetails,safe = False)

        else:
            movieList = db.collection('Movies').get()
            for element in movieList:
                indice = movieList.index(element)
                movieList[indice]=element.to_dict()          
            
            return JsonResponse(movieList, safe = False)
    
    # Método que encapsula las peticiones POST
    # Method that encapsules the POST's petitions
    
    elif request.method == 'POST':
        
        movie_data = JSONParser().parse(request)
        '''Impresión para verificar el formato que se guardará en Firestore
        Print to verify the format that will be save on Firestore'''
        print(movie_data)
        try:
            db.collection('Movies').add(movie_data)
            return JsonResponse("Agregado con éxito", safe=False)
        except Exception:
            return JsonResponse('Error al agregar',movie_data.errors,safe=False)

    elif request.method == 'PUT':
        movie_data = JSONParser().parse(request)
        print('Actualizar')
        print(movie_data)
        movies = db.collection('Movies').get()
        for movie in movies:
            if movie.to_dict()['id'] == movie_data['id']:
                key = movie.id
                print('Llave')
                print(key)
                try:
                    db.collection('Movies').document(key).update(movie_data)
                    return JsonResponse("Actualizado con éxito", safe=False)
                except Exception:
                    return JsonResponse("Error al actualizar", safe=False)                     

    elif request.method == 'DELETE':
        movie_data = JSONParser().parse(request)
        print('Actualizar')
        print(movie_data)
        movies = db.collection('Movies').get()
        for movie in movies:
            if movie.to_dict()['id'] == movie_data['id']:
                key = movie.id
                print('Llave')
                print(key)
                try:
                    db.collection('Movies').document(key).delete(movie_data)
                    return JsonResponse("Eliminado con éxito", safe=False)
                except Exception:
                    return JsonResponse("Error al eliminar", safe=False)  

@csrf_exempt
def movieCollectionsApi(request,idCollection=0):
    if request.method == 'GET':
        if idCollection ==0:
            movieCollectionList = db.collection('Collections').get()
            for element in movieCollectionList:
                indice = movieCollectionList.index(element)
                movieCollectionList[indice]=element.to_dict()
            for element in movieCollectionList:
                print(element)
            
        return JsonResponse(movieCollectionList, safe = False)        

@csrf_exempt
def movieGenresApi(request,idGenre=''):
    if request.method == 'GET':
        if idGenre == 'null':
            movieGenreList = db.collection('Genres').get()
            for element in movieGenreList:
                indice = movieGenreList.index(element)
                movieGenreList[indice]=element.to_dict()
            for element in movieGenreList:
                print(element)
        return JsonResponse(movieGenreList, safe = False)

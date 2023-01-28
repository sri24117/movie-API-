from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.dbmodel import User
from app.dbmodel import Session
from app.dbmodel import Movie
from app.dbmodel import Cast

from app.auth import user_authentication

from django.contrib import admin
admin.site.register(Movie)
admin.site.register(User)
admin.site.register(Cast)
admin.site.register(Session)

import re
import jwt
import time
import datetime

# user Registration API
@api_view(['GET','POST','DELETE'])
def UserRegistration(request):
    if request.method == 'POST':
        inpId = request.data.get("id")
        inpName = request.data.get("name")
        inpEmail = request.data.get("email")
        inpPassword = request.data.get("password")
        inpconfirmpassword = request.data.get("confirmpassword")

        if (inpName == "" or inpName == None) and (inpEmail == "" or inpEmail == None) and (inpPassword == "" or inpPassword == None) and (inpconfirmpassword == "" or inpconfirmpassword == None):
            return Response(data={
                "Message": "Please Enter Required Fields"
            }, status=400)
        elif inpPassword != inpconfirmpassword:
            return Response(data={
                "Message": "Password Not Matched"
            }, status=401)
        elif re.search("^[a-z0-9]+@[a-z]+\.[a-z]+",inpEmail) == None:
            return Response(status=400,data={
                "Message":"Incorrect mail"
            })
        elif re.search("^(?=.{8,15}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*",inpPassword) == None:
            return Response(status=400,data={
                "Message":"Please enter valid password"
            })

        user_data = User.objects.filter(id=inpId)
        if len(user_data) >= 1:
            return Response(data={
                "Message": "User already Existed"
            }, status=401)
        created_time = datetime.datetime.now()
        User(id=inpId, username=inpName, email=inpEmail, password=inpPassword, created_at=created_time).save()
        return Response(data={
            "Message": "User Created Successfully"
        }, status=200)

# User login using username, password and generating jwt token for user maintain Session
@api_view(['GET','POST','DELETE'])
def loginProcess(request):
    if request.method == 'POST':
        inpusername = request.data.get("username")
        inppassword = request.data.get("password")
        userdata = User.objects.filter(username=inpusername, password=inppassword)
        key = "Secret_Key"
        jwt_token = jwt.encode({"username": inpusername, "password": inppassword}, key, algorithm='HS256')
        if len(userdata) == 0:
            return Response(status=404, data={
                "Message": "This username is not in usersdata"
            })
        Email = userdata[0].email
        Session.objects.filter(email=Email).delete()
        Session(email=Email, token=jwt_token, created_at=int(time.time() * 1000), expiry_at=int(time.time() * 1000)+86400000).save()
        return Response(status=200,data={
            "Message":"Session Created Successfully"
        })

# Movie Registration API
@api_view(['GET','POST','DELETE'])
@user_authentication
def moviecontents(request):
    if request.method == 'POST':
        inpId = request.data.get("id")
        inpTitle = request.data.get("title")
        inpRuntime = request.data.get("runtime")
        inpLanguage = request.data.get("language")
        inpTagline = request.data.get("tagline")
        Createdtime=datetime.datetime.now()
        movie = Movie.objects.filter(id=inpId)
        if len(movie) >= 1:
            return Response(status=401,data={
                "Message":"Same movie has in Moviestable"
            })
        else:
            inpdata = request.data
            Movie(**inpdata, created_at=Createdtime, updated_at=datetime.datetime.now()).save()
            return Response(data={
                "code": 200,
                "Content": {
                    "id": inpId,
                    "title": inpTitle,
                    "created_at": Createdtime,
                    "updated_at": datetime.datetime.now(),
                    "runtime": inpRuntime,
                    "language": inpLanguage,
                    "tagline": inpTagline
                }
            }, status=200)

    # Get method to get a list of movies in database
    elif request.method == 'GET':
        movies_list = []
        total_movies = Movie.objects.all()
        if len(total_movies) == 0:
            return Response(status=200, data={
                "Message": "Sorry, there is no any movie in the movi"
            })
        for m in total_movies:
            movies_list.append({
                "id": m.id,
                "title": m.title,
                "created_at": m.created_at,
                "updated_at": m.updated_at,
                "runtime": m.runtime,
                "language": m.language,
                "tagline": m.tagline
            })
        return Response(data={
            "movies": movies_list
        }, status=200)

# Getting the movie and list of cast details with desired movie id
@api_view(['GET','POST','DELETE'])
@user_authentication
def getmovie(request):
    if request.method == 'GET':
        querymid = request.query_params.get("mid")
        movie = Movie.objects.filter(id=querymid)
        movie_object = {}
        if len(movie) == 0:
            return Response(data={
                "Content": {"Message": "movie doesn't exist"}
            }, status=404)
        else:
            for m in movie:
                movie_object["id"] = m.id
                movie_object["title"] = m.title
                movie_object["created_at"] = m.created_at
                movie_object["updated_at"] = m.updated_at
                movie_object["runtime"] = m.runtime
                movie_object["language"] = m.language
                movie_object["tagline"] = m.tagline
        cast_list = []
        for c in Cast.objects.filter(movieid=querymid):
            cast_list.append({
                "movieid": c.movieid,
                "title": c.title,
                "name": c.name,
                "gender": c.gender,
                "dob": c.dob
            })
        return Response(data={
            "Content": {"movie": movie_object, "cast": cast_list}
        }, status=200)

# Creating Cast details
@api_view(['GET','POST','DELETE'])
@user_authentication
def castcontent(request):
    if request.method == 'POST':
        movieid = request.data.get("mid")
        inpdata = request.data
        cast=Movie.objects.filter(id=movieid)
        if (len(cast)) == 0:
            return Response(status=401,data={
                "Message":"No movie in the Movietable"
            })
        else:
            Cast(**inpdata).save()
            return Response(status=200, data=inpdata)

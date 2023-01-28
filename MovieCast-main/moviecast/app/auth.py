from rest_framework.response import Response

from app.dbmodel import Session
import time

def user_authentication(check):
    def inner_check(request):
        inp_token = request.headers["Token"]
        session_data = Session.objects.filter(token=inp_token)
        if len(session_data) == 0:
            return Response(status=400,data={
                "message":"There is no Session for user, please login"
            })
        else:
            if session_data[0].expiry_at < int(time.time() * 1000):
                return Response(status=401, data={
                    "message": "Session expire please login."
                })
            else:
                return check(request)

    return inner_check


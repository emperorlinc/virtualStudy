from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# Create your views here.


@api_view(['get'])
def api_overview(request):
    routes = [
        {
            "function": "Return all data",
            "method": "GET",
            "route": "api/v1/query",
            "restriction": "None"
        },
        {
            "function": "Return a data with id",
            "method": "GET",
            "route": "api/v1/query/detail/id",
            "restriction": "id type is string, NOT integer."
        },
        {
            "function": "Search data by name and location.",
            "method": "GET",
            "route": "api/v1/query?search=",
            "restriction": "filter down by name and location is possible by +, not &"
        },
        {
            "function": "Return random data.",
            "method": "GET",
            "route": "api/v1/query/random",
            "restriction": "None"
        },
        {
            "function": "Return datas that are set to favorite",
            "method": "GET",
            "route": "api/v1/query/favorite",
            "restriction": "None"
        },
        {
            "function": "Set or remove data favorites",
            "method": "PUT",
            "route": "api/v1/query/favorite/id",
            "restriction": "None"
        },
    ]
    return Response(routes, status=status.HTTP_200_OK)

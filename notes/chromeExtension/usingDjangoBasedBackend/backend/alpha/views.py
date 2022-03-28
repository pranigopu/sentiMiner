from itertools import count
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def vowels(string):
    vowels, foundVowels = ['a', 'e', 'i', 'o', 'u'], []
    string = string.lower()
    for c in string:
        if c in vowels: foundVowels.append(c)
    return foundVowels
def getName(request):
    name = request.GET.get('name')
    data = {
        'name': name,
        'vowels': vowels(name)
    }
    return JsonResponse(data)
"""
NOTE ON ATTRIBUTES OF A REQUEST
'request' objects may contain additional attributes.
These are specified in the URL using the following formal:
<base url>?attribute=value

Or for multiple attributes:
<base url>?attribute1=value1&attribute2=value2...

For the above 'getName' function, we need to provide:
http://127.0.0.1:8000/alpha/name?name=xyz
...to get response of the name 'xyz'.
If the attribute is not found, 'None' is returned.
"""
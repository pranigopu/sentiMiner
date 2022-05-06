from django.urls import path
from .views import *
urlpatterns = [
    path('scrape', scrapeEndpoint),
    path('format', formatEndpoint),
    path('clean', cleanEndpoint),
    path('normalize', normalizeEndpoint),
    path('summarize', summarizeEndpoint),
    path('analyze', analyzeEndpoint)
]
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

def home(request):
    html = """
    <h1>ATO incident/accident registraties</h1>
    <a href="/report_ia/">Registraties</a><br>
    """
    return HttpResponse(html)



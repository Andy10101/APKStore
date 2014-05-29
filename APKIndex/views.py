# Create your views here.
#-*-coding:utf-8-*-

#  views.py
#
#  Copyright 2014 Jorge Alberto Díaz Orozco <jaorozco@estudiantes.uci.cu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.urlresolvers import resolve

from models import apks
from utiles.misc_functions import search_keywords

def checkSearch(request):
    if request.GET.has_key('asearch'):
        keywords= request.GET['asearch']
        
        if keywords == "":
            keywords = "*all*"
        
        page = 1
        if request.GET.has_key('page'):
            page = request.GET['page']
        return HttpResponseRedirect('/buscar/'+keywords+'/'+str(page))
    else:
        return False

def adec(*args,**kwargs):
    print args
    return args[0]

def main(request):
    s = checkSearch(request)
    if  s != False:
        return s
    else:
        return aresponse(request)

def app(request,id):
    s = checkSearch(request)
    if  s != False:
        return s
    return aresponse(request,id)

def all(request):
    s = checkSearch(request)
    if  s != False:
        return s
    return search(request,keywords="*all*")

def search(request,keywords,page=1):
    s = checkSearch(request)
    if  s != False:
        return s
    else:
        return aresponse(request,keywords=keywords,page=page)

def aresponse(request,id=None,keywords=None,page=None):
    c = RequestContext(request)

    from forms import SearchForm
    sform = SearchForm()

    if request.method == 'GET':
        if id:
            apk = apks.objects.get(ind=id)

            rel = apk.relativo.split(":")
            if len(rel)>0:
                del rel[0]
            import os
            dir = os.path.dirname(apk.ruta)

            return render_to_response("desc.html",{"dir":dir,"rel":rel,"apk":apk,"err":False,"sform":sform},context_instance=c)
        elif keywords != None and page != None:
            asearch = keywords
            searchp = asearch.split()
            
            if len(searchp) == 0:
                return render_to_response("main.html",{"err":False,"sform":sform},context_instance=c)

            if keywords == "*all*":
                apk = apks.objects.all()
            else:
                apk = search_keywords(apks,searchp)

            paginator = Paginator(apk,20)
            try:
                lapk = paginator.page(page)
            except PageNotAnInteger:
                lapk = paginator.page(1)
            except EmptyPage:
                lapk = paginator.page(paginator.num_pages)


            if len(apk) > 0:
                return render_to_response("main.html",{"err":False,"cursor":lapk,"asearch":asearch,"sform":sform},context_instance=c)
            else:
                return render_to_response("main.html",{"err":True,"msg":"No se han encontrado coincidencias","sform":sform},context_instance=c)
        else:
            return render_to_response("index.html",{"err":False,"cursor":[],"sform":sform},context_instance=c)
    else:
        pass

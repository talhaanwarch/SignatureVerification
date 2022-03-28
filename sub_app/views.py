from django.shortcuts import render
from django.http import HttpResponseRedirect
from .py_templates.my_model import getdist
from PIL import Image
import numpy as np
from .forms import SignForm
from django.core.files.storage import FileSystemStorage
import os 
from django.conf import settings

def home(request):
	
	if request.method=='POST':
		form = SignForm(request.POST,request.FILES)
		if form.is_valid():
			print('form is valid')
			refimg=form.cleaned_data['ReferenceImage']
			quesimg=form.cleaned_data['QuestionedImage']
			if refimg:
				print('image upload')
				fs = FileSystemStorage()
				print(refimg.name)
				reffilename = fs.save(refimg.name, refimg)
				refpath = fs.url(reffilename)

				quesfilename = fs.save(quesimg.name, quesimg)
				quespath = fs.url(quesfilename)
				
				dist=getdist(refpath,quespath)
				print('dist',dist)
				dist='Forged' if dist > 0.83 else 'Genuine'
			return render(request,'home.html',{'form':form,'pred':dist,'refpath':refpath,
				'quespath':quespath,})
	else:
		form = SignForm()
		return render(request,'home.html',{'form':form,'pred':"None"})




from django.shortcuts import render
from django.http import HttpResponseRedirect
from .py_templates.my_model import get_ensemble_results
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
			refimg=form.cleaned_data['ReferenceImage']
			quesimg=form.cleaned_data['QuestionedImage']
			if refimg:
				fs = FileSystemStorage()
				reffilename = fs.save(refimg.name, refimg)
				refpath = fs.url(reffilename)

				quesfilename = fs.save(quesimg.name, quesimg)
				quespath = fs.url(quesfilename)
				
				dist=get_ensemble_results(refpath,quespath)
				
				
			return render(request,'home.html',{'form':form,'pred':dist,'refpath':refpath,
				'quespath':quespath,})
	else:
		form = SignForm()
		return render(request,'home.html',{'form':form,'pred':"None"})




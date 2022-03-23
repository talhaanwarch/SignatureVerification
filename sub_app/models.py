from django.db import models

from django.db import models
class SignModel(models.Model):
	ReferenceImage=models.FileField(upload_to='images')
	QuestionedImage=models.FileField(upload_to='images')


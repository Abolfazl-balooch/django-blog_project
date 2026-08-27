from django.db import models

# Create your models here.

class article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='images/articles')
    def __str__(self):
        return self.title


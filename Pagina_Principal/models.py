from django.db import models
from Usuario.models import Info_User


class Postagem(models.Model):
    titulo = models.CharField(max_length=50)
    conteudo = models.TextField()
    autor = models.ForeignKey(Info_User, on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)

from django.db import models
from user.models import User
from django.db.models.signals import pre_save, post_save


FORNECEDOR = (
    ('ECHO', 'ECHO'),
    ('MISAU', 'MISAU'),
)

TIPO_APROVACAO = (
    ('Aprovada', 'Aprovada'),
    ('Rejeitada', 'Rejeitada')
)

STATUS_REQUISICAO = (
    ('Pendente', 'Pendente'),
    ('Aprovada', 'Aprovada'),
    ('Rejeitada', 'Rejeitada'),
)

class Provincia(models.Model):
    nome = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nome
    
    
class Sector(models.Model):
    nome = models.CharField(max_length=150)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'
    
    def __str__(self):
        return self.nome
    
class Instrumento(models.Model):
    nome = models.CharField(max_length=150)
    stock = models.IntegerField()
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
        
    def __str__(self):
        return self.nome
    
class Necessidade(models.Model):
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    ano = models.PositiveSmallIntegerField()
    quantidade = models.IntegerField()
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.instrumento.nome
    
class Entrada(models.Model):
    data_entrada = models.DateField()
    fornecedor = models.CharField(max_length=100, choices=FORNECEDOR)
    quantidade = models.IntegerField()
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.instrumento.nome
    

    
class LevantamentoDeposito(models.Model):
    data_levantamento = models.DateField()
    quantidade = models.IntegerField()
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE)
    feito_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Levantamento no Deposito'
        verbose_name_plural = 'Levantamentos no Deposito'
    
    def __str__(self):
        return self.instrumento.nome
    
class Requisicao(models.Model):
    data_requisicao = models.DateField()
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    status_requisicao = models.CharField(max_length=50, choices=STATUS_REQUISICAO)
    
    class Meta:
        verbose_name = 'Requisicao'
        verbose_name_plural = 'Requisicoes'
        
    def __str__(self):
        return self.instrumento.nome
    
class Aprovacao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE)
    tipo_aprovacao = models.CharField(max_length=100, choices=TIPO_APROVACAO)
    comentario = models.TextField(null=True, blank=True)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE)
    feito_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Aprovacao'
        verbose_name_plural = 'Aprovacoes'
        
        
class ResumoInstrumento(models.Model):
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    necessidade = models.ForeignKey(Necessidade, on_delete=models.CASCADE, null=True, blank=True)
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Resumo de Instrumento'
        verbose_name_plural = 'Resumo de Instrumentos'
        
    def __str__(self):
        return self.instrumento.nome
    

def update_stock(sender, instance, created, *args, **kwargs):
    if created:
        instrumento = Instrumento.objects.get(entrada=instance)
        instrumento.stock += instance.quantidade
        instrumento.save()
        
post_save.connect(update_stock, sender=Entrada)
         
    
    
    
    
    
    
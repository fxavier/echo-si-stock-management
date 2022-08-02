from django.db import models
from user.models import User
from django.db.models.signals import pre_save, post_save



FORNECEDOR = (
    ('ECHO', 'ECHO'),
    ('MISAU', 'MISAU'),
    ('LEVANTAMENTO DEPOSITO', 'LEVANTAMENTO NO DEPOSITO')
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

qs = '"select 1 AS id, p.nome AS provincia, s.nome AS sector, i.nome AS instrumento, i.stock,"\
                                  "i.quantidade_necessaria AS necessidade, i.ano,  e.data_entrada, e.quantidade AS quantidade_entrada, e.fornecedor,"\
                                  "r.id AS requisicao_id, r.data_requisicao, r.quantidade AS quantidade_requisitada, r.status_requisicao from core_instrumento i" \
                                  " inner join core_sector s on s.id=i.sector_id" \
                                  " inner join core_provincia p on i.provincia_id=p.id" \
                                  " left join core_entrada e on e.instrumento_id=i.id" \
                                  " left join core_requisicao r on r.instrumento_id=i.id"'
                                   

class Provincia(models.Model):
    nome = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nome
    
    
class Sector(models.Model):
    nome = models.CharField(max_length=150)
    # provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'
    
    def __str__(self):
        return self.nome
    
class Instrumento(models.Model):
    nome = models.CharField(max_length=150)
    stock = models.IntegerField()
    ano = models.PositiveSmallIntegerField()
    quantidade_necessaria = models.IntegerField()
    provincia = models.ForeignKey(Provincia, related_name='instrumentos', on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, related_name='instrumentos', on_delete=models.CASCADE)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.nome
    
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

     
class Requisicao(models.Model):
    data_requisicao = models.DateField()
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    status_requisicao = models.CharField(max_length=50, choices=STATUS_REQUISICAO, default='Pendente')
    
    class Meta:
        verbose_name = 'Requisicao'
        verbose_name_plural = 'Requisicoes'
        
    def __str__(self):
        return self.instrumento.nome
    
class Aprovacao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE)
    tipo_aprovacao = models.CharField(max_length=100, choices=TIPO_APROVACAO)
    comentario = models.TextField(null=True, blank=True)
    feito_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feito_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Aprovacao'
        verbose_name_plural = 'Aprovacoes'
        
        
        
class Resumo(models.Model):
    provincia = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    instrumento = models.CharField(max_length=100)
    entrada_id = models.IntegerField()
    data_entrada = models.DateField()
    quantidade = models.IntegerField()
    fornecedor = models.CharField(max_length=100)
    stock = models.IntegerField()
    necessidade = models.IntegerField()
    ano = models.PositiveSmallIntegerField()
    id_requisicao = models.IntegerField()
    data_requisicao = models.DateField()
    quantidade_requisicao = models.IntegerField()
    status_requisicao = models.CharField(max_length=100)
    
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

def update_requisicao_status(sender, instance, created, *args, **kwargs):
    if created:
        requisicao = Requisicao.objects.get(aprovacao=instance)
        requisicao.status_requisicao = instance.tipo_aprovacao
        requisicao.save()
        if instance.tipo_aprovacao == 'Aprovada':
             instrumento = Instrumento.objects.get(pk=instance.requisicao.instrumento.id)
             instrumento.stock -= instance.requisicao.quantidade
             instrumento.save()
        # print('Created at:', datetime.now(), instance.tipo_aprovacao)
        # print("Instrumento:", instance.requisicao.instrumento.nome)
        # print("Instrumento:", instrumento.id, instrumento.nome, instance.requisicao.quantidade)
        
post_save.connect(update_requisicao_status, sender=Aprovacao)


# def insert_resumo_via_entrada(sender, instance, created, *args, **kwargs):
#     if created:
#         Resumo.objects.all().delete()
#         resumo_query = Resumo.objects.raw("select 1 AS id, p.nome AS provincia, s.nome AS sector, i.nome AS instrumento, i.stock,"\
#                                   "i.quantidade_necessaria AS necessidade, i.ano, e.id AS entrada_id, e.data_entrada, e.quantidade AS quantidade_entrada, e.fornecedor,"\
#                                   "r.id AS requisicao_id, r.data_requisicao, r.quantidade AS quantidade_requisitada, r.status_requisicao from core_instrumento i" \
#                                   " inner join core_sector s on s.id=i.sector_id" \
#                                   " inner join core_provincia p on i.provincia_id=p.id" \
#                                   " left join core_entrada e on e.instrumento_id=i.id" \
#                                   " left join core_requisicao r on r.instrumento_id=i.id"
#                                    )
#         # provincia = Provincia.objects.get(nome=resumo_query.provincia)
#         # sector = Sector.objects.get(nome=resumo_query.sector)
#         # entrada = Entrada.objects.get(pk=resumo_query.entrada_id)
#         # requisicao = Requisicao.objects.get(pk=resumo_query.requisicao_id)
#         # resumo = Resumo.objects.create(
#         #     provincia=resumo_query.provincia,
#         #     sector=resumo_query.sector,
#         #     instrumento=resumo_query.instrumento,
#         #     entrada_id=resumo_query.entrada_id,
#         #     data_entrada=resumo_query.data_entrada, 
#         #     quantidade=resumo_query.quantidade_entrada,
#         #     fornecedor=resumo_query.fornecedor,
#         #     stock=resumo_query.stock,
#         #     necessidade=resumo_query.necessidade,
#         #     ano=resumo_query.ano,
#         #     id_requisicao= resumo_query.requisicao_id,
#         #     data_requisicao=resumo_query.data_requisicao,
#         #     quantidade_requisicao=resumo_query.quantidade_requisitada,
#         #     status_requisicao=resumo_query.status_requisicao
#         # )
        
#         # resumo.save()
#         print(resumo_query.ano)
# post_save.connect(insert_resumo_via_entrada, sender=Entrada)
        
        
        
    
    
    
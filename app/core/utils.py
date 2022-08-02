import uuid
import os
from io import BytesIO


def user_image_path(instance, filename):
    """Generates file name """
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile', filename)

def str_query():
    qs = '"select 1 AS id, p.nome AS provincia, s.nome AS sector, i.nome AS instrumento, i.stock,"\
                                  "i.quantidade_necessaria AS necessidade, i.ano,  e.data_entrada, e.quantidade AS quantidade_entrada, e.fornecedor,"\
                                  "r.id AS requisicao_id, r.data_requisicao, r.quantidade AS quantidade_requisitada, r.status_requisicao from core_instrumento i" \
                                  " inner join core_sector s on s.id=i.sector_id" \
                                  " inner join core_provincia p on i.provincia_id=p.id" \
                                  " left join core_entrada e on e.instrumento_id=i.id" \
                                  " left join core_requisicao r on r.instrumento_id=i.id"'
                                   
                                   
    return qs

def metodo(self):
     pass
from pydantic import BaseModel, field_validator

from util.validators import *


class AlterarOuCriarCategoriaDto(BaseModel):
    id: Optional[int] = None
    descricao: str
    cor: str

    @field_validator("descricao")
    def validar_descricao(cls, v):
        msg = is_not_empty(v, "Descrição")
        msg = msg or is_size_between(v, "Descrição", 3, 1024)
        if msg: raise ValueError(msg)
        return v
    
    @field_validator("cor")
    def validar_cor(cls, v):
        msg = is_not_empty(v, "Descrição")
        msg = msg or is_size_between(v, "Cor", 3, 255)
        if msg: raise ValueError(msg)
        return v


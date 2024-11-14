from pydantic import BaseModel, field_validator

from util.validators import *


class AlterarCategoriaDto(BaseModel):
    id: int
    descricao: str

    @field_validator("id")
    def validar_id(cls, v):
        msg = is_greater_than(v, "Id", 0)
        if msg: raise ValueError(msg)
        return v

    @field_validator("descricao")
    def validar_descricao(cls, v):
        msg = is_not_empty(v, "Descrição")
        msg = msg or is_size_between(v, "Descrição", 3, 1024)
        if msg: raise ValueError(msg)
        return v

from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int]
    descricao: Optional[str] = None
    cor: Optional[str] = None

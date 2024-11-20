import asyncio
from io import BytesIO
import json
from typing import List, Optional
from fastapi import APIRouter, File, Form, Path, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from pydantic import ValidationError

from dtos.alterar_ou_criar_categoria_dto import AlterarOuCriarCategoriaDto
from dtos.alterar_pedido_dto import AlterarPedidoDto
from dtos.alterar_produto_dto import AlterarProdutoDto
from dtos.inserir_produto_dto import InserirProdutoDto
from dtos.problem_details_dto import ProblemDetailsDto
from models.categoria_model import Categoria
from models.pedido_model import EstadoPedido
from models.produto_model import Produto
from models.usuario_model import Usuario
from repositories.categoria_repo import CategoriaRepo
from repositories.item_pedido_repo import ItemPedidoRepo
from repositories.pedido_repo import PedidoRepo
from repositories.produto_repo import ProdutoRepo
from repositories.usuario_repo import UsuarioRepo
from util.images import transformar_em_quadrada
import os
from datetime import datetime
SLEEP_TIME = 0.2
router = APIRouter(prefix="/admin", tags=["Administrador"])


@router.get("/obter_produtos")
async def obter_produtos():
    try:
        await asyncio.sleep(SLEEP_TIME)

        def anexar_imagem(alvo: Produto):
            hasImagemUrl = os.path.exists(os.getcwd() + f'/static/img/produtos/{alvo.id:04d}.jpg')
            if hasImagemUrl:
                timestamp = int(datetime.now().timestamp())
                alvo.imagemUrl = f"{os.getenv('URL_TEST')}/static/img/produtos/{alvo.id:04d}.jpg?timestamp={timestamp}"
            return alvo

        produtos = list(map(anexar_imagem, ProdutoRepo.obter_todos()))
        return produtos

    except Exception as err:
        print(err)


@router.post("/inserir_produto", status_code=201)
async def inserir_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    descricao: str = Form(...),
    estoque: int = Form(...),
    id_categoria: int = Form(...),
    imagem: Optional[UploadFile] = File(None)
):
    try:
        produto_dto = InserirProdutoDto(
            nome=nome,
            preco=preco,
            descricao=descricao,
            estoque=estoque,
            id_categoria=id_categoria
        )
        if not imagem:
            pd = ProblemDetailsDto(
                "imagem",
                "O arquivo enviado não é uma imagem válida.",
                "invalid_file",
                ["body", "imagem"],
            )
            return JSONResponse(pd.to_dict(), status_code=422)
        
        conteudo_arquivo = await imagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
    
        await asyncio.sleep(SLEEP_TIME)
        novo_produto = Produto(
            None,
            produto_dto.nome,
            produto_dto.preco,
            produto_dto.descricao,
            produto_dto.estoque,
            produto_dto.id_categoria
        )
        novo_produto = ProdutoRepo.inserir(novo_produto)
        if novo_produto:
            imagem_quadrada = transformar_em_quadrada(imagem)
            imagem_quadrada.save(f"static/img/produtos/{novo_produto.id:04d}.jpg", "JPEG")
        return novo_produto
    except ValidationError as err: 
        return JSONResponse(json.loads(err.json()), status_code=400)
    except Exception as err:
        print(err)


@router.post("/excluir_produto", status_code=204)
async def excluir_produto(id_produto: int = Form(..., title="Id do Produto", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    if ProdutoRepo.excluir(id_produto):
        return None
    pd = ProblemDetailsDto(
        "int",
        f"O produto com id <b>{id_produto}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id_produto"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.get("/obter_produto/{id_produto}")
async def obter_produto(id_produto: int = Path(..., title="Id do Produto", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    produto = ProdutoRepo.obter_um(id_produto)
    if produto:
        def anexar_imagem(alvo: Produto):
            hasImagemUrl = os.path.exists(os.getcwd() + f'/static/img/produtos/{alvo.id:04d}.jpg')
            if hasImagemUrl:
                timestamp = int(datetime.now().timestamp())
                alvo.imagemUrl = f"{os.getenv('URL_TEST')}/static/img/produtos/{alvo.id:04d}.jpg?timestamp={timestamp}"
            return alvo
        return anexar_imagem(produto)
    pd = ProblemDetailsDto(
        "int",
        f"O produto com id <b>{id_produto}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id_produto"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.post("/alterar_produto/{id}", status_code=204)
async def alterar_produto(
    id: int,
    nome: str = Form(...),
    preco: float = Form(...),
    descricao: str = Form(...),
    estoque: int = Form(...),
    id_categoria: int = Form(...),
    imagem: Optional[UploadFile] = File(None)
):
    try:
        produto = Produto(
            id, 
            nome, 
            preco, 
            descricao, 
            estoque, 
            id_categoria
        )
        
        if ProdutoRepo.alterar(produto):
            if imagem:
                print(imagem)
                conteudo_arquivo = await imagem.read()
                imagem = Image.open(BytesIO(conteudo_arquivo))
                imagem_quadrada = transformar_em_quadrada(imagem)
                imagem_quadrada.save(f"static/img/produtos/{id:04d}.jpg", "JPEG")
            return JSONResponse({ 'alterado': True })
        
        pd = ProblemDetailsDto(
            "int",
            f"O produto com id <b>{id}</b> não foi encontrado.",
            "value_not_found",
            ["body", "id"],
        )
        return JSONResponse(pd.to_dict(), status_code=404)
    except Exception as err:
        print(err)


@router.post("/alterar_pedido", status_code=204)
async def alterar_pedido(inputDto: AlterarPedidoDto):
    await asyncio.sleep(SLEEP_TIME)
    if PedidoRepo.alterar_estado(inputDto.id, inputDto.estado.value):
        return None
    pd = ProblemDetailsDto(
        "int",
        f"O pedido com id <b>{inputDto.id}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.post("/cancelar_pedido", status_code=204)
async def cancelar_pedido(id_pedido: int = Form(..., title="Id do Pedido", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    if PedidoRepo.alterar_estado(id_pedido, EstadoPedido.CANCELADO.value):
        return None
    pd = ProblemDetailsDto(
        "int",
        f"O pedido com id <b>{id_pedido}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.post("/evoluir_pedido", status_code=204)
async def evoluir_pedido(id_pedido: int = Form(..., title="Id do Pedido", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if not pedido:
        pd = ProblemDetailsDto(
            "int",
            f"O pedido com id <b>{id_pedido}</b> não foi encontrado.",
            "value_not_found",
            ["body", "id"],
        )
        return JSONResponse(pd.to_dict(), status_code=404)
    estado_atual = pedido.estado
    estados = [e.value for e in list(EstadoPedido) if e != EstadoPedido.CANCELADO]
    indice = estados.index(estado_atual)
    indice += 1
    if indice < len(estados):
        novo_estado = estados[indice]
        if PedidoRepo.alterar_estado(id_pedido, novo_estado):
            return None
    pd = ProblemDetailsDto(
        "int",
        f"O pedido com id <b>{id_pedido}</b> não pode ter seu estado evoluído para <b>cancelado</b>.",
        "state_change_invalid",
        ["body", "id"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.get("/obter_pedido/{id_pedido}")
async def obter_pedido(id_pedido: int = Path(..., title="Id do Pedido", ge=1)):
    await asyncio.sleep(SLEEP_TIME)
    pedido = PedidoRepo.obter_por_id(id_pedido)
    if pedido:
        cliente = UsuarioRepo.obter_por_id(pedido.id_cliente)
        itens = ItemPedidoRepo.obter_por_pedido(pedido.id)
        pedido.cliente = cliente
        pedido.itens = itens
        return pedido
    pd = ProblemDetailsDto(
        "int",
        f"O pedido com id <b>{id_pedido}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.get("/obter_pedidos_por_estado/{estado}")
async def obter_pedidos_por_estado(estado: EstadoPedido = Path(..., title="Estado do Pedido")):
    await asyncio.sleep(SLEEP_TIME)
    pedidos = PedidoRepo.obter_todos_por_estado(estado.value)
    return pedidos


@router.get("/obter_usuarios")
async def obter_usuarios() -> List[Usuario]:
    await asyncio.sleep(SLEEP_TIME)
    usuarios = UsuarioRepo.obter_todos()
    return usuarios


@router.post("/excluir_usuario", status_code=204)
async def excluir_usuario(id_usuario: int = Form(...)):
    await asyncio.sleep(SLEEP_TIME)
    if UsuarioRepo.excluir(id_usuario):
        return None
    pd = ProblemDetailsDto(
        "int",
        f"O usuario com id <b>{id_usuario}</b> não foi encontrado.",
        "value_not_found",
        ["body", "id_produto"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)


@router.post("/inserir_categoria", status_code=201, tags= ["Categoria"])
async def inserir_categoria(record: AlterarOuCriarCategoriaDto) -> Categoria:
   try:
        nova_categoria_criada = CategoriaRepo.inserir(Categoria(**record.__dict__))
        return JSONResponse({ 'criada': nova_categoria_criada != None })
   except Exception as err:
       print(err)


@router.get("/obter_categorias", tags= ["Categoria"])
async def obter_categorias():
    await asyncio.sleep(SLEEP_TIME)
    categorias = CategoriaRepo.obter_todos()
    return categorias


@router.post("/alterar_categoria", status_code=204, tags= ["Categoria"])
async def alterar_categoria(inputDto: AlterarOuCriarCategoriaDto):
    await asyncio.sleep(SLEEP_TIME)
    categoria = Categoria(**inputDto.__dict__)
    return JSONResponse({ 'alterado': CategoriaRepo.alterar(categoria) })


@router.delete("/excluir_categoria/{id_categoria}", status_code=204, tags= ["Categoria"])
async def excluir_categoria(id_categoria: int):
    return JSONResponse({ 'deletado': CategoriaRepo.excluir(id_categoria) })


@router.get("/obter_categoria/{id_categoria}", tags= ["Categoria"])
async def obter_categoria(id_categoria: int = Path(..., title="Id da categoria", ge=1)):
    categoria = CategoriaRepo.obter_por_id(id_categoria)
    if categoria:
        return categoria
    pd = ProblemDetailsDto(
        "int",
        f"A categoria com id <b>{id_categoria}</b> não foi encontrada.",
        "value_not_found",
        ["body", "id"],
    )
    return JSONResponse(pd.to_dict(), status_code=404)

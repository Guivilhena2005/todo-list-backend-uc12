from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends,Query, Response,status
from app.dependencies import obter_tarefa_servico
from app.enums import CampoOrdenacao,Ordem,PrioridadeTarefa,StatusTarefa
from app.repositories import FiltroTarefas
from app.schemas import TarefaCreate,tarefaUpdate, tarefaOut
from app.services import AlteracaoDaTarefa, TarefaServicos
router = APIRouter(prefix="/tarefas", tags=["Tarefas"])
@router.post(
    "",
    response_model=tarefaOut,
    status_code=status.HTTP_201_CREATED,
    summary= "Criar tarefa",
    responses={404: {"description": "Usuario nao encontrado!"}},
)
def criar_tarefa(
    dados: TarefaCreate,
    servico: Annotated[TarefaServicos,
                       Depends(obter_tarefa_servico)],
)-> tarefaOut:
    return servico.criar(
        usuario_id=dados.usuario_id,
        titulo=dados.titulo,
        prioridade=dados.prioridade,
        prazo=dados.prazo
    )
def _montar_alteracoes(dados: tarefaUpdate) -> AlteracaoDaTarefa:
    return AlteracaoDaTarefa(**dados.model_dump(exclude_unset=True))
@router.patch(
    "/{tarefa_id}",
    response_model=tarefaOut,
    summary= "Atualizar tarefa",
    responses={404: {"description": "Tarefa nao encontrado!"}},
)
def atualizar_tarefa(
    tarefa_id: int,
    dados: tarefaUpdate,
    servico: Annotated[TarefaServicos,
                       Depends(obter_tarefa_servico)],
)-> TarefaOut:
    return servico.atualizar(tarefa_id, _montar_alteracoes(dados))

@router.delete(
    "/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary= "deletar tarefa",
    responses={404: {"description": "Tarefa nao encontrada!"}},
)
def remover_tarefa(
    tarefa_id: int,
    servico: Annotated[TarefaServicos,
                       Depends(obter_tarefa_servico)],
)-> Response: 
    servico.remover(tarefa_id) 
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get(
    "",
    response_model=tarefaOut,
    status_code=status.HTTP_201_CREATED,
    summary= "Listar tarefas",
    responses={404: {"description": "Usuario nao encontrado!"}},
)
def listar_tarefa(
    servico: Annotated[TarefaServicos,
                       Depends(obter_tarefa_servico)],
    usuario_id : Annotaded[int, Query(allias="usuario_id" , description="Id do usuario")],
    status_tarefa: Annotated[StatusTarefa | None, Query(allias="status")]=None,
    prioridade_tarefa: Annotated[StatusTarefa | None, Query()]=None,
    prazo_ate: Annotated[date | None, Query(alias="prazo ate" , description="Somente tarefas com prazo até essa data")]=None,
ordem: Annotaded[Ordem , Query()] = Ordem.DESC,
limite: Annotaded[Ordem , Query(ge=1 , le=200 , alias ="limit")] = 50,
deslocamento: Annotaded[Ordem , Query(ge=0 , alias="limit")] = 0,
ordenar_por: Annotaded[CampoOrdenacao , Query(alias="ordenar por")] = CampoOrdenacao.CRIADO_EM,

)-> list[tarefaOut]:
    filtro = FiltroTarefas(
        usuario_id=usuario_id,
        status=status_tarefa,
        prioridade=prioridade_tarefa,
        prazo_ate=prazo_ate,
        ordem=ordem,
        limite=limite,
        deslocamento=deslocamento,
        ordenar_por=ordenar_por
    )
    return servico.listar(filtro)

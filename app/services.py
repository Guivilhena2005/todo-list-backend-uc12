from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from app.enums import PrioridadeTarefa , StatusTarefa
from app.exceptions import (
    CredencialInvalidas,
    EmailCadastrado,
    TarefaNaoEncontrado,
    UsuarioNaoEncontrado
)
from app.models import Tarefa , Usuario
from app.repositories import FiltroTarefas , TarefaRepositorio , UsuarioRepositorio
from app.security import HashdeSenha

NAO_INFORMADO: Any = object()

@dataclass(frozen=True)
class AlteracoesDaTarefa:
    titulo: Any = NAO_INFORMADO
    status: Any = NAO_INFORMADO
    prioridade : Any = NAO_INFORMADO
    
    def informado(self, campo: str) -> bool:
        return getattr(self , campo) is not NAO_INFORMADO
    
class UsuarioService:
    def __init__(self, repositorio : UsuarioRepositorio, Hasher : HashdeSenha) -> None:
        self._repositorio = repositorio
        self._hasher = Hasher
    def cadastrar(self, nome : str , email: str , senha : str) -> Usuario:
        if self._repositorio.email_exist(email):
            raise EmailCadastrado  
        usuario = Usuario(nome=nome , email=email)
        usuario.definir_senha(senha, self._hasher)
        return self._repositorio.salvar(usuario)
    def autenticar(self, email:str, senha:str) -> Usuario:
        usuario = self._repositorio.Buscar_por_email(email)
        if usuario is None or not usuario.senha_conferir(senha, self._hasher):
            raise CredencialInvalidas()
        return usuario
    def buscar(self, usuario_id: int) -> Usuario:
        usuario = self._repositorio.Buscar_por_id(usuario_id)
        if usuario is None:
            raise UsuarioNaoEncontrado()
        return usuario
class TarefaServicos:
    def _init(
        self, tarefa: TarefaRepositorio , usuario: UsuarioRepositorio
    ) -> None:
        self._tarefa = tarefa
        self._usuario = usuario
        
    def criar (
        self , usuario_id: int,
        titulo : str,
        prioridade: PrioridadeTarefa,
        prazo: date | None) -> Tarefa:
        
        if self._usuario.Buscar_por_id(usuario_id) is None:
            raise UsuarioNaoEncontrado()
        tarefa = Tarefa(
            usuario_id=usuario_id,
            titulo=titulo,
            prioridade=prioridade,
            prazo=prazo)
        return self._tarefa.Salvar(tarefa)
    def atualizar(
        self, tarefa_id: int, alteracoes: AlteracoesDaTarefa
    ) -> Tarefa:
        tarefa = self._tarefa.Buscar_por_id(tarefa_id)
        if tarefa is None:
            raise TarefaNaoEncontrado()
        if alteracoes.informado("titulo"):
            tarefa.titulo = alteracoes.titulo
        if alteracoes.informado("status"):
            tarefa.definir_status(StatusTarefa(alteracoes.status))
        if alteracoes.informado("prioridade"):
            tarefa.prioridade = alteracoes.prioridade
        if alteracoes.informado("prazo"):
            tarefa.prazo = alteracoes.prazo
        return self._tarefa.Salvar(tarefa)
    def remover(self, tarefa_id: int) -> None:
        tarefa = self._tarefa.Buscar_por_id(tarefa_id)
        if tarefa is not None:
            self._tarefa.remover(tarefa)
        else:
            raise TarefaNaoEncontrado()
    def listar(self, filtro:FiltroTarefas) -> list[Tarefa]:
        return self._tarefa.listar(filtro)
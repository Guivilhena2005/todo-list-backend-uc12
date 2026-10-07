class ErroDoDominio(Exception):
    mensagem = "Não foi possivel concluir sua operação"
    def _init_(self , mensagem: str | None = None) -> None:
      self.mensagem = mensagem or type(self).mensagem
      
      
class RecursoNaoEncontrado(ErroDoDominio) : mensagem = "Recurso não encontrado"
class UsuarioNaoEncontrado(RecursoNaoEncontrado): mensagem = "Usuaeio não encontrado"
class TarefaNaoEncontrado(RecursoNaoEncontrado) : mensagem = "Tarefa não encontrada"

class RegraDeNegocioViolada(ErroDoDominio) : mensagem = "Operação recusada por uma regra de software"
class TituloObrigatorio(RegraDeNegocioViolada): mensagem = "O titulo da tarefa é obrigatoria"
class ValorInvalido(RegraDeNegocioViolada): mensagem = "O valor inserido é invalido"

class EmailCadastrado(ErroDoDominio): mensagem = "Email ja cadastrado"
class CredencialInvalidas(ErroDoDominio): mensagem = "Email ou senha invalidas"
class AcessoNaoAutorizada(ErroDoDominio): mensagem = "Voce nao tem acesso para esse recurso"
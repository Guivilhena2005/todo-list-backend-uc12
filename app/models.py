from datetime import datatime
from sqlalchemy import collum , DateTime, Integer , String
from sqlalchemy.orm import validates
from app.database import Base
from app.exceptions import ValorInvalido
from app.security import HashdeSenha

class Usuario(Base):
    _tablename_ = "usuarios"
    id = Collum(Integer, primary_key=True , index=True)
    nome= Collum(String(120),nullable=False)
    email=Collum(String(120),nullable=False)
    _senha_hash = Collum("senha_hash", String(255), nullab=False)
    criado_em=Collum(DataTime, nullable=False , default=datatime.now)
    def __init__(self, *, nome: str, email: str, senha: str, hash_de_senha: HashdeSenha) -> None:
        self.nome = nome
        self.email = email.strip().lower()
    def definir_senha(self, senha: str, hasher: HashdeSenha) -> None:
        self._senha_hash = hasher.gerar(senha)
    def senha_confere(self, senha: str, hasher: HashdeSenha) -> bool:
        return hasher.verificar(senha, self._senha_hash)
    @validates("nome")
    def validar_nome(self, _campo: str, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValorInvalido("O nome do usuario é obrigatorio")
        return valor.strip()
    def __repr__(self) -> str: return f"<Usuario {self.id} - {self.email}>"
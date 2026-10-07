from abc import ABC , abstractmethod
import bcrypt
from app.exceptions import ValorInvalido
LIMITE_BYTES = 72

class HashdeSenha(ABC):
    @abstractmethod
    def gerar(self , senha: str) -> str: 
        "Cria um hashcode do usuario"
    
    @abstractmethod
    def verificar(self , senha : str , hash_armazenado : str) -> bool: 
        "Verifica se hashcode da senha do usuario e o msm do DB: "
    
class Hashcrypt(HashdeSenha):
    def __init__(self, custo: int = 12):  
        self._custo = custo
    def gerar(self, senha : str) -> str: 
        em_bytes = senha.encode("utf-8")
        if len(em_bytes) >  LIMITE_BYTES:
            raise ValorInvalido(
            f"Sua senha respeita o limite de caracteres" 
            )
            
        return bcrypt.hashpw(em_bytes, bcrypt.gensalt(self._custo)).decode("utf-8")
    def verificar(self, senha: str , hash_armazenado : str) -> bool:
        try:
            return bcrypt.checkpw(senha.encode("utf-8"), hash_armazenado.encode("utf-8"))
        except ValueError: 
            return False
    
        

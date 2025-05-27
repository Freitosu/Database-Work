from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
import transaction
from zodb.modelos import Jogo # Corrigido para o caminho correto


class BaseDB():
    def __init__(self):
        self.storage = FileStorage.FileStorage('jogos.fs')
        self.db = DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root()

        # Inicializa as "tabelas" se não existirem
        if not hasattr(self.root, 'jogos'):
            self.root.jogos = OOBTree()
        if not hasattr(self.root, 'usuarios'):
            self.root.usuarios = OOBTree()

    def fechar(self):
        transaction.abort()  # Garante que nenhuma transação fique aberta
        self.connection.close()
        self.db.close()
        self.storage.close()


class JogoDB(BaseDB):
    def __init__(self):        
        super().__init__()

    # Métodos para jogo
    def criar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()

    def buscar_jogo(self, id) -> Jogo:
        return self.root.jogos.get(id)
    
    def listar_jogos(self) -> list[Jogo]:
        return list(self.root.jogos.values())
    
    def atualizar_jogo(self, jogo: Jogo):
        self.root.jogos[jogo.id] = jogo
        transaction.commit()
    
    def excluir_jogo(self, id: int) -> Jogo:
        jogo = self.buscar_jogo(id)
        if jogo:
            del self.root.jogos[jogo.id]
            transaction.commit()
            return jogo

    # # Métodos para Usuário
    # def criar_usuario(self, usuario: Usuario):
    #     self.root.usuarios[usuario.id] = usuario  # Corrigido: era self.root.usuario
    #     transaction.commit()

    # def buscar_usuario_id(self, id) -> Usuario:
    #     return self.root.usuarios.get(id)
    
    # def buscar_usuario_email(self, email) -> Usuario:
    #     for usuario in self.root.usuarios.values():
    #         if usuario.email == email:
    #             return usuario
    
    # def listar_usuarios(self) -> list[Usuario]:
    #     return list(self.root.usuarios.values())
    
    # def atualizar_usuario(self, usuario: Usuario):
    #     self.root.usuarios[usuario.id] = usuario
    #     transaction.commit()

    # def excluir_usuario(self, id: int) -> Usuario:
    #     usuario = self.buscar_usuario_id(id)  # Corrigido: era self.buscar_usuario
    #     if usuario:
    #         del self.root.usuarios[usuario.id]
    #         transaction.commit()
    #         return usuario



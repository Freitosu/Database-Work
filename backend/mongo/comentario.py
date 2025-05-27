from datetime import datetime

def novo_comentario(jogo_id, cliente_id, comentario, avaliacao):
    return {
        "jogo_id": str(jogo_id),
        "cliente_id": cliente_id,
        "comentario": comentario,
        "avaliacao": avaliacao,
        "data_comentario": datetime.now()
}
"""
Helpers para padronizar textos de feedback de operações CRUD.

Uso básico:
    from utils.messages import msg_criado, msg_atualizado, msg_excluido
    from utils.messages import msg_erro_criar, msg_erro_atualizar

    messages.success(request, msg_criado("Cliente"))
    messages.error(request, msg_erro_criar("Cliente"))

Override pontual (texto customizado): basta passar a string diretamente
ao invés de usar a função helper.
"""


def msg_criado(entidade: str) -> str:
    return f"{entidade} criado(a) com sucesso!"


def msg_atualizado(entidade: str) -> str:
    return f"{entidade} atualizado(a) com sucesso!"


def msg_excluido(entidade: str) -> str:
    return f"{entidade} excluído(a) com sucesso!"


def msg_erro_criar(entidade: str) -> str:
    return f"Não foi possível criar {entidade.lower()}. Revise os campos destacados."


def msg_erro_atualizar(entidade: str) -> str:
    return f"Não foi possível atualizar {entidade.lower()}. Revise os campos destacados."

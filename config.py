import os

def get_path_dados_gerados():
    """
    Retorna o caminho para a pasta onde os dados gerados serão armazenados.
    """

    dirname = 'dados_gerados'

    path = os.path.join(os.getcwd(), dirname)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

DIR_DADOS_GERADOS = get_path_dados_gerados()
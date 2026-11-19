from base_conhecimento import BaseConhecimento
from assistente import Assistente, pedir_opcao
import gerir
import tela_da_energia


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    print("=" * 50)
    print(f" {assistente.nome}: orientação para pessoas idosas")
    print("=" * 50)
    print("Este assistente NÃO é um canal oficial e não pede nome, CPF,")
    print("telefone ou e-mail. Não digite dados pessoais.")

    if len(base) == 0:
        print("\nAtenção: a base de conhecimento está vazia ou não foi carregada.")

    try:
        while True:
            print("\n--- Menu principal ---")
            print(" 1. Fazer uma pergunta")
            print(" 2. Navegar por categorias")
            print(" 3. Consultar orientação por ID")
            print(" 4. Pesquisar (título ou categoria)")
            print(" 5. Cadastrar orientação")
            print(" 6. Atualizar orientação")
            print(" 7. Excluir orientação")
            print(" 8. Listar orientações ordenadas")
            print(" 9. Análise da base")
            print("10. Ver indicadores de uso")
            print("11. Exportar atendimentos (CSV)")
            print("12. Calcular economia de energia")
            print(" 0. Sair")
            opcao = pedir_opcao("Escolha uma opção: ", 0, 12)

            if opcao == 1:
                assistente.perguntar()
            elif opcao == 2:
                assistente.navegar()
            elif opcao == 3:
                gerir.consultar_id(base)
            elif opcao == 4:
                gerir.pesquisar(base)
            elif opcao == 5:
                gerir.cadastrar(base)
            elif opcao == 6:
                gerir.atualizar(base)
            elif opcao == 7:
                gerir.excluir(base)
            elif opcao == 8:
                gerir.listar_ordenado(base)
            elif opcao == 9:
                gerir.analise(base)
            elif opcao == 10:
                assistente.indicadores()
            elif opcao == 11:
                assistente.exportar_csv()
            elif opcao == 12:
                tela_da_energia.calcular_economia()
            else:
                assistente.pedir_nota()
                assistente.exportar_csv()
                print("\nObrigado por usar o assistente. Até logo!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nAtendimento encerrado.")


if __name__ == "__main__":
    main()

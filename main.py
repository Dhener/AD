from models import Sistema 
import sys
import matplotlib.pyplot as plt 

sys.stdout.reconfigure(encoding='utf-8')

def plot_resultados(sistema):
    utilizacoes = sistema.calcular_utilização()
    servidores = list(sistema.servidores.keys())

    # Plot de utilização dos servidores
    plt.figure(figsize=(10, 6))
    plt.bar(servidores, utilizacoes, color=['blue', 'orange', 'green'])
    plt.title('Utilização dos Servidores')
    plt.xlabel('Servidores')
    plt.ylabel('Utilização (%)')
    plt.ylim(0, 1)
    plt.xticks(rotation=45)
    plt.show()

    # Histograma de tempos no sistema
    plt.figure(figsize=(10, 6))
    plt.hist(sistema.tempos_no_sistema_de_cada_job, bins=30, alpha=0.7, color='purple')
    plt.title('Histograma de Tempos no Sistema')
    plt.xlabel('Tempo no Sistema')
    plt.ylabel('Frequência')
    plt.show()

    # Evolução do tamanho das filas
    plt.figure(figsize=(14, 8))
    for servidor_nome, servidor in sistema.servidores.items():
        plt.plot(servidor.eventos_tempo, servidor.tamanhos_da_fila, label=f'Fila {servidor_nome}')
    plt.title('Tamanho das Filas ao Longo do Tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Tamanho da Fila')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":

    print("## Métricas do caso 1")

    print()

    sistema1 = Sistema(10000, 10000, "constante")
    sistema1.planejar_chegadas()
    sistema1.rodar_o_sistema()
    media1, desvio_padrão1 = sistema1.calcular_metricas()
    print(f"Média do tempo: {media1}")
    print(f"Desvio padrão: {desvio_padrão1}")
    #plot_resultados(sistema1)

    print()

    print("## Métricas do caso 2")

    print()

    sistema2 = Sistema(10000, 10000, "uniforme")
    sistema2.planejar_chegadas()
    sistema2.rodar_o_sistema()
    media2, desvio_padrão2 = sistema2.calcular_metricas()
    print(f"Média do tempo: {media2}")
    print(f"Desvio padrão: {desvio_padrão2}")
    #plot_resultados(sistema2)

    print()

    print("## Métricas do caso 3")

    print()

    sistema3 = Sistema(10000, 10000, "exponencial")
    sistema3.planejar_chegadas()
    sistema3.rodar_o_sistema()
    media3, desvio_padrão3 = sistema3.calcular_metricas()
    print(f"Média do tempo: {media3}")
    print(f"Desvio padrão: {desvio_padrão3}")
    #plot_resultados(sistema3)

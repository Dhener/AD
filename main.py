from models import Sistema 

if __name__ == "__main__":

    sistema1 = Sistema(10000, 10000, "constante")
    sistema1.planejar_chegadas()
    sistema1.rodar_o_sistema()
    media1, desvio_padrão1 = sistema1.calcular_metricas()
    print(f"Média do tempo: {media1}")
    print(f"Desvio padrão: {desvio_padrão1}")
    sistema1.calcular_utilização()

    print()

    sistema2 = Sistema(10000, 10000, "uniforme")
    sistema2.planejar_chegadas()
    sistema2.rodar_o_sistema()
    media2, desvio_padrão2 = sistema2.calcular_metricas()
    print(f"Média do tempo: {media2}")
    print(f"Desvio padrão: {desvio_padrão2}")

    print()

    sistema3 = Sistema(10000, 10000, "exponencial")
    sistema3.planejar_chegadas()
    sistema3.rodar_o_sistema()
    media3, desvio_padrão3 = sistema3.calcular_metricas()
    print(f"Média do tempo: {media3}")
    print(f"Desvio padrão: {desvio_padrão3}")
import heapq
from random import uniform, seed
from math import log
import numpy as np

seed(42)

def inversa_da_cdf(Lambda):
    """ Processo de poisson que gera tempos com distribuição exponencial"""
    u = uniform(0,1)
    x = (-1) * log(1 - u) / Lambda
    #x = round(x, 4)
    return x

class Job:
  def __init__(self, tempo_na_entrada):
    self.tempo_na_entrada = tempo_na_entrada
    self.tempo_na_saida = None

  def processar(self, tempo_na_saida):
    self.tempo_na_saida = tempo_na_saida


class Servidor:
    def __init__(self, nome, tipo_do_tempo_de_serviço):
        self.nome = nome
        self.fila = []
        self.ocupado = False
        self.job_em_processamento = None
        self.total_de_jobs = 0
        self.tipo_do_tempo_de_serviço = tipo_do_tempo_de_serviço
        self.tempo_ocupado = 0  # Serve para calculo da utilização
        self.tamanhos_da_fila = []  # Rastrear tamanhos da fila ao longo do tempo
        self.eventos_tempo = [] # Rastrear tempos do tamanho da fila ao longo do tempo


    def empilhar(self, job, tempo_do_evento, eventos):
        self.fila.append(job)
        if not self.ocupado:
            self.processar(tempo_do_evento, eventos)

    def gerar_tempo_de_serviço(self, tipo):
        if tipo == "constante":
            if self.nome == "S1":
                return 0.4
            elif self.nome == "S2":
                return 0.6
            else:
                return 0.95
        elif tipo == "uniforme":
            if self.nome == "S1":
                return uniform(0.1, 0.7)
            elif self.nome == "S2":
                return uniform(0.1, 1.1)
            else:
                return uniform(0.1, 1.8)
        else:
            if self.nome == "S1":
                return inversa_da_cdf(1/0.4)
            elif self.nome == "S2":
                return inversa_da_cdf(1/0.6)
            else:
                return inversa_da_cdf(1/0.95)

    def processar(self, tempo_do_evento, eventos):

        if len(self.fila) > 0:

            self.job_em_processamento = self.fila.pop(0)

            tempo_de_serviço = self.gerar_tempo_de_serviço(self.tipo_do_tempo_de_serviço)
            self.job_em_processamento.processar(tempo_do_evento + tempo_de_serviço)
            self.total_de_jobs += 1

            evento = (tempo_do_evento + tempo_de_serviço, "saída", self.nome)
            heapq.heappush(eventos, evento)

            self.tempo_ocupado += tempo_de_serviço # Serve para calculo da utilização
            
            self.tamanhos_da_fila.append(len(self.fila)) # Atualizar tamanho da fila para análise
            self.eventos_tempo.append(tempo_do_evento)
            self.ocupado = True

    def retornar_job_processado(self, tempo_do_evento, eventos):
        job_finalizado = self.job_em_processamento
        self.ocupado = False
        self.job_em_processamento = None
        self.processar(tempo_do_evento, eventos)
        return job_finalizado

class Sistema:
    def __init__(self, próximos_jobs, warmup_jobs, tipo_do_tempo_de_serviço):
        self.servidores = {"S1": Servidor("S1", tipo_do_tempo_de_serviço), "S2": Servidor("S2", tipo_do_tempo_de_serviço), "S3": Servidor("S3", tipo_do_tempo_de_serviço)}
        self.jobs_completados = 0
        self.próximos_jobs = próximos_jobs
        self.warmup_jobs = warmup_jobs
        self.tempos_no_sistema_de_cada_job = []
        self.eventos = []
        self.tempo_total = 0

    def planejar_chegadas(self):
        """Planeja todos os eventos de chegada antes do processamento."""

        tempo_atual = 0
        total_jobs = self.warmup_jobs + self.próximos_jobs

        for _ in range(total_jobs):
            evento_chegada = (tempo_atual, "chegada", "S1")
            heapq.heappush(self.eventos, evento_chegada)
            tempo_atual += inversa_da_cdf(2)  # Gerando tempo entre chegadas

    def rodar_o_sistema(self):
        """Executa o processamento baseado na fila de eventos."""
        while self.jobs_completados < self.warmup_jobs + self.próximos_jobs:

            evento = heapq.heappop(self.eventos)

            tempo_do_evento = evento[0]
            tipo_de_evento = evento[1]
            servidor = self.servidores[evento[2]]

            if tipo_de_evento == "chegada":
                """ Processar evento programado para chegada """

                job = Job(tempo_do_evento) # Criando um Job chegando no servidor 1

                self.servidores["S1"].empilhar(job, tempo_do_evento, self.eventos) # Empilhando o Job na fila do servidor 1

            else:
                """ Processar evento programado para saída """

                job_finalizado = servidor.retornar_job_processado(tempo_do_evento, self.eventos) # Job que acabou de sair do servidor

                if servidor.nome == "S1":
                    """ Caso o job estiver saindo do servidor 1"""

                    p1 = uniform(0, 1) 

                    if p1 <= 0.5:
                        """ Probabilidade de aceitação para o job ir para o servidor 2 """

                        self.servidores["S2"].empilhar(job_finalizado, tempo_do_evento, self.eventos)

                    else:
                        """ Probabilidade de aceitação para o job ir para o servidor 3 """

                        self.servidores["S3"].empilhar(job_finalizado, tempo_do_evento, self.eventos)

                elif servidor.nome == "S2":
                    """ Caso o job estiver saindo do servidor 2 """

                    p2 = uniform(0, 1)

                    if p2 <= 0.2:
                        """ Probabilidade de aceitação para o job voltar para o servidor 2 """

                        self.servidores["S2"].empilhar(job_finalizado, tempo_do_evento, self.eventos)

                    else:
                        """ Probabilidade de aceitação para o job sair do servidor 2 """

                        if self.jobs_completados >= self.warmup_jobs:
                            """ Considerando apenas os Jobs depois dos 10.000 descartados """
                            self.tempos_no_sistema_de_cada_job.append(job_finalizado.tempo_na_saida - job_finalizado.tempo_na_entrada)

                        self.jobs_completados += 1
                else:
                    # servidor.nome == "S3"
                    """ Probabilidade de aceitação para o job sair do servidor 3 """

                    if self.jobs_completados >= self.warmup_jobs:
                        """ Considerando apenas os Jobs depois dos 10.000 descartados """
                        self.tempos_no_sistema_de_cada_job.append(job_finalizado.tempo_na_saida - job_finalizado.tempo_na_entrada)

                    self.jobs_completados += 1

            self.tempo_total = tempo_do_evento # Serve para calculo da utilização

    def calcular_metricas(self):
        média_do_tempo = np.mean(self.tempos_no_sistema_de_cada_job)
        desvio_padrão = np.std(self.tempos_no_sistema_de_cada_job)
        return média_do_tempo, desvio_padrão

    def calcular_utilização(self):
        utilizações = []
        for nome, servidor in self.servidores.items():
           utilizações.append(servidor.tempo_ocupado/self.tempo_total)
        return utilizações

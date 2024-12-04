import heapq
from random import uniform
from math import log
import numpy as np

def inverse_of_cdf(Lambda):
    u = uniform(0,1)
    x = (-1) * log(1 - u) / Lambda
    x = round(x, 4)
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
                return inverse_of_cdf(1/0.4)
            elif self.nome == "S2":
                return inverse_of_cdf(1/0.6)
            else:
                return inverse_of_cdf(1/0.95)

    def processar(self, tempo_do_evento, eventos):

        if len(self.fila) > 0:
            self.job_em_processamento = self.fila.pop(0)
            tempo_de_serviço = self.gerar_tempo_de_serviço(self.tipo_do_tempo_de_serviço)
            self.job_em_processamento.processar(tempo_do_evento + tempo_de_serviço)
            self.total_de_jobs += 1
            evento = (tempo_do_evento + tempo_de_serviço, id(self), self ,"saída")
            heapq.heappush(eventos, evento)
            #print(f"servidor {self.nome}")
            #print(f"Job na fila: tempo de serviço: {tempo_de_serviço}, tempo do evento: {tempo_do_evento} - tempo_na_entrada: {self.job_em_processamento.tempo_na_entrada} => entrada do job: {self.job_em_processamento.tempo_na_entrada} e saida do job: {self.job_em_processamento.tempo_na_saida}")
            self.ocupado = True
            #print(eventos)

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
            evento_chegada = (tempo_atual, id(self.servidores["S1"]), self.servidores["S1"], "chegada")
            heapq.heappush(self.eventos, evento_chegada)
            tempo_atual += inverse_of_cdf(2)  # Tempo entre chegadas
        #print(self.eventos)

    def rodar_o_sistema(self):
        """Executa o processamento baseado na fila de eventos."""
        while self.jobs_completados < self.warmup_jobs + self.próximos_jobs:
            evento = heapq.heappop(self.eventos)
            #print(f"evento retirado: {evento}")
            tempo_do_evento = evento[0]
            servidor = evento[2]
            tipo_de_evento = evento[3]

            if tipo_de_evento == "chegada":
                """ Processar evento programado para chegada """
                job = Job(tempo_do_evento)
                self.servidores["S1"].empilhar(job, tempo_do_evento, self.eventos)
            else:
                """ Processar evento já programado para saída """
                job_finalizado = servidor.retornar_job_processado(tempo_do_evento, self.eventos)

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
                            self.tempos_no_sistema_de_cada_job.append(job_finalizado.tempo_na_saida - job_finalizado.tempo_na_entrada)
                        self.jobs_completados += 1
                else:
                    # servidor.nome == "S3"
                    """ Probabilidade de aceitação para o job sair do servidor 3 """
                    if self.jobs_completados >= self.warmup_jobs:
                        self.tempos_no_sistema_de_cada_job.append(job_finalizado.tempo_na_saida - job_finalizado.tempo_na_entrada)
                    self.jobs_completados += 1

    def calcular_metricas(self):
        média_do_tempo = np.mean(self.tempos_no_sistema_de_cada_job)
        desvio_padrão = np.std(self.tempos_no_sistema_de_cada_job)
        return média_do_tempo, desvio_padrão

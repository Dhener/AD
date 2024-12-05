# Simulação de Processamento em Servidores

## **Objetivo**
Este projeto simula o processamento de jobs em um sistema composto por três servidores interconectados. Através de uma abordagem baseada em eventos, a simulação analisa o desempenho do sistema, calculando métricas como o tempo médio no sistema e o desvio padrão dos tempos processados.

---

## **Descrição do Sistema**
### Estrutura do Sistema
O sistema é composto por:
1. **Job**: Unidade de trabalho que passa pelos servidores.
2. **Servidor**: Componente que processa jobs, gerencia filas e define tempos de serviço.
3. **Sistema**: Gerencia os servidores, eventos de chegada/saída e coleta métricas de desempenho.

---

## **Estruturas de Dados Utilizadas e Complexidades**

### **1. Fila de Jobs (`list`)**
- Cada servidor possui uma fila de jobs implementada com uma lista Python (`list`).
- **Operações**:
  - **Adição de um job ao final (`append`)**: O(1).
  - **Remoção do primeiro job (`pop(0)`)**: O(n), pois os elementos precisam ser realocados.

### **2. Fila de Eventos (`heapq`)**
- A fila de eventos utiliza uma heap mínima para processar os eventos em ordem cronológica.
- **Operações**:
  - **Inserção de evento (`heapq.heappush`)**: O(log n).
  - **Extração do menor evento (`heapq.heappop`)**: O(log n).
- A estrutura é eficiente para cenários onde é necessário manter os eventos ordenados dinamicamente.

### **3. Lista de Tempos (`list`)**
- Utilizada para armazenar os tempos que cada job passa no sistema.
- **Operações**:
  - **Adição de elementos (`append`)**: O(1).
  - **Cálculo de métricas (`mean`, `std`)**: O(n).

Essas estruturas foram escolhidas para balancear simplicidade e eficiência em um sistema baseado em eventos.

---

## **Classes e Funções**
### **Funções Utilitárias**
- **`inverse_of_cdf(Lambda)`**  
  Calcula o tempo entre eventos com base em uma distribuição exponencial.  
  - **Parâmetro**: `Lambda` (taxa da distribuição).  
  - **Retorna**: Tempo gerado.

---

### **Classe `Job`**
Representa um job no sistema.  
#### **Atributos**
- `tempo_na_entrada`: Tempo de entrada do job no sistema.
- `tempo_na_saida`: Tempo de saída do job (após processamento).

#### **Métodos**
- `processar(tempo_na_saida)`: Registra o tempo de saída do job.

---

### **Classe `Servidor`**
Simula um servidor que processa jobs.  
#### **Atributos**
- `nome`: Identificação do servidor.
- `fila`: Lista de jobs esperando para serem processados.
- `ocupado`: Indica se o servidor está em uso.
- `tipo_do_tempo_de_serviço`: Tipo de distribuição usada para calcular o tempo de serviço.

#### **Métodos**
- `empilhar(job, tempo_do_evento, eventos)`: Adiciona um job à fila e inicia o processamento, se o servidor estiver disponível.
- `gerar_tempo_de_serviço(tipo)`: Gera o tempo necessário para processar um job, baseado no tipo especificado (`constante`, `uniforme`, ou `exponencial`).
- `processar(tempo_do_evento, eventos)`: Processa um job da fila e agenda o próximo evento de saída.
- `retornar_job_processado(tempo_do_evento, eventos)`: Finaliza o processamento de um job e o retorna.

---

### **Classe `Sistema`**
Gerencia o funcionamento geral da simulação.  
#### **Atributos**
- `servidores`: Dicionário com os três servidores do sistema.
- `jobs_completados`: Número de jobs processados.
- `tempos_no_sistema_de_cada_job`: Lista de tempos totais que os jobs passaram no sistema.
- `eventos`: Fila de eventos programados.

#### **Métodos**
- `planejar_chegadas()`: Planeja os eventos de chegada dos jobs no servidor 1, baseado em uma distribuição exponencial.
- `rodar_o_sistema()`: Processa os eventos em ordem cronológica, simulando o fluxo de jobs pelo sistema.
- `calcular_metricas()`: Calcula e retorna métricas como a média e o desvio padrão do tempo dos jobs no sistema.

---

## **Como Executar**
1. Certifique-se de que o Python 3.x e as dependências necessárias estejam instalados (`numpy`, etc.).
2. Configure os parâmetros da simulação no código principal, como o número de jobs, o número de warm up jobs e o tipo de tempo de serviço.
3. Execute o código usando:
   ```bash
   python3 main.py

from tkinter import *
from PIL import Image, ImageTk #pip install pillow
import time
import threading
import numpy as np
import random

class Window(Frame):

     def __init__(self, master=None):
        
        self.populacao_individuos = []
        self.max_fitness = 0
        self.geracao = 0
        self.numGeracao = 10
        self.numExecucao = 130
        self.individuos = 2

        self.axisX = 50
        self.axisY = 70

        self.obstacle1X = 100
        self.obstacle1Y = 70

        self.obstacleList = []
        linha = 100
        coluna = 50
        proximaLinha = False
        index = 0
        for i in range(10):

          if index == 5:
               proximaLinha = True
               coluna = 50

          if proximaLinha:
               linha += 150
               proximaLinha = False

          self.obstacleList.append([linha, coluna])
          index += 1
          coluna += 50

        self.chegada1X = 500
        self.chegada1Y = 5

        self.linhaEliminatoriaX = 5
        self.avancaLinhaEliminatoria = True

        self.tamanhoImagem = [18, 16]

        self.cenario = []

        self.limiteHorizontalSuperior = [0, 0, 5, 499]
        self.limiteHorizontalInferior = [399, 0, 5, 499]
        self.limiteVerticalEsquerda = [0, 0, 399, 5]
        self.linhaChegada = [0, 499, 5, 399]

        for i in range(400):
             self.cenario = self.cenario + [[0]*500]
             for j in range(500):

               if self.limiteHorizontalSuperior[0] + self.limiteHorizontalSuperior[2] >= i and self.limiteHorizontalSuperior[1] + self.limiteHorizontalSuperior[3] >= j:
                    self.cenario[i][j] = 1
               elif self.limiteHorizontalInferior[0] <= i and self.limiteHorizontalInferior[1] + self.limiteHorizontalInferior[3] >= j:
                    self.cenario[i][j] = 1
               elif self.limiteVerticalEsquerda[2] >= i and self.limiteVerticalEsquerda[3] >= j:
                    self.cenario[i][j] = 1
               elif self.linhaChegada[0] +  self.linhaChegada[3] >= i and self.linhaChegada[1] <= j:
                    self.cenario[i][j] = -1
               elif (j >= self.obstacle1X and j  <= self.obstacle1X + self.tamanhoImagem[0]) and (i >= self.obstacle1Y - self.tamanhoImagem[1] and i<=  self.obstacle1Y + self.tamanhoImagem[1]):
                    self.cenario[i][j] = 1
               # elif (i >= self.chegada1X and i  <= self.chegada1X + self.tamanhoImagem[0]) and (j <= self.chegada1Y and j>=  self.chegada1Y - self.tamanhoImagem[1]):
               #      self.cenario[i][j] = -1
               else:
                    self.cenario[i][j] = 0
               for x in range(len(self.obstacleList)):
                    if (i >= self.obstacleList[x][0]  - self.tamanhoImagem[1] and i  <= self.obstacleList[x][0] + self.tamanhoImagem[1]) and (j >= self.obstacleList[x][1] and j <=  self.obstacleList[x][1] + self.tamanhoImagem[0]):
                         self.cenario[i][j] = 1

        Frame.__init__(self, master)
        self.master = master
        
        self.pack(fill=BOTH, expand=1)

        leftButton = Button(self, text="<", command=self.clickLeft)
        leftButton.place(x=250, y=430)

        rightButton = Button(self, text=">", command=self.clickRight)
        rightButton.place(x=350, y=430)

        leftButton = Button(self, text="/\\", command=self.clickUp)
        leftButton.place(x=300, y=410)

        rightButton = Button(self, text="\/", command=self.clickDown)
        rightButton.place(x=300, y=450)


        rightButton = Button(self, text="Inicia", command=self.executaGeracoes)
        rightButton.place(x=50, y=420)

        rightButton = Button(self, text="Verifica Resultado", command=self.verificaResultado)
        rightButton.place(x=50, y=450)        


        imagemObstacle = PhotoImage(file="./img/obstacle.png")
        self.label = Label(master, image=imagemObstacle)
        self.label.imagem = imagemObstacle
        self.label.place(x=self.obstacle1X, y=self.obstacle1Y)

        for i in range(len(self.obstacleList)):
          imagemObstacle = PhotoImage(file="./img/obstacle.png")
          self.label = Label(master, image=imagemObstacle)
          self.label.imagem = imagemObstacle

          self.label.place(x=self.obstacleList[i][1], y=self.obstacleList[i][0])

        self.frameLinhaEliminatoria = Frame(master=master, width=5, height=395, bg="red")
        self.frameLinhaEliminatoria.place(x=self.linhaEliminatoriaX, y=5)

        frame1 = Frame(master=master, width=5, height=400, bg="black")
        frame1.place(x=0, y=0)

        frame1 = Frame(master=master, width=5, height=400, bg="black")
        frame1.place(x=795, y=0)

        frame1 = Frame(master=master, width=800, height=5, bg="black")
        frame1.place(x=0, y=0)

        frame1 = Frame(master=master, width=800, height=5, bg="black")
        frame1.place(x=0, y=400)

        frame1 = Frame(master=master, width=10, height=395, bg="blue")
        frame1.place(x=self.chegada1X, y=5)

     # def clickExitButton(self):
     #           exit()

     def clickLeft(self):
          self.axisX -= 3
          self.w.place(x=self.axisX, y=self.axisY)
          self.verificaObstaculos(self.axisX,self.axisY)
          print('X: '+str(self.axisX)+' Y: '+str(self.axisY))

     def clickRight(self):
          self.axisX += 3
          self.w.place(x=self.axisX, y=self.axisY)
          self.verificaObstaculos(self.axisX,self.axisY)
          print('X: '+str(self.axisX)+' Y: '+str(self.axisY))

     def clickUp(self):
         self.axisY -= 3
         self.w.place(x=self.axisX, y=self.axisY)
         self.verificaObstaculos(self.axisX,self.axisY)
         print('X: '+str(self.axisX)+' Y: '+str(self.axisY))

     def clickDown(self):
          self.axisY += 3
          self.w.place(x=self.axisX, y=self.axisY)
          self.verificaObstaculos(self.axisX,self.axisY)
          print('X: '+str(self.axisX)+' Y: '+str(self.axisY))

     def verificaObstaculos(self, axisX, axisY):

          verificaTamanhoImagemX = self.tamanhoImagem[0]
          verificaTamanhoImagemY = self.tamanhoImagem[1]

          if (len(self.cenario[0]) < axisX+verificaTamanhoImagemY and 
              len(self.cenario) < axisY) or (
               self.cenario[axisY][axisX] == 1) or (
               self.cenario[axisY][axisX] ==1 or 
               self.cenario[axisY][axisX+verificaTamanhoImagemX] ==1):
               print("colisão")


     def findObstacles(self, x, y):
          deepFind = 1
          initX = 0
          initY = 0
          if x - deepFind > 0:
               initX = x - deepFind
          if y - deepFind > 0:
               initY = y - deepFind
          result = [0,0,0,0]
          for i in range(initX , + + x):
               for j in range(initY , deepFind + y):
                    if self.cenario[i][j] == 1:
                         if i == x+1:
                              result = [0,0,1,0]
                         if j == y+1:
                              result = [1,0,0,0]
                         if j == y-1:
                              result = [0,1,0,0]

          return result


     def movimentaLinhaEliminatoriaThread(self):
          x = threading.Thread(target=self.movimentaLinhaEliminatoria, args=())
          print("start thread: movimentaLinhaEliminatoriaThread")
          x.start()
          print("finish thread: movimentaLinhaEliminatoriaThread")

     def movimentaLinhaEliminatoria(self, inicializaLinhaEliminatoria=5):
          numGeracao = self.geracao
          self.linhaEliminatoriaX = inicializaLinhaEliminatoria
          self.avancaLinhaEliminatoria = True
          while self.avancaLinhaEliminatoria:
               time.sleep(0.3)
               self.frameLinhaEliminatoria.place(x=self.linhaEliminatoriaX, y=5)
               self.linhaEliminatoriaX += 5
               
               if not self.buscaAutomato():
                    self.avancaLinhaEliminatoria = False

               if numGeracao != self.geracao:
                    print("################Nova Geração################")
                    self.linhaEliminatoriaX = 5
                    self.avancaLinhaEliminatoria = False
               if self.linhaEliminatoriaX >= 498:
                    self.avancaLinhaEliminatoria = False
     
     def buscaAutomato(self):
          somaIndividuosEliminados = 0
          for i in range(len(self.populacao_individuos)):
               if self.populacao_individuos[i]['axisX'] <= self.linhaEliminatoriaX and ( 
                    'eliminado' in self.populacao_individuos[i] and self.populacao_individuos[i]['eliminado'] != 1) and (
                    'colisao' in self.populacao_individuos[i] and self.populacao_individuos[i]['colisao'] != 1) and (
                    'chegou' in self.populacao_individuos[i] and self.populacao_individuos[i]['chegou'] != 1):
                    self.populacao_individuos[i]['eliminado'] = 1
                    automato = self.populacao_individuos[i]['label']
                    automato.after(100, automato.destroy())
                    print("Eliminado")
                    return False
               elif ('eliminado' in self.populacao_individuos[i] and self.populacao_individuos[i]['eliminado'] == 1) or (
                    'colisao' in self.populacao_individuos[i] and self.populacao_individuos[i]['colisao'] == 1) or (
                    'chegou' in self.populacao_individuos[i] and self.populacao_individuos[i]['chegou'] == 1):
                    somaIndividuosEliminados += 1
                    if somaIndividuosEliminados >= len(self.populacao_individuos):
                         return False

          return True

     def executaGeracoes(self):
          x = 50
          y = 200
          if self.geracao >= self.numGeracao:     
               print("Finaliza número de gerações")
               self.geracao = 0
               return
          
          for i in range(self.individuos):
               self.executaMovimentoThead(x, y, i)
               
          self.movimentaLinhaEliminatoriaThread()
          self.esperaFinalizarGeracao()

     def esperaFinalizarGeracao(self):
          x = threading.Thread(target=self.verificaGeracao, args=())
          print("start thread: verificaGeracao")
          x.start()
          print("finish thread: verificaGeracao")

     def verificaGeracao(self):
          verifica = True
          while verifica:
               verifica = False
               time.sleep(5)
               if len(self.populacao_individuos) == 0:
                    verifica = False
               else:
                    somaColisao = 0
                    for i in range(len(self.populacao_individuos)):
                         if 'colisao' in self.populacao_individuos and self.populacao_individuos[i]['colisao'] == 1:
                              somaColisao += 1
                         if self.populacao_individuos[i]['executa'] < self.numExecucao and ((not 'colisao' in self.populacao_individuos[i]) or ('colisao' in self.populacao_individuos[i] and self.populacao_individuos[i]['colisao'] < 1)):
                         # if self.populacao_individuos[i]['executa'] < self.numExecucao:
                              verifica = True
                    if somaColisao >= len(self.populacao_individuos):
                         verifica = False
          self.geracao += 1
          self.gera_nova_popupacao()
          self.executaGeracoes()

     def executaMovimentoThead(self, x = 50, y = 70, individuo = 1):
          x = threading.Thread(target=self.move, args=(x, y, 1, individuo))
          print("start thread: move")
          x.start()
          print("finish thread: move")
          
     def sigmoid(self, soma):
          return 1 / (1 + np.exp(-soma))

     def sigmoidDerivada(self, sig):
          return sig * (1 - sig)

     def neuralNetwork(self, entradas, individuo):
          #print('entradas: ',entradas)
          # entradas = np.array(
          #      [[0, #esquerda
          #        0, #direita
          #        0]] #frente
          # )
          
          individuo_selecionado = [element for element in  self.populacao_individuos if element['individuo'] == individuo]

          if len(individuo_selecionado)>0:
               individuo_selecionado = individuo_selecionado[0]
          
          pesos0 = []
          pesos1 = []

          if 'pesos0' in individuo_selecionado and len(individuo_selecionado['pesos0']) > 0: 
               pesos0 = individuo_selecionado['pesos0']
               pesos1 = individuo_selecionado['pesos1']
          else:
               pesos0 = 2*np.random.random((3,3)) - 1
               pesos1 = 2*np.random.random((3,3)) - 1


          individuo_selecionado['pesos0'] = pesos0
          individuo_selecionado['pesos1'] = pesos1

          camadaSaida = []

          camadaEntrada = entradas
          somaSinapse0 = np.dot(camadaEntrada, pesos0)
          camadaOculta = self.sigmoid(somaSinapse0)
          
          somaSinapse1 = np.dot(camadaOculta, pesos1)
          camadaSaida = self.sigmoid(somaSinapse1)

          return camadaSaida.round()

     # Crossover traits between two Genetic Neural Networks
     def dynamic_crossover(self, nn1, nn2):
          # Lists for respective weights
          nn1_weights = []
          nn2_weights = []
          child_weights = []

          # for layer in nn1['pesos0']:
          #      nn1_weights.append(layer)
          nn1_weights.append(nn1['pesos0'])
          nn1_weights.append(nn1['pesos1'])


          # for layer in nn2['pesos1']:
          #      nn2_weights.append(layer)

          nn2_weights.append(nn2['pesos0'])
          nn2_weights.append(nn2['pesos1'])

          # Iterate through all weights from all layers for crossover
          for i in range(0, len(nn1_weights)):

               split = random.randint(0, np.shape(nn1_weights[i])[1]-1)
               # Iterate through after a single point and set the remaing cols to nn_2
               for j in range(split, np.shape(nn1_weights[i])[1]-1):
                    nn1_weights[i][:, j] = nn2_weights[i][:, j]

               child_weights.append(nn1_weights[i])


          self.mutation(child_weights)

          # child = GeneticNeuralNetwork(child_weights)
          # return child
          return child_weights

     def mutation(self, child_weights):
          # Add a chance for random mutation
          selection = random.randint(0, len(child_weights)-1)
          mut = random.uniform(0, 1)
          if mut >= .5:
               child_weights[selection] *= random.randint(2, 5)
          else:
               # No mutation
               pass

     def verificaResultado(self):
          print('resultado', self.populacao_individuos)

     def gera_nova_popupacao(self):
          self.populacao_individuos = sorted(self.populacao_individuos, key=lambda x: x['axisX'])
          self.populacao_individuos.reverse()

          for i in range(0, len(self.populacao_individuos)):
               if self.max_fitness < self.populacao_individuos[i]['axisX']:
                    self.max_fitness = self.populacao_individuos[i]['axisX']

          nova_populacao = []
          rangeNovaPopulacao = int(self.individuos/2)
          for i in range(0, rangeNovaPopulacao):
               for j in range(0, 2):
                    # Create a child and add to networks
                    temp = self.dynamic_crossover(self.populacao_individuos[i], random.choice(self.populacao_individuos))
                    # Add to networks to calculate fitness score next iteration
                    self.populacao_individuos[i]['pesos0'] = temp[0]
                    self.populacao_individuos[i]['pesos1'] = temp[1]
                    self.populacao_individuos[i]['colisao'] = 0
                    self.populacao_individuos[i]['eliminado'] = 0
                    nova_populacao.append(self.populacao_individuos[i].copy())
          
          # self.populacao_individuos = list(nova_populacao)
          self.populacao_individuos = nova_populacao

          for i in range(self.individuos):
               self.populacao_individuos[i]['individuo'] = i

          print("individuos", self.populacao_individuos)

     def move(self, axisX = 50, axisY = 70, executa=1, individuo = 1):

          individuo_selecionado = [element for element in  self.populacao_individuos if element['individuo'] == individuo]
          w = []

          if individuo_selecionado:
               individuo_selecionado[0]['executa'] = executa
               individuo_selecionado[0]['axisX'] = axisX
               individuo_selecionado[0]['axisY'] = axisY

               if 'colisao' in individuo_selecionado[0] and individuo_selecionado[0]['colisao'] == 1:
                    imagem = PhotoImage(file="./img/img.png")
                    w = Label(self.master, image=imagem)
                    w.imagem = imagem
                    w.place(x=axisX, y=axisY)
                    individuo_selecionado[0]['label'] = w
                    #individuo_selecionado[0]['colisao'] = 0
               else:     
                    w = individuo_selecionado[0]['label']
          else:

               imagem = PhotoImage(file="./img/img.png")
               w = Label(self.master, image=imagem)
               w.imagem = imagem
               w.place(x=axisX, y=axisY)
               
               individuo_selecionado = [{ 'individuo': individuo, 'executa': executa, 'pesos0': [], 'pesos1': [], 'label': w, 'axisX': axisX, 'axisY': axisY }]
               self.populacao_individuos.append(individuo_selecionado[0])

          if executa >= self.numExecucao:
               # if len(individuo_selecionado) > 0:
               #      individuo_selecionado[0]['colisao'] = 0
               return
          
          time.sleep(0.1)

          verificaTamanhoImagemX = self.tamanhoImagem[0]
          verificaTamanhoImagemY = self.tamanhoImagem[1]

          if len(self.cenario) < axisY + verificaTamanhoImagemY:
               ajuste = len(self.cenario) - (axisY + verificaTamanhoImagemY)
               ajuste -=1
               verificaTamanhoImagemY +=ajuste
          if len(self.cenario[0]) < axisX + verificaTamanhoImagemX:
               ajusteX = len(self.cenario[0]) - (axisX + verificaTamanhoImagemX)
               ajusteX -=1
               verificaTamanhoImagemX +=ajusteX


          #resultNeuralNetwork = [0,0,1] #TODO saida [esq, dir, frent, atras]
          # if self.cenario[axisX+20][axisY] == 1:
          #      resultNeuralNetwork = [1,0,0]
          
          # esquerda =  self.cenario[axisY-verificaTamanhoImagemY][axisX] #1 if self.cenario[axisY-verificaTamanhoImagemY][axisX] == 1 else 0 
          # direita = self.cenario[axisY+verificaTamanhoImagemY][axisX] #1 if self.cenario[axisY+verificaTamanhoImagemY][axisX] == 1 else 0 
          # frente = self.cenario[axisY][axisX+verificaTamanhoImagemX] #1 if self.cenario[axisY][axisX+verificaTamanhoImagemX] == 1 else 0 

          esquerda =  1 if self.cenario[axisY-verificaTamanhoImagemY][axisX] == 1 else 0 
          direita = 1 if self.cenario[axisY+verificaTamanhoImagemY][axisX] == 1 else 0 
          frente = 1 if self.cenario[axisY][axisX+verificaTamanhoImagemX] == 1 else 0 

          entrada = np.array([[esquerda, direita, frente]])

          resultNeuralNetwork = self.neuralNetwork(entrada, individuo) #Rede Neural
          # resultNeuralNetwork = np.array(
		# [[0, #esquerda
		#   1, #direita
		#   0]] #frente
          # )
          # individuo_selecionado[0]['pesos0'] = 2*np.random.random((3,3)) - 1
          # individuo_selecionado[0]['pesos1'] = 2*np.random.random((3,3)) - 1

          print('Individuo: '+ str(individuo) +' Executa: '+ str(executa))

          try:

               if self.cenario[axisY][axisX+verificaTamanhoImagemX] == -1 :
                    print("chegou")
                    individuo_selecionado[0]['chegou'] = 1
                    return
               if self.linhaEliminatoriaX == axisX:
                    print("eliminado")
                    individuo_selecionado[0]['colisao'] = 1
                    return

               if (len(self.cenario[0]) < axisX+verificaTamanhoImagemY and 
                    len(self.cenario) < axisY) or (
                    self.cenario[axisY][axisX] == 1) or (
                    self.cenario[axisY][axisX] ==1 or 
                    self.cenario[axisY][axisX+verificaTamanhoImagemX] ==1):

                    print("colisão")
                    individuo_selecionado[0]['colisao'] = 1      
                    w.after(100, w.destroy())
                    return
          
               if resultNeuralNetwork[0, 0] == 1:
                    axisY -= 5
                    w.place(x=axisX, y=axisY)

               if resultNeuralNetwork[0, 1] == 1:
                    axisY += 5
                    w.place(x=axisX, y=axisY)

               if resultNeuralNetwork[0, 2] == 1:
                    axisX += 5
                    w.place(x=axisX, y=axisY)
          except IndexError as err:
               print("Index error", err)
               individuo_selecionado = [element for element in  self.populacao_individuos if element['individuo'] == individuo]
               if individuo_selecionado:
                    self.move(axisX, axisY, executa, individuo)
               else:
                    print("Individuo não encontrado")
          except Exception as err:
               print("error", err)
               imagem = PhotoImage(file="C:/projetos/python/AlgoritmoGenetico/test1/img/img.png")
               w = Label(self.master, image=imagem)
               w.imagem = imagem
               w.place(x=axisX, y=axisY)
          
          executa += 1

          self.move(axisX, axisY, executa, individuo)


root = Tk()

app = Window(root)


root.wm_title("Algoritmo Genético com Redes Neurais")

root.geometry("800x600")

# show window
root.mainloop()

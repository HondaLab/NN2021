import numpy as np
import matplotlib.pyplot as plt

input_data = np.arange(0,np.pi*2,0.1)
correct_data = np.sin(input_data)
input_data = (input_data-np.pi)/np.pi
n_data = len(correct_data)

n_in =1
n_mid = 3
n_out = 1

wb_width = 0.01
eta = 0.2
epoch = 15001
interval = 1500
m_sumgrad_w = 0
m_sumgrad_b = 0
o_sumgrad_w = 0
o_sumgrad_b = 0

class MiddleLayer:
   def __init__(self,n_upper,n):
       self.w = wb_width*np.random.randn(n_upper,n)
       self.b = wb_width*np.random.randn(n)

   def forward(self,x):
       self.x = x
       u = np.dot(x,self.w) + self.b
       self.y = 1/(1+np.exp(-u))

   def backward(self,grad_y):
       delta = grad_y*(1-self.y)*self.y
       self.grad_w = np.dot(self.x.T,delta)
       self.grad_b = np.sum(delta,axis=0)

       self.grad_x = np.dot(delta,self.w.T)

   def update(self,eta,m_sumgrad_w,m_sumgrad_b):
       self.w -= eta*m_sumgrad_w
       self.b -= eta*m_sumgrad_b


class OutputLayer:
   def __init__(self,n_upper,n):
       self.w = wb_width*np.random.randn(n_upper,n)
       self.b = wb_width*np.random.randn(n)

   def forward(self,x):
       self.x = x
       u = np.dot(x,self.w) + self.b
       self.y = u

   def backward(self,t):
       delta = self.y - t

       self.grad_w = np.dot(self.x.T,delta)
       self.grad_b = np.sum(delta,axis=0)

       self.grad_x = np.dot(delta,self.w.T)
       return self.grad_w,self.grad_b,self.grad_x

   def update(self,eta,o_sumgrad_w,o_sumgrad_b):
       self.w -= eta*o_sumgrad_w
       self.b -= eta*o_sumgrad_b

middle_layer = MiddleLayer(n_in,n_mid)
output_layer = OutputLayer(n_mid,n_out)

for i in range(epoch):

   index_random = np.arange(n_data)
   np.random.shuffle(index_random)

   total_error = 0
   plot_x = []
   plot_y = []

   for idx in index_random:

       x = input_data[idx:idx+1]
       t = correct_data[idx:idx+1]

       middle_layer.forward(x.reshape(1,1))
       output_layer.forward(middle_layer.y)

       grad_w,grad_b,grad_x = output_layer.backward(t.reshape(1,1))
       middle_layer.backward(grad_x)

       m_sumgrad_w += middle_layer.grad_w
       m_sumgrad_b += middle_layer.grad_b
       o_sumgrad_w += grad_w
       o_sumgrad_b += grad_b

       if i%interval == 0:

          y = output_layer.y.reshape(-1)

          total_error += 1.0/2.0+np.sum(np.square(y-t))

          plot_x.append(x)
          plot_y.append(y)

   m_sumgrad_w = m_sumgrad_w / n_data
   m_sumgrad_b = m_sumgrad_b / n_data
   
   o_sumgrad_w = o_sumgrad_w / n_data
   o_sumgrad_b = o_sumgrad_b / n_data

   middle_layer.update(eta,m_sumgrad_w,m_sumgrad_b)
   output_layer.update(eta,o_sumgrad_w,o_sumgrad_b)


   if i%interval == 0:

          plt.plot(input_data,correct_data,linestyle="dashed")
          plt.scatter(plot_x,plot_y,marker="+")
          plt.show()

          print("Epoch:" +str(i) + "/" + str(epoch),"Error" + str(total_error/n_data))
              

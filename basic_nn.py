import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import SGD
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class BasicNN(nn.Module):

    def __init__(self):
        super().__init__()
        
        self.w00 = nn.Parameter(torch.tensor(1.7), requires_grad=False)
        self.b00 = nn.Parameter(torch.tensor(-0.85), requires_grad=False)
        self.w01 = nn.Parameter(torch.tensor(-40.8), requires_grad=False)
        
        self.w10 = nn.Parameter(torch.tensor(12.6), requires_grad=False)
        self.b10 = nn.Parameter(torch.tensor(0.0), requires_grad=False)
        self.w11 = nn.Parameter(torch.tensor(2.7), requires_grad=False)
        
        self.final_bias = nn.Parameter(torch.tensor(-16.0), requires_grad=False)

    def forward(self, input):
        input_to_top_relu = input * self.w00 + self.b00
        top_relu_output = F.relu(input_to_top_relu)
        scaled_top_relu_output = top_relu_output * self.w01

        input_to_bottom_relu = input * self.w10 + self.b10
        bottom_relu_output = F.relu(input_to_bottom_relu)
        scaled_bottom_relu_output = bottom_relu_output * self.w11

        input_to_final_relu = scaled_top_relu_output + scaled_bottom_relu_output + self.final_bias

        output = F.relu(input_to_final_relu)

        return output

class BasicNN_train(nn.Module):

    def __init__(self):
        super().__init__()
        
        self.w00 = nn.Parameter(torch.tensor(1.7), requires_grad=False)
        self.b00 = nn.Parameter(torch.tensor(-0.85), requires_grad=False)
        self.w01 = nn.Parameter(torch.tensor(-40.8), requires_grad=False)
        
        self.w10 = nn.Parameter(torch.tensor(12.6), requires_grad=False)
        self.b10 = nn.Parameter(torch.tensor(0.0), requires_grad=False)
        self.w11 = nn.Parameter(torch.tensor(2.7), requires_grad=False)
        
        self.final_bias = nn.Parameter(torch.tensor(0.), requires_grad=True)

    def forward(self, input):
        input_to_top_relu = input * self.w00 + self.b00
        top_relu_output = F.relu(input_to_top_relu)
        scaled_top_relu_output = top_relu_output * self.w01

        input_to_bottom_relu = input * self.w10 + self.b10
        bottom_relu_output = F.relu(input_to_bottom_relu)
        scaled_bottom_relu_output = bottom_relu_output * self.w11

        input_to_final_relu = scaled_top_relu_output + scaled_bottom_relu_output + self.final_bias

        output = F.relu(input_to_final_relu)

        return output

if __name__ == '__main__':

    model = BasicNN_train()

    output_values = model(input_doses)

    inputs = torch.tensor([0., 0.5, 1.])
    labels = torch.tensor([0., 1., 0.])

    optimizer = SGD(model.parameters(), lr=0.1)

    print("Final bias, before optimization: " + str(model.final_bias.data) + "\n")

    loss_fn = nn.MSELoss()

    epochs = 100
    losses = []

    for epoch in range(epochs):
        
        total_loss = 0

        for iteration in range(len(inputs)):

          input_i = inputs[iteration]
          label_i = inputs[iteration]

          output_i = model(input_i)

          loss = (output_i - label_i)**2

          loss.backward()

          total_loss += float(loss)

        if (total_loss < 0.001):
          print("Num steps: " + str(epochs))
          break
        
        optimizer.step()
        optimizer.zero_grad()

        print("step: " + str(epochs) + " Final Bias: " + str(model.final_bias.data) + "\n")
    
    input_doses = torch.linspace(start=0, end=1, steps=11)

    output_values = model(input_doses)

    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.lineplot(x=input_doses, y=output_values.detach(), color='green', linewidth=2.5)
    plt.xlabel('Input Doses')
    plt.ylabel('Output Values')

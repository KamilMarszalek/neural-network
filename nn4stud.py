#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:51:50 2021

@author: Rafał Biedrzycki
Kodu tego mogą używać moi studenci na ćwiczeniach z przedmiotu Wstęp do Sztucznej Inteligencji.
Kod ten powstał aby przyspieszyć i ułatwić pracę studentów, aby mogli skupić się na algorytmach sztucznej inteligencji. 
Kod nie jest wzorem dobrej jakości programowania w Pythonie, nie jest również wzorem programowania obiektowego, może zawierać błędy.

Nie ma obowiązku używania tego kodu.
"""

import numpy as np

# ToDo tu prosze podac pierwsze cyfry numerow indeksow
p = [1, 8]


L_BOUND = -5
U_BOUND = 5


def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))


x = np.linspace(L_BOUND, U_BOUND, 100)
y = q(x)

np.random.seed(1)


# f logistyczna jako przykład sigmoidalej
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# pochodna fun. 'sigmoid'
def d_sigmoid(x):
    s = 1 / (1 + np.exp(-x))
    return s * (1 - s)


FUNCTION = sigmoid
D_FUNCTION = d_sigmoid


# f. straty
def nloss(y_out, y):
    return (y_out - y) ** 2


# pochodna f. straty
def d_nloss(y_out, y):
    return 2 * (y_out - y)


class DlNet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_out = 0

        self.HIDDEN_L_SIZE = 14
        self.LR = 0.1

        self.W1 = np.random.randn(
            1, self.HIDDEN_L_SIZE
        )  # weights between input and hidden layer
        self.b1 = np.random.randn(
            1, self.HIDDEN_L_SIZE
        )  # bias between input and hidden layer
        self.W2 = np.random.randn(
            self.HIDDEN_L_SIZE, 1
        )  # weights between hidden and output layer
        self.b2 = np.random.randn(1, 1)  # bias between hidden and output layer

    def forward(self, x):
        x_res = x.reshape(-1, 1)
        self.z1 = np.dot(x_res, self.W1) + self.b1
        self.a1 = FUNCTION(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.y_out = self.z2
        return self.y_out

    def predict(self, x):
        return self.forward(x)

    def backward(self, x, y):
        x_res = x.reshape(-1, 1)
        y_res = y.reshape(-1, 1)
        n = x_res.shape[0]

        dLoss_dyOut = d_nloss(self.y_out, y_res)

        dLoss_dz2 = dLoss_dyOut

        dLoss_dW2 = np.dot(self.a1.T, dLoss_dz2) / n
        dLoss_db2 = np.sum(dLoss_dz2, axis=0, keepdims=True) / n

        dLoss_da1 = np.dot(dLoss_dz2, self.W2.T)
        dLoss_dz1 = dLoss_da1 * D_FUNCTION(self.z1)

        dLoss_dW1 = np.dot(x_res.T, dLoss_dz1) / n
        dLoss_db1 = np.sum(dLoss_dz1, axis=0, keepdims=True) / n
        self.W2 -= self.LR * dLoss_dW2
        self.b2 -= self.LR * dLoss_db2
        self.W1 -= self.LR * dLoss_dW1
        self.b1 -= self.LR * dLoss_db1

    def train(self, x_set, y_set, batch_size=16, epochs=20):
        n_samples = len(x_set)
        for epoch in range(epochs):
            indices = np.arange(n_samples)
            np.random.shuffle(indices)
            x_shuffled = x_set[indices]
            y_shuffled = y_set[indices]
            for start_idx in range(0, n_samples, batch_size):
                end_idx = start_idx + batch_size
                x_batch = x_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                self.forward(x_batch)
                self.backward(x_batch, y_batch)
            y_pred = self.forward(x_set)
            loss_val = np.mean(nloss(y_pred.flatten(), y_set))
            print(f"Epoch: {epoch+1}/{epochs}, Loss: {loss_val:.5f}")


nn = DlNet(x, y)

nn.train(x, y, batch_size=20, epochs=1000)

yh = nn.predict(x).flatten()

import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines["left"].set_position("center")
ax.spines["bottom"].set_position("zero")
ax.spines["right"].set_color("none")
ax.spines["top"].set_color("none")
ax.xaxis.set_ticks_position("bottom")
ax.yaxis.set_ticks_position("left")

plt.plot(x, y, "r")
plt.plot(x, yh, "b")

plt.show()

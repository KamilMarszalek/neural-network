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

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# ToDo tu prosze podac pierwsze cyfry numerow indeksow
p = [1, 8]


L_BOUND = -5
U_BOUND = 5


def q(x):
    return np.sin(x * np.sqrt(p[0] + 1)) + np.cos(x * np.sqrt(p[1] + 1))


np.random.seed(1)


# f logistyczna jako przykład sigmoidalej
def sigmoid(x):
    x = np.exp(-x)
    res = 1 / (1 + x)
    return res


# pochodna fun. 'sigmoid'
def d_sigmoid(x):
    x = np.exp(-x)
    s = 1 / (1 + x)
    s = s * (1 - s)
    return s


FUNCTION = sigmoid
D_FUNCTION = d_sigmoid


# f. straty
def nloss(y_out, y):
    return (y_out - y) ** 2


# pochodna f. straty
def d_nloss(y_out, y):
    return 2 * (y_out - y)


def distribution(shape_in, shape_out):
    limit = 1.0 / np.sqrt(shape_in)
    return np.random.uniform(-limit, limit, size=(shape_in, shape_out))


class DlNet:
    def __init__(self, layer_size, lr):
        self.y_out = 0

        self.HIDDEN_L_SIZE = layer_size
        self.LR = lr

        self.W1 = distribution(1, self.HIDDEN_L_SIZE)
        self.b1 = distribution(1, self.HIDDEN_L_SIZE)
        self.W2 = np.zeros((self.HIDDEN_L_SIZE, 1))
        self.b2 = np.zeros((1, 1))

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
        self.forward(x_set)
        loss_val = self.calc_total_loss_val(y_set, self.y_out)
        return loss_val

    @staticmethod
    def calc_total_loss_val(y, pred_y):
        return np.mean(nloss(pred_y.flatten(), y))


if __name__ == "__main__":
    x = np.linspace(L_BOUND, U_BOUND, 10000)
    y = q(x)

    np.seterr(over="warn")
    np.seterr(under="warn")
    np.seterr(invalid="raise")

    rng = np.random.default_rng()
    train_indices = rng.choice(len(x), 2000, replace=False)
    train_x = x[train_indices]
    train_y = y[train_indices]

    nn = DlNet(15, 0.1)
    loss = nn.train(train_x, train_y, batch_size=100, epochs=5000)

    print(loss)

    yh = nn.predict(x).flatten()

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

    plt.savefig(Path(__file__).parent / "plot.png")

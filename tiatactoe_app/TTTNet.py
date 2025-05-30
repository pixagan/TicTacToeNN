import numpy as np
import pandas as pd

import torch
import torch.nn as nn

# Define the neural network model

import torch.nn as nn



class TicTacToeNet(nn.Module):
    def __init__(self):
        super(TicTacToeNet, self).__init__()
        # self.fc1 = nn.Linear(10, 32)
        # self.fc2 = nn.Linear(32, 64)
        # self.fc3 = nn.Linear(64, 32)
        # self.fc4 = nn.Linear(32, 10)

        self.fc1 = nn.Linear(10, 16)
        self.fc2 = nn.Linear(16, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 10)
        
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
        
        # Dropout layers
        self.dropout1 = nn.Dropout(p=0.2)
        self.dropout2 = nn.Dropout(p=0.3)
        self.dropout3 = nn.Dropout(p=0.3)
        self.dropout4 = nn.Dropout(p=0.2)


    def forward(self, x):
        x = self.relu(self.fc1(x))
        #x = self.dropout1(x)
        
        x = self.relu(self.fc2(x))
        #x = self.dropout2(x)

        x = self.relu(self.fc3(x))
        #x = self.dropout3(x)

        x = self.fc4(x)
        
        #x = self.softmax(self.fc4(x))
        return x



    #---------------------------------------------------

def main():
    net = TicTacToeNet()
    net.load_state_dict(torch.load("TTT_Weights.pth",weights_only=True))

    board_tensor = torch.zeros(10)
    board_tensor[0] = 0
    board_tensor[1] = -1
    board_tensor[2] = -1
    board_tensor[3] = -1
    board_tensor[4] = -1
    board_tensor[5] = -1
    board_tensor[6] = 1
    board_tensor[7] = 1
    board_tensor[8] = -1
    board_tensor[9] = 0
    board_tensor_2d = board_tensor.view(1, 10)
    #0,-1,-1,-1,-1,-1,1,1,-1,0,2

    net.eval()

    output = net(board_tensor_2d)
    print(output)

    _, predicted = torch.max(output.data, 1)

    print("Prediction : ",predicted)

#---------------------------------------------------


if __name__ == "__main__":
    main()
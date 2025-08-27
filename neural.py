import torch.nn as nn

class CyberModel(nn.Module):
	def __init__(self, features):
		super().__init__()

		self.fc1 = nn.Linear(features, 16)
		self.fc2 = nn.Linear(16, 3)

	def forward(self, x):
		x = self.fc1(x)
		x = self.fc2(x)
		return x
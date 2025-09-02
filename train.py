import numpy as np
import torch
import torch.nn as nn
import json_parse
import os
import neural

LEARNING_RATE = 1e-2
TRAINING_LOGS = "training/training_events.json"

def trainModel(model, optimizer, epochs, training_input, training_output):
	for _ in range(epochs):
		optimizer.zero_grad()

		# Step 1: Place all our inputs into our model, and get all our outputs.
		outputs = model.forward(training_input)

		# Step 2: Calculate loss between our outputs and expected outputs
		# MSELoss for mean squared error loss (scalar), 
		# BCELoss() for binary 
		# Cross Entropy Loss for multicategory classifications, output for eval must be torch.long
		loss_fn = nn.CrossEntropyLoss()
		loss = loss_fn(outputs, training_output.to(torch.long))
		loss.backward()

		# Step 3: Update model parameters
		optimizer.step()
	
	# Final Step: Save the model to 
	torch.save(model.state_dict(), 'cybermodel.pt')

if __name__ == "__main__":
	# GET TRAINING DATA
	entries = json_parse.logs_to_data(TRAINING_LOGS)

	logs = []
	labels = []

	for entry in entries:
		logs.append(entry["features"])
		labels.append(entry["label"])

	# INITALIZATION
	device = torch.device("cpu")
	model = neural.CyberModel(len(logs[0])).to(device)
	if os.path.isfile('cybermodel.pt'):
		model.load_state_dict(torch.load('cybermodel.pt', weights_only=True))
	optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

	# DATA -> TENSOR
	X = torch.tensor(logs).to(torch.float32)
	Y = torch.tensor(labels).to(torch.float32)
	
	# GET NUMBER OF EPOCHS
	epochs = str(input("Number of Epochs (Default 1000): "))
	if not epochs.isdigit():
		epochs = 1000
	else:
		epochs = int(epochs)

	# BEGIN TRAINING
	print("Starting Training")
	trainModel(model, optimizer, epochs, X, Y)
	print("Training Complete")

import torch
import os
import neural
import json_parse
import numpy as np
import datetime

EVAL_LOGS = "eve_copy.json"

if __name__ == "__main__":

    # CHECK IF PARAMETERS EXIST
    if not os.path.isfile('cybermodel.pt'):
        print('Model parameters not detected, try running train.py first.')
        print('Exting...')
        exit()

    # GET DATA
    entries = json_parse.logs_to_data(EVAL_LOGS)

    if len(entries) == 0:
        print('No training data found. Check file at log path')
        print('Exiting...')
        exit()

    logs = []
    flow_ids = []

    for entry in entries:
        logs.append(entry["features"])
        flow_ids.append(entry["flow_id"])

    # INITALIZE MODEL
    device = torch.device("cpu")
    model = neural.CyberModel(len(logs[0])).to(device)
    model.eval()

    # WRITE RESULTS TO FILE
    file = open('model_evaluations.txt', 'w')

    # BEGIN EVALUATION
    file.write(str(datetime.datetime.now()))
    file.write("\n")

    with torch.no_grad():
        for i in range(100):
            out = model.forward(torch.tensor(logs[i]).to(torch.float32))

            file.write(f"{logs[i]}\n - Model: {np.argmax(out)}, ID: {flow_ids[i]}")
            file.write("\n")



    
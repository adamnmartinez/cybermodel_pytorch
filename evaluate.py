import torch
import os
import neural
import json_parse
import numpy as np
import datetime

EVAL_LOGS = "training/eve_test.json"

def evaluate(log_path):
    # CHECK IF PARAMETERS EXIST
    if not os.path.isfile('cybermodel.pt'):
        print('Model parameters not detected, try running train.py first.')
        print('Exting...')
        exit()

    # GET DATA
    entries = json_parse.logs_to_data(log_path)

    if len(entries) == 0:
        print('[ EVALUATE: No training data found. Cancelling Evaluation ]')
        return
    
    # INITALIZE MODEL
    device = torch.device("cpu")
    model = neural.CyberModel(len(entries[0]["features"])).to(device)
    model.eval()

    # WRITE RESULTS TO FILE
    file = open('eval/model_evaluations.txt', 'w')
    notify = open('eval/notify.txt', 'a')
    review = open('eval/review.txt', 'a')

    # BEGIN EVALUATION
    file.write(str(datetime.datetime.now()))
    file.write("\n")

    with torch.no_grad():
        for entry in entries:
            out = model.forward(torch.tensor(entry["features"]).to(torch.float32))

            choice = torch.argmax(out).item()

            file.write(f"{entry["traffic"]}\n - Model: {choice}, ID: {entry["flow_id"]}, Features: {entry["features"]}")
            file.write("\n")

            if choice == 2:
                # Log and Notify
                notify.write(entry["traffic"])
                notify.write('\n')

                review.write(entry["traffic"])
                review.write('\n')
            elif choice == 1:
                # Log
                review.write(entry["traffic"])
                review.write('\n')

    file.close()
    notify.close()
    review.close()

if __name__ == "__main__":
    evaluate(EVAL_LOGS)
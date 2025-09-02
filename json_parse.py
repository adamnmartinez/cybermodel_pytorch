import json
import environment
import suricata

TRAINING_LOGS = "training/training_events.json"
PRIVATE_IPS = environment.known_ips
SURICATA_EVENTS = suricata.suricata_event_types

def logs_to_data(log_path):
    file = open(log_path, "r")

    data = []

    for line_number, line in enumerate(file, start=1):
        if not line.startswith("{"):
            continue

        try:
            json_line = json.loads(line)

            # Assign Features
            features = []
        
            # (0) Add Time as HHMM
            features.append(int(json_line["timestamp"].split("T")[1][:5].replace(":", "")))

            # (1) Event Type
            features.append(SURICATA_EVENTS.index(json_line["event_type"]))

            # (2) Is Local Source
            if json_line.get("src_ip", None):
                features.append(1 if json_line["src_ip"] in PRIVATE_IPS else 0)
            else: features.append(1)

            # (3) Is Local Destination
            if json_line.get("dest_ip", None):
                features.append(1 if json_line["dest_ip"] in PRIVATE_IPS else 0)
            else: features.append(1)

            # (4) Source Port Number
            if json_line.get("src_port", None):
                features.append(json_line["src_port"])
            else: features.append(0)

            # (5) Destination Port Number
            if json_line.get("dest_port", None):
                features.append(json_line["dest_port"])
            else: features.append(0)

            # (6) Alert Severity (if present)
            if json_line.get("alert", None) and json_line.get("alert", None).get("severity") is not None:
                features.append(json_line.get("alert", None).get("severity", None))
            else: features.append(0)

            entry = {
                "features": features,
                "flow_id": json_line.get("flow_id", None) if json_line.get("flow_id", None) else 0,
                "traffic": str(json_line),
                "label": json_line.get("label") if json_line.get("label") is not None else -1
            }

            data.append(entry)

        except ValueError:
            print(f"ValueError Exception at line {line_number} (unrecognized event type?)")
        except KeyError as ke:
            print(f"KeyError Exception at line {line_number}")
            print(ke)
        except Exception as e:
            print(f"An unknown error occured at line {line_number}")
            print(e)

    file.close()

    return data

if __name__ == "__main__":
    logs = logs_to_data(TRAINING_LOGS)
    for i in range(len(logs)):
        print(logs[i])
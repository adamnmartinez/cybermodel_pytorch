import time
import os
import shutil
import difflib
import evaluate
import notify

SURICATA_LOGS = "/var/log/suricata/eve.json"
FREQUENCY = 10
NOTIFY_FREQ = 5 # After how many "frequencies" do we notify? (90 * 10 seconds = 900 Seconds = 15 Minutes)
SMTP_PORT = 465
LOG_LENGTH = 100
LOG_CUT = 5

if __name__ == "__main__":
    notify_counter = 0

    while(True):
        print("Evaluating...")

        # Step 1: Copy log file.
        if os.path.isfile(SURICATA_LOGS):
            shutil.copy(SURICATA_LOGS, "run/eve_copy.json")
            print(" - Copied Suricata eve.logs to local directory.")

        # Step 2: Check for differences using cached version
        if os.path.isfile("run/eve_cache.json"):
            print(" - Cache found, running evaluation on new traffic...")
            # Step 2.1 Find diff between cache and copy, the evaluate diff
            f_eval = open("run/evaluate_set.json", "w")

            f_copy = open("run/eve_copy.json", "r")
            f_cache = open("run/eve_cache.json", "r")
            lines_copy = f_copy.readlines()
            lines_cache = f_cache.readlines()

            diff = difflib.ndiff(lines_copy, lines_cache)

            changed = [line[2:] for line in diff if line.startswith('+ ') or line.startswith('- ')]

            for line in changed:
                f_eval.write(line)
                f_eval.write('\n')

            evaluate.evaluate("run/evaluate_set.json")

            shutil.copy("run/eve_copy.json", "run/eve_cache.json")
            os.remove("run/eve_copy.json")

            f_copy.close()
            f_cache.close()
            f_eval.close()
        else:
            # Step 2.2: No Cache Detected, save cache and watch for changes
            print(" - No Cache detected, saving cache and awaiting changes...")
            shutil.copy("run/eve_copy.json", "run/eve_cache.json")
            os.remove("run/eve_copy.json")

        # Step 3: Send Notifications + Clear Notify file
        if notify_counter >= NOTIFY_FREQ:
            print(" - Sending Notification.")
            
            f_notify_list = open("eval/notify.txt")

            notify_lines = f_notify_list.readlines()

            notify.send_email_report(notify_lines)

            f_notify_list.close()

            os.remove("eval/notify.txt")
            
            notify_counter = 0

        # Step 4: Trim Log File to prevent overly-large file
        if os.path.isfile("eval/review.txt"):
            f_output = open("eval/review.txt", 'r+')
            output_lines = f_output.readlines()
           
            while len(output_lines) > LOG_LENGTH:
                f_output.seek(0)
                f_output.truncate(0)
                f_output.writelines(output_lines[LOG_CUT:])

                output_lines = f_output.readlines()
           
        notify_counter += 1
        print("Sleeping...")
        time.sleep(FREQUENCY)
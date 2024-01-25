import sys
from colorama import Fore as color
from time import sleep
import subprocess
import re
import os


bold = '\033[1m'
endbold = '\033[0m'

def banner():
    print(bold+color.RED+'''
        
         # #       #             # # #       
        #   #       #           #  #  #      DNS Zone Transfer
       #     #       #         #   #   #      
      #       #       #       #    #    #    
     #         #       #     #     #     #   
    #           #       #   #      #      #  
   #             #       # #       #       # 

     '''+endbold)

    print(bold+color.WHITE+'''
    
         -----------------------
       ⚒  DNS Zone Transfer  ⚒    
         -----------------------
         
     '''+endbold)  
    sleep(1)

os.system('clear')
banner()

def get_command_output(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def run_dig_commands(DOMAIN):
    command1 = f"dig +short ns {DOMAIN}"
    output1 = get_command_output(command1)

    lines = output1.splitlines()

    if len(lines) >= 2:
        command2 = f"dig axfr {DOMAIN} @{lines[0]}"
        output2 = get_command_output(command2)

        command3 = f"dig axfr {DOMAIN} @{lines[1]}"
        output3 = get_command_output(command3)

        return output2, output3

    return "", ""

DOMAIN = input("Enter Domain: ")

result1, result2 = run_dig_commands(DOMAIN)

def clean_output(output):
    domains = set()
    for line in output.splitlines():
        matches = re.findall(r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', line)
        domains.update(matches)
    return "\n".join(domains)

clean_result1 = clean_output(result1)
clean_result2 = clean_output(result2)

with open("Firs_OutPut", "w") as file:
    file.write("Result:\n")
    file.write(f"{clean_result1};{clean_result2}") 


with open("Firs_OutPut", "r") as file:
    lines = file.readlines()

matched_lines = [line for line in lines if DOMAIN in line]

with open("ZoneTransfer", "w") as file:
    file.writelines(matched_lines)

os.remove("Firs_OutPut")

print("Result Successfully Saved in ZoneTransfer File.")

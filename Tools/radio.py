import requests
import subprocess


radio_list = "http://www.radiofeeds.co.uk/bbcradio4fm.pls"
pls_content = requests.get(radio_list).content
mpc_exec = "/usr/bin/mpc"

for line in pls_content.split():
    line_list = line.split("=")
    if "File1" == line_list[0]:
        line_list.remove("File1")
        radio_url = "=".join(line_list)

subprocess.check_output("{mpc_exec} -q clear && {mpc_exec} -q add {radio_url} && {mpc_exec} volume 80 && {mpc_exec} -q play".format(
    mpc_exec=mpc_exec, radio_url=radio_url), shell=True)
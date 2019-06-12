#!/usr/bin/env python3

# read this to make it work
# https://stackoverflow.com/questions/11003981/printf-ignoring-excess-arguments

# tell me about completion
bashCommand = "printf '\n' | mail -s 'Alo Som Teste' f99f17dc-4b20-472f-958a-aa59f1ed7ca2@notify.moosa.it"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

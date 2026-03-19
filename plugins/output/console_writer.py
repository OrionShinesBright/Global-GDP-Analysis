# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/output/console_writer.py

> Compact terminal output for each verified, processed packet.
> need to write to console is not viable anymore. But writing to console
> JUST in case the browser on the TA's computer just.. gives up or something.
> So we will at least still have something to show for ourselves.
"""

import platform

from core.protocols import FromStream
from typing import List, Dict

###############################################################################
# Console Writer Class
#
# Writes the packet to terminal screen. Colors yayyy
# I checked Stack overflow and it apperas that these colors might go wacky
# on windows terminal. So if you are checking on windows, then your loss.
# I'll apply a check for that, but seriously. Grow up. And check on a UNIX machine.
class ConsoleWriter:

    ###############################################################################
    # I hope this is self-explanatory, cuz if not..
    # May your God help you.
    def __init__(self):
        ...

    ###############################################################################
    # write
    #
    # Prints a compact single-line summary of each processed packet.
    #
    # ARG: data1 (dict), data2 (float average), count (int)
    # RET: None
    def write(self, data1, data2, count) -> None:
        entity    = data1.get('entity_name',  '?')
        period    = data1.get('time_period',  '?')
        value     = data1.get('metric_value', '?')
        hash_tail = str(data1.get('security_hash', '????'))[-4:]

        # give colors to everyone other than windows lol
        # show hashes on windows as well, cuz they have less stuff
        # trynna make it even for them
        if platform.system() == "Windows":
            print(f"#{count:>4}\t for [{entity}]: ({period}, {value}) - short hash: {hash_tail}\t|\tAvg={data2:.4f}")
        else:
            print(f"\033[31m#{count:>4}\t \033[90mfor \033[31m[{entity}]\033[90m: \033[32m({period}, {value}) \t\033[90m|\tAvg=\033[34m{data2:.4f}\033[0m")

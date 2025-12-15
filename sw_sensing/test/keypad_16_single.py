import lcapy
import sympy as sy
import numpy as np

from common import check, get_new_resistances

def generate_circuit():
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add(f"R0 pin5 side_1 r0; right=2")
    cct.add("W side_1 node_1; right=2")
    cct.add(f"R1 node_1 node_2 r1; down")
    cct.add(f"W node_2 out; down")
    cct.add("W side_1 pin2; down=2")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add(f"W node_2 c; right=2")
    cct.add("C c 0 100e-12; down, ground")
    
    return cct

if __name__ == "__main__":
    substitute = lambda resistances, node: {"r0": resistances[0], "r1": sum(resistances[1:node])}
    resistances = [432837, 409632, 449660, 419437, 401071, 378266, 411354, 402799, 392903, 447375, 401663, 403171, 433107, 404175, 396619]
    resistances = [r * 0.23 for r in resistances]
    check([2300e3] + resistances, generate_circuit, substitute)

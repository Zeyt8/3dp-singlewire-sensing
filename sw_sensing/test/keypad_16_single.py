import lcapy
import sympy as sy
import numpy as np

from common import check, get_new_resistances

def generate_circuit(extra_c=False):
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add(f"R0 pin5 side_1 r0; right=2")
    cct.add("W side_1 node_1; right=2")
    cct.add(f"R1 node_1 node_2 r1; down")
    cct.add(f"W node_2 out; down")
    cct.add("W side_1 pin2; down=2")
    if extra_c:
        cct.add("C1 pin2 0 c1; right")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add(f"W node_2 c; right=2")
    cct.add("C0 c 0 c0; down, ground")
    
    return cct
    
base_circuit = lambda : generate_circuit(False)
circuit_with_extra_c = lambda : generate_circuit(True)
substitute = lambda resistances, node: {"r0": resistances[0], "r1": sum(resistances[1:node]), "c0": 100e-12, "c1": 100e-12}

if __name__ == "__main__":
    # simulate initial values
    print("= INITIAL RESISTANCES =\n")
    resistances = [432837, 409632, 449660, 419437, 401071, 378266, 411354, 402799, 392903, 447375, 401663, 403171, 433107, 404175, 396619]
    resistances = [r * 0.23 for r in resistances]
    check([2300e3] + resistances, base_circuit, substitute, True)
    # calculate new values and simulate
    print("\n= IDEAL VALUES =\n")
    maxes = [462147, 409632, 456646, 457509, 401071, 378266, 467924, 402799, 392903, 466741, 401663, 403171, 475801, 404175, 396619]
    maxes = [r * 0.23 for r in maxes]
    r1, resistances = get_new_resistances(maxes, single_wire=True)
    check([r1] + resistances, base_circuit, substitute, True)
    print(f"\nMinimum R1: {int(r1)}")
    print("Optimized resistances:")
    print("[" + ", ".join(f"{int(r)}" for r in resistances) + "]")
    # simulate actual possible values
    print("\n= ACTUAL POSSIBLE VALUES =\n")
    resistances = [106282.45292145321, 98372.21176184688, 23031.50883575576, 95099.33838280731, 74263.14521716886, 67446.37266744737, 61403.812109792234, 55454.954148189776, 50508.54053194302, 46116.1950063792, 38519.75146200466, 36771.50436843857, 34561.500017412174, 45379.90752711366, 23347.750615425386]
    check([r1] + resistances, base_circuit, substitute, True)
    print("\n= WITH EXTRA CAPACITOR =\n")
    check([r1] + resistances, circuit_with_extra_c, substitute, True)

import lcapy
import sympy as sy
import numpy as np

from common import check, get_new_resistances

def generate_circuit():
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add(f"R0 pin5 node_1 r0; right=2")
    cct.add(f"R1 node_1 node_2 r1; down")
    cct.add(f"W node_2 pin2; down")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add(f"W node_1 c; right=2")
    cct.add("C c 0 100e-12; down, ground")
    
    return cct

if __name__ == "__main__":
    substitute = lambda resistances, node: {"r0": sum(resistances[:node]), "r1": sum(resistances[node:])}
    # simulate initial values
    print("= INITIAL RESISTANCES =\n")
    resistances = [462147, 409632, 456646, 457509, 401071, 378266, 467924, 402799, 392903, 466741, 401663, 403171, 475801, 404175, 396619]
    check([100e3] + resistances, generate_circuit, substitute)
    # calculate new values and simulate
    print("\n= IDEAL VALUES =\n")
    maxes = [462147, 409632, 456646, 457509, 401071, 378266, 467924, 402799, 392903, 466741, 401663, 403171, 475801, 404175, 396619]
    r1, resistances = get_new_resistances(maxes)
    check([r1] + resistances, generate_circuit, substitute)
    print(f"\nMaximum R1: {int(r1)}")
    print("Optimized resistances:")
    print("[" + ", ".join(f"{int(r)}" for r in resistances) + "]")
    # simulate actual possible values
    print("\n= ACTUAL POSSIBLE VALUES =\n")
    resistances = [106080.9743290255, 120585.66560991325, 149809.198721259, 142731.79560941426, 153969.8081231417, 176341.42110080222, 181796.5204009313, 204927.1942525951, 231283.02949481242, 256639.82688809067, 265839.75572184625, 303710.1801825228, 332533.3678946336, 374589.41399135167, 396619.32283761894]
    check([100e3] + resistances, generate_circuit, substitute)

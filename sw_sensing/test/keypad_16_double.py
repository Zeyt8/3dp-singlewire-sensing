import lcapy
import sympy as sy
import numpy as np

from common import check, get_new_resistances, compute_epsilons_with_extra_c

def generate_circuit(extra_c=False):
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add("R0 pin5 node_1 r0; right=2")
    cct.add("R1 node_1 node_2 r1; down")
    cct.add("R2 node_2 pin2 r2; down")
    if extra_c:
        cct.add("C1 pin2 0 c1; down, ground")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add("W node_2 c; right")
    cct.add("C0 c 0 c0; down, ground")

    return cct

def generate_circuit2(extra_c=False):
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add("R0 pin5 node_1 r0; right=2")
    cct.add("R1 node_1 node_2 r1; down")
    cct.add("R2 node_2 pin2 r2; down")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add("W node_2 c; right")
    cct.add("C0 c 0 c0; down, ground")
    if extra_c:
        cct.add("C1 c 0 c1; up, ground")

    return cct

base_circuit = generate_circuit2(False)
circuit_with_extra_c = generate_circuit2(True)
substitute = lambda resistances, node: {"r0": resistances[0], "r1": sum(resistances[1:node]), "r2": sum(resistances[node:]), "c0": 100e-12, "c1": 100e-12}
resistances16 = [462147, 409632, 456646, 457509, 401071, 378266, 467924, 402799, 392903, 466741, 401663, 403171, 475801, 404175, 396619]
maxes16 =       [462147, 409632, 456646, 457509, 401071, 378266, 467924, 402799, 392903, 466741, 401663, 403171, 475801, 404175, 396619]
actual16 =      [106080.9743290255, 120585.66560991325, 149809.198721259, 142731.79560941426, 153969.8081231417, 176341.42110080222, 181796.5204009313, 204927.1942525951, 231283.02949481242, 256639.82688809067, 265839.75572184625, 303710.1801825228, 332533.3678946336, 374589.41399135167, 396619.32283761894]
actual4 = [72412.25406348177, 65263.473967994265, 86403.35146608776]
maxes9 = [368397.65229989454, 373406.1824703731, 423310.7839047706, 468623.6337075447, 370989.7391898882, 385092.14214907715, 397326.72298632615, 425089.0027653635]
maxes4 = [367584.24365348386, 408133.8589512185, 354446.0651659377]

if __name__ == "__main__":
    # simulate initial values
    print("= INITIAL RESISTANCES =\n")
    resistances = resistances16
    check([100e3] + resistances, base_circuit, substitute)
    # calculate new values and simulate
    print("\n= IDEAL VALUES =\n")
    maxes = maxes4
    r1, resistances = get_new_resistances(maxes)
    check([r1] + resistances, base_circuit, substitute)
    print(f"\nMaximum R1: {int(r1)}")
    print("Optimized resistances:")
    print("[" + ", ".join(f"{int(r)}" for r in resistances) + "]")
    # simulate actual possible values
    print("\n= ACTUAL POSSIBLE VALUES =\n")
    resistances = actual16
    threshold = check([r1] + resistances, base_circuit, substitute)
    #accuraccy_test(threshold, [r1] + resistances, base_circuit, substitute)
    print("\n= WITH EXTRA CAPACITOR =\n")
    threshold, epsilons = check([r1] + resistances, circuit_with_extra_c, substitute)
    print("\n= ACCURACCY CHECK =\n")
    compute_epsilons_with_extra_c(threshold, epsilons, [r1] + resistances, circuit_with_extra_c, substitute, single_wire=False)
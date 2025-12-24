import lcapy

def generate_circuit_double(extra_c=False):
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add("R0 pin5 node_1 r0; right=2")
    cct.add("R1 node_1 node_2 r_till_p; down")
    cct.add("R2 node_2 pin2 r_after_p; down=1.1")
    if extra_c:
        cct.add("C1 pin2 0 c1; down, ground")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add("W node_2 c; right")
    cct.add("C0 c 0 c0; down, ground")
    
    return cct

def generate_circuit_single(extra_c=False):
    cct = lcapy.Circuit()
    cct.add("V pin5 0 step 5.0; down=1, ground")
    cct.add(f"R0 pin5 side_1 r0; right=2")
    cct.add("W side_1 node_1; right")
    cct.add(f"R1 node_1 node_2 r_till_p; down")
    cct.add(f"W node_2 out; down, ground")
    cct.add("W side_1 pin2; down=2")
    if extra_c:
        cct.add("C1 pin2 0 c1; down, ground")
    cct.add("Rx pin2 0 100e6; left=2, ground")

    cct.add(f"W node_2 c; right")
    cct.add("C0 c 0 c0; down, ground")
    
    return cct

def generate_circ_glove():
    cct = lcapy.Circuit()
    cct.add("W node_2 c; right")
    cct.add("C0 c 0 c0; down, ground")
    cct.add("W c c2; right")
    cct.add("C1 c2 0 c1; down, ground")
    
    return cct

if __name__ == "__main__":
    generate_circuit_double(False).draw('lcapy_circuit_double.png')
    generate_circuit_single(False).draw('lcapy_circuit_single.png')
    generate_circuit_double(True).draw('lcapy_circuit_double_cap.png')
    generate_circuit_single(True).draw('lcapy_circuit_single_cap.png')
    generate_circ_glove().draw('lcapy_capacitor_at_sensor.png')
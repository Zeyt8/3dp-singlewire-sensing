import sympy as sy
import numpy as np

def get_new_resistances(max_resistances):
    index = 0
    min_over_max = len(max_resistances)
    for i in range(0, len(max_resistances)):
        new_resistances = [max_resistances[i] * (1.1 ** (j - i)) for j in range(len(max_resistances))]
        over_maxes = sum((new_resistances[j] - max_resistances[j]) / max_resistances[j] for j in range(len(new_resistances)) if new_resistances[j] > max_resistances[j])
        #print(f"Pivot at index {i}: {over_maxes} over max")
        if over_maxes < min_over_max:
            min_over_max = over_maxes
            index = i
    return [max_resistances[index] * (1.1 ** (j - index)) for j in range(len(max_resistances))]

def substitute_symbols(f, symbol_val_dict):
    substitutes = []
    for symbol in f.free_symbols:
        if symbol.name in symbol_val_dict:
            substitutes.append((symbol, symbol_val_dict[symbol.name]))
    return f.subs(substitutes)

def check(resistances, generate_circuit, substitute):
    times = []
    smallest_epsilon = float('inf')
    for node in range(1, len(resistances) + 1):
        cct = generate_circuit()
        transfer = sy.simplify(cct.pin2.V.transient_response().sympy)

        eq = substitute_symbols(
            sy.Eq(transfer, 2.5), substitute(resistances, node)
        )
        for symbol in transfer.free_symbols:
            if symbol.name == "t":
                tsymbol = symbol
                break

        ans = sy.solveset(eq, tsymbol, domain=sy.core.S.Reals)
        t_thres = ans.args[0] if len(ans.args) > 0 else np.nan

        eps_lower_bound = (-100 * resistances[node-1]) / (2 * sum(resistances[:node]))
        if node == len(resistances):
            eps_upper_bound = (100 * 100e6) / (2 * sum(resistances[:node]))
        else:
            eps_upper_bound = (100 * resistances[node]) / (2 * sum(resistances[:node]))
        eps_range = abs(eps_upper_bound - eps_lower_bound)
        print(f"Node: {node}, Threshold time: {t_thres * 1e6:.4f} us (+{t_thres * 1e6 - times[-1] if times else 0:.4f} us), Epsilon range: {eps_range:.2f} e-12")
        smallest_epsilon = min(smallest_epsilon, eps_range)
        times.append(t_thres * 1e6)

    smallest_gap = float('inf')
    for i in range(1, len(times)):
        gap = times[i] - times[i - 1]
        if gap < smallest_gap:
            smallest_gap = gap
    print(f"Smallest gap between thresholds: {smallest_gap:.4f} us")
    print(f"Smallest epsilon range: {smallest_epsilon}")
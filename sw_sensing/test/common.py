import sympy as sy
import numpy as np

def get_new_resistances(max_resistances: list[float], alpha: int=1.1, single_wire: bool=False) -> tuple[float, list[float]]:
    index = 0
    min_over_max = len(max_resistances)
    for i in range(0, len(max_resistances)):
        if single_wire:
            new_resistances = [max_resistances[i] * (alpha ** (i - j)) for j in range(len(max_resistances))]
        else:
            new_resistances = [max_resistances[i] * (alpha ** (j - i)) for j in range(len(max_resistances))]
        over_maxes = sum((new_resistances[j] - max_resistances[j]) / max_resistances[j] for j in range(len(new_resistances)) if new_resistances[j] > max_resistances[j])
        #print(f"Pivot at index {i}: {over_maxes} over max")
        if over_maxes < min_over_max:
            min_over_max = over_maxes
            index = i
    if single_wire:
        new_resistances = [max_resistances[index] * (alpha ** (index - j)) for j in range(len(max_resistances))]
        r1 = 1.01 * sum(new_resistances)
    else:
        new_resistances = [max_resistances[index] * (alpha ** (j - index)) for j in range(len(max_resistances))]
        r1 = 0.99 * new_resistances[0]
    return r1, new_resistances
    

def substitute_symbols(f, symbol_val_dict) -> None:
    substitutes = []
    for symbol in f.free_symbols:
        if symbol.name in symbol_val_dict:
            substitutes.append((symbol, symbol_val_dict[symbol.name]))
    return f.subs(substitutes)

def get_epsilon_bounds(node: int, r: list[float], single_wire: bool) -> tuple[float, float]:
    # l_p = ln(2*r1/r_tillp)
    def l(p):
        return np.log(2 * r[0] / sum(r[:p]))
    
    if single_wire:
        eps_lower_bound = -(100 / 2) * (1 - (sum(r[:node+1]) * l(node+1)) / (sum(r[:node]) * l(node)))
        if node == 1:
            eps_upper_bound = np.nan
        else:
            eps_upper_bound = (100 / 2) * ((sum(r[:node-1]) * l(node-1)) / (sum(r[:node]) * l(node)) - 1)
    else:
        eps_lower_bound = -(100 / 2) * (r[node-1] / sum(r[:node]))
        if node == len(r):
            eps_upper_bound = np.nan
        else:
            eps_upper_bound = (100 / 2) * (r[node] / sum(r[:node]))

    return eps_lower_bound, eps_upper_bound

def check(resistances: list[float], generate_circuit, substitute: dict[str, float], single_wire: bool=False) -> None:
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

        eps_lower_bound, eps_upper_bound = get_epsilon_bounds(node, resistances, single_wire)
        eps_range = abs(eps_upper_bound - eps_lower_bound)
        print(f"Node: {node}, Threshold time: {t_thres * 1e6:.4f} us (+{t_thres * 1e6 - times[-1] if times else 0:.4f} us), Epsilon range: {eps_range:.2f} e-12")
        smallest_epsilon = min(smallest_epsilon, eps_range)
        times.append(t_thres * 1e6)

    smallest_gap = float('inf')
    for i in range(1, len(times)):
        gap = times[i] - times[i - 1]
        if gap < smallest_gap:
            smallest_gap = gap
    print(f"\nSmallest gap between thresholds: {smallest_gap:.4f} us")
    print(f"Smallest epsilon range: {smallest_epsilon}")
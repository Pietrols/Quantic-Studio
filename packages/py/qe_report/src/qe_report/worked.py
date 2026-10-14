"""Governing equations and worked calculations for study reports (decision D11).

Every worked line states the equation, the values substituted into it and the
result, so a reviewer can redo the arithmetic by hand. The numbers come from the
result's trace, which the adapter has already checked against the engine; this
module only formats them. Notation is ASCII so the PDF fonts can render it.
"""
from __future__ import annotations

import math

KASIKCI = "Kasikci, Short Circuits in Power Systems, 1st ed (Wiley-VCH, 2002)"
FITZGERALD = "Fitzgerald, Kingsley and Umans, Electric Machinery, 6th ed (McGraw-Hill, 2003)"
GLOVER = "Glover, Overbye and Sarma, Power System Analysis and Design, 6th ed (Cengage, 2017)"


def g(value: float, digits: int = 6) -> str:
    """Significant-figure formatting used in every substituted value."""
    return f"{value:.{digits}g}"


def shortcircuit_method() -> list[str]:
    return [
        "## Method", "",
        "The equivalent voltage source c Un / sqrt(3) acts at the fault bus; all other sources are "
        "replaced by their internal impedances. Impedances are in ohms, voltages in kV and currents in kA.", "",
        f"- Voltage factor c: maximum and minimum values by voltage level ({KASIKCI}, Table 1.1, p. 8; "
        "low-voltage c_min = 0.95 for both tolerance classes, decision D10).",
        f"- External grid: Z_Q = c U_nQ^2 / S''_kQ, R_Q = Z_Q (R/X) / sqrt(1 + (R/X)^2), "
        f"X_Q = Z_Q / sqrt(1 + (R/X)^2) ({KASIKCI}, eq. 8.1, p. 48).",
        "- Line: Z_L = (r' + j x') l, with R multiplied by the conductor temperature factor in the minimum case.",
        f"- Transformer, on its LV side: Z_T = K_T (r + j x) U_rLV^2 / S_rT, with "
        f"K_T = 0.95 c_max / (1 + 0.6 x_T) in the maximum case ({KASIKCI}, eq. 9.14, p. 79).",
        f"- Generator: Z_GK = K_G (R_G + j x''_d U_rG^2 / S_rG), "
        f"K_G = (U_n / U_rG) c_max / (1 + x''_d sin phi_rG) ({KASIKCI}, eq. 9.3, p. 76).",
        f"- Referral across a transformer by its rated ratio: Z_B = Z_A (U_rB / U_rA)^2 ({KASIKCI}, eq. 8.2, p. 48).",
        f"- Radial network: Z_k = sum of the referred element impedances; Ik'' = c Un / (sqrt(3) |Z_k|) "
        f"({KASIKCI}, section 11.2, p. 92).",
        f"- Peak current: kappa = 1.02 + 0.98 exp(-3 R/X), ip = kappa sqrt(2) Ik'' ({KASIKCI}, eqs. 11.22 "
        "and 11.23, p. 98).",
        f"- Thermal current: Ith = Ik'' sqrt(m + n), m = [exp(4 f Tk ln(kappa - 1)) - 1] / "
        f"(2 f Tk ln(kappa - 1)), n = 1 far from generators ({KASIKCI}, eqs. 13.1 and 13.2, p. 117).",
        "- Every hand-summed Z_k is checked against the solver's own network reduction to a relative "
        "1e-9 before any current is reported; a disagreement makes the value unavailable.",
        "",
    ]


def _element_equation(element: dict) -> str:
    i = element["inputs"]
    kind = element["element_type"]
    if kind == "external_grids":
        z = i["c"] * i["un_kv"] ** 2 / i["s_sc_mva"]
        return (f"Z_Q = c U_nQ^2 / S''_kQ = {g(i['c'])} * {g(i['un_kv'])}^2 / {g(i['s_sc_mva'])} "
                f"= {g(z)} ohm, R/X = {g(i['rx'])}")
    if kind == "lines":
        text = (f"Z_L = (r' + j x') l = ({g(i['r_ohm_per_km'])} + j{g(i['x_ohm_per_km'])}) ohm/km "
                f"* {g(i['length_km'])} km")
        if i["temperature_factor"] != 1:
            text += f", R * {g(i['temperature_factor'])} for conductor temperature"
        return text
    if kind == "transformers":
        text = (f"Z_T = K_T (r + j x) U_rLV^2 / S_rT = {g(i['k_t'])} * ({g(i['r_pu'])} + j{g(i['x_pu'])}) "
                f"* {g(i['vn_lv_kv'])}^2 / {g(i['sn_mva'])}")
        if i["k_t"] != 1:
            text += (f"; K_T = 0.95 c_max / (1 + 0.6 x_T) = 0.95 * {g(i['c_max_lv'])} / "
                     f"(1 + 0.6 * {g(i['x_pu'])}) = {g(i['k_t'])}")
        return text
    sin_phi = math.sqrt(max(0.0, 1 - i["cos_phi"] ** 2))
    return (f"Z_GK = K_G (R_G + j x''_d U_rG^2 / S_rG) = {g(i['k_g'])} * ({g(i['rdss_ohm'])} + j"
            f"{g(i['xdss_pu'])} * {g(i['vn_kv'])}^2 / {g(i['sn_mva'])}); K_G = (U_n / U_rG) c_max / "
            f"(1 + x''_d sin phi_rG) = ({g(i['un_kv'])} / {g(i['vn_kv'])}) * {g(i['c_max'])} / "
            f"(1 + {g(i['xdss_pu'])} * {g(sin_phi)}) = {g(i['k_g'])}")


def shortcircuit_worked(row: dict, case: str, frequency_hz: float, duration_s: float, table) -> list[str]:
    """One bus, one case: element impedances, Z_k, then each current with its numbers."""
    t = row["trace"]
    label = "maximum" if case == "max" else "minimum"
    out = [f"### Worked calculation: bus {row['bus_id']}, {label} case", ""]
    if t["impedance_basis"] == "radial-sum":
        out += table(["Element", "Equation with inputs", "R (ohm)", "X (ohm)", "Referral factor",
                      "R at bus (ohm)", "X at bus (ohm)"],
                     [[f"{e['element_type'][:-1].replace('_', ' ')}: {e['element_id']}", _element_equation(e),
                       g(e["r_ohm"]), g(e["x_ohm"]), g(e["referral_factor"]),
                       g(e["r_referred_ohm"]), g(e["x_referred_ohm"])] for e in t["elements"]])
        out += ["", f"- Z_k = sum of the referred impedances = {g(t['zk_r_ohm'])} + j{g(t['zk_x_ohm'])} ohm."]
    else:
        out += [f"- Z_k from the solver's network reduction (meshed or multi-source component) = "
                f"{g(t['zk_r_ohm'])} + j{g(t['zk_x_ohm'])} ohm."]
    out += [f"- |Z_k| = sqrt({g(t['zk_r_ohm'])}^2 + {g(t['zk_x_ohm'])}^2) = {g(t['zk_ohm'])} ohm.",
            f"- Ik'' = c Un / (sqrt(3) |Z_k|) = {g(t['voltage_factor'])} * {g(t['un_kv'])} / "
            f"(sqrt(3) * {g(t['zk_ohm'])}) = {g(row['ikss_ka'])} kA."]
    if t["kappa"] is not None and row["ip_ka"] is not None:
        out += [f"- R/X = {g(t['zk_r_ohm'])} / {g(t['zk_x_ohm'])} = {g(t['rx_ratio'])}; "
                f"kappa = 1.02 + 0.98 exp(-3 * {g(t['rx_ratio'])}) = {g(t['kappa'])}.",
                f"- ip = kappa sqrt(2) Ik'' = {g(t['kappa'])} * sqrt(2) * {g(row['ikss_ka'])} = {g(row['ip_ka'])} kA."]
    if t["m"] is not None and row["ith_ka"] is not None:
        ln = math.log(t["kappa"] - 1) if t["kappa"] < 2 else 0.0
        if t["kappa"] < 2:
            out.append(f"- m = [exp(4 * {g(frequency_hz)} * {g(duration_s)} * ln({g(t['kappa'])} - 1)) - 1] / "
                       f"(2 * {g(frequency_hz)} * {g(duration_s)} * ln({g(t['kappa'])} - 1)), with "
                       f"ln(kappa - 1) = {g(ln)}, so m = {g(t['m'])}; n = {g(t['n'])}.")
        else:
            out.append(f"- kappa = 2, so m takes its limit 2; n = {g(t['n'])}.")
        out.append(f"- Ith = Ik'' sqrt(m + n) = {g(row['ikss_ka'])} * sqrt({g(t['m'])} + {g(t['n'])}) = "
                   f"{g(row['ith_ka'])} kA.")
    out.append("")
    return out


def motorstart_worked(motor: dict, trace: dict | None, rows: list[dict]) -> list[str]:
    out = ["## Method and worked calculation", "",
           f"The motor is modelled at standstill (slip s = 1) by its blocked-rotor input impedance "
           f"({FITZGERALD}, section 6.6.2, pp. 333 to 334), connected as a constant-impedance shunt; the "
           "network is solved by load flow before and after it is connected.", "",
           "- Rated current: I_r = P_shaft / (sqrt(3) U_r eta cos phi_r).",
           "- Locked-rotor current: I_LR = k_LR I_r.",
           "- Impedance: |Z_LR| = U_r / (sqrt(3) I_LR), angle phi_LR = acos(cos phi_LR), "
           "R_LR = |Z_LR| cos phi_LR, X_LR = |Z_LR| sin phi_LR.",
           "- Equivalent shunt at the bus nominal voltage: S = U_bus^2 / conj(Z_LR) = P + jQ; its power "
           "scales with |V|^2 in the locked-rotor load flow.",
           "- Dip (%) = 100 (V_pre - V_LR) / V_pre.", ""]
    if trace is None:
        return out + ["Worked values are unavailable because the calculation did not complete; see diagnostics.", ""]
    m = motor
    out += [
        f"- I_r = {g(m['shaft_rated_kw'])} kW / (sqrt(3) * {g(m['rated_voltage_kv'])} kV * {g(m['efficiency'])} * "
        f"{g(m['rated_power_factor'])}) = {g(trace['rated_current_ka'] * 1000)} A.",
        f"- I_LR = {g(m['locked_rotor_current_ratio'])} * {g(trace['rated_current_ka'] * 1000)} A = "
        f"{g(trace['locked_rotor_current_ka'] * 1000)} A.",
        f"- |Z_LR| = {g(m['rated_voltage_kv'] * 1000)} V / (sqrt(3) * {g(trace['locked_rotor_current_ka'] * 1000)} A) "
        f"= {g(trace['z_lr_ohm'])} ohm; phi_LR = acos({g(m['locked_rotor_power_factor'])}) = "
        f"{g(trace['locked_rotor_angle_deg'])} deg.",
        f"- R_LR = {g(trace['z_lr_ohm'])} * {g(m['locked_rotor_power_factor'])} = {g(trace['r_lr_ohm'])} ohm; "
        f"X_LR = {g(trace['z_lr_ohm'])} * sin({g(trace['locked_rotor_angle_deg'])} deg) = {g(trace['x_lr_ohm'])} ohm.",
        f"- S = {g(trace['bus_kv'])}^2 / ({g(trace['r_lr_ohm'])} - j{g(trace['x_lr_ohm'])}) = "
        f"{g(trace['shunt_p_mw'])} + j{g(trace['shunt_q_mvar'])} MVA.", ""]
    for row in rows:
        if row["dip_percent"] is not None:
            out.append(f"- Bus {row['bus_id']}: dip = 100 * ({g(row['prestart_vm_pu'], 8)} - "
                       f"{g(row['locked_rotor_vm_pu'], 8)}) / {g(row['prestart_vm_pu'], 8)} = "
                       f"{g(row['dip_percent'])} %.")
    out.append("")
    return out


def loadflow_method(solver_name: str) -> list[str]:
    limits = ("The pandapower solver enforces generator reactive limits: a PV bus whose required Q leaves its "
              "range becomes a PQ bus with Q fixed at the limit, and its voltage is then solved "
              f"({GLOVER}, section 6.6, p. 356)." if solver_name == "pandapower" else
              "This solver does not enforce generator reactive limits; section 4 checks them instead.")
    return [
        "## 10. Method", "",
        f"Balanced positive-sequence Newton-Raphson power flow ({GLOVER}, sections 6.4 and 6.6).", "",
        "- Bus admittance matrix Y_bus from line pi models (series z = r + jx, half the charging at each end) "
        f"and transformer series impedances ({GLOVER}, eq. 6.4.2, p. 346).",
        "- Power balance at bus k, with Y_kn = |Y_kn| at angle theta_kn: P_k = V_k sum_n |Y_kn| V_n "
        "cos(delta_k - delta_n - theta_kn) and Q_k = V_k sum_n |Y_kn| V_n sin(delta_k - delta_n - theta_kn) "
        f"({GLOVER}, eqs. 6.6.2 and 6.6.3, p. 354).",
        "- Unknowns: delta at every non-slack bus and V at every PQ bus. Each iteration solves "
        "J dx = [P_spec - P(x); Q_spec - Q(x)] for the correction dx, with the Jacobian J of partial "
        f"derivatives ({GLOVER}, eqs. 6.6.4 to 6.6.7, pp. 354 to 356).",
        "- Converged when the largest power mismatch is below the tolerance in section 7.",
        "- Branch flow: S_ij = V_i conj(I_ij); series loss = S_ij + S_ji.",
        "- Loading: 100 max(|I_from| / I_rated,from, |I_to| / I_rated,to), with I_rated = S_r / (sqrt(3) U_r) "
        "for transformers and the stated maximum current for lines.",
        f"- {limits}",
        "- Section 11 closes the power balance at every bus from the reported flows, so the solution can "
        "be checked by hand.", "",
    ]


def loadflow_balance(network: dict, result: dict, table) -> list[str]:
    """Kirchhoff's current law at each bus from the reported branch flows."""
    ends = {line["line_id"]: (line["from_bus"], line["to_bus"]) for line in network["lines"]}
    ends.update({t["transformer_id"]: (t["hv_bus"], t["lv_bus"]) for t in network["transformers"]})
    vm = {b["bus_id"]: b["vm_pu"] for b in result["bus_results"]}
    flows = {b: [0.0, 0.0] for b in vm}
    for branch in result["branch_results"]:
        if branch["branch_id"] in ends and all(end in vm for end in ends[branch["branch_id"]]):
            a, b = ends[branch["branch_id"]]
            flows[a][0] += branch["p_from_mw"]
            flows[a][1] += branch["q_from_mvar"]
            flows[b][0] += branch["p_to_mw"]
            flows[b][1] += branch["q_to_mvar"]
    demand = {b: [0.0, 0.0] for b in vm}
    for load in network["loads"]:
        if load["bus_id"] in demand:
            demand[load["bus_id"]][0] += load["p_mw"]
            demand[load["bus_id"]][1] += load["q_mvar"]
    for shunt in network["shunts"]:
        if shunt["bus_id"] not in demand:
            continue
        v2 = vm[shunt["bus_id"]] ** 2
        demand[shunt["bus_id"]][0] += shunt["p_mw"] * v2
        demand[shunt["bus_id"]][1] += shunt["q_mvar"] * v2
    grids = {g_["bus_id"] for g_ in network["external_grids"]}
    gens: dict[str, float] = {}
    for gen in network["generators"]:
        gens[gen["bus_id"]] = gens.get(gen["bus_id"], 0.0) + gen["p_mw"]
    rows = []
    for bus in vm:
        p = flows[bus][0] + demand[bus][0]
        q = flows[bus][1] + demand[bus][1]
        if bus in grids:
            rows.append([bus, g(p), g(q), "grid supplies the balance", "n/a", "n/a"])
        elif bus in gens:
            rows.append([bus, g(p), g(q), f"generator P = {g(gens[bus])} MW, Q free",
                         f"{p - gens[bus]:.3e}", "n/a"])
        else:
            rows.append([bus, g(p), g(q), "none", f"{p:.3e}", f"{q:.3e}"])
    return ["## 11. Power balance check", "",
            "At every bus, the power leaving through branches plus load plus shunt (scaled by V^2) must equal "
            "what sources inject: Sum S_branch + S_load + S_shunt V^2 = S_source. At buses without a source, "
            "both residuals must be close to zero.", "",
            *table(["Bus", "Sum P out + demand (MW)", "Sum Q out + demand (Mvar)", "Source", "P residual (MW)",
                    "Q residual (Mvar)"], rows), ""]

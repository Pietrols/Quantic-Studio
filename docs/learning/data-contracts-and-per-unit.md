# Data contracts and the per-unit system

This note explains how Quantic Studio describes engineering data in JSON and why power engineers often use per-unit quantities. The examples are for learning and arithmetic illustration only. They are not equipment ratings, design guidance, or published reference cases.

## What is a data contract?

A data contract is an agreed description of the shape and meaning of data passed between parts of a system. In this platform, a project file can pass through a loader, a study adapter, a report generator, and later a TypeScript interface. Each part needs to agree about the names, units, required properties, and allowed values.

JSON Schema describes that agreement independently of a programming language. A schema can say that a bus has a string identifier, a positive nominal voltage named `vn_kv`, and a bus type chosen from `slack`, `pv`, or `pq`. The same schema can validate a JSON file before it reaches Python or TypeScript. The Markdown specification beside the schema explains intent and includes a concrete example.

Schema validation checks the structure of an object. It cannot by itself confirm every relationship in a network. For example, checking that `from_bus` is a string does not prove that it names a bus in the network. The project loader must resolve references, check identifier uniqueness, and return diagnostics that identify the element and field when a relationship is invalid.

Units are part of the contract. Names such as `vn_kv`, `p_mw`, `q_mvar`, `length_km`, and `r_ohm_per_km` tell a reader which unit applies without guessing. The suffix does not perform a conversion. A producer must put a value in that unit, and a consumer must interpret it accordingly.

## Why use per-unit values?

Per-unit expresses an electrical quantity as a ratio to a chosen base quantity:

$$
q_{pu} = \frac{q_{actual}}{q_{base}}
$$

The ratio is dimensionless. Choosing shared bases lets quantities on different voltage levels be compared cleanly, and transformer impedance values are easier to transfer between sides when voltage bases follow the transformer turns ratio. Per-unit values also keep many power-system calculations near a manageable numerical scale. The actual engineering values remain necessary for reports, protection settings, and equipment checks.

A study must state or inherit its bases. A per-unit value without its base is incomplete data. The network contract therefore names the system power base `base_mva`; bus `vn_kv` values define the nominal voltage bases at each bus. The base voltage is line-to-line RMS in the three-phase formulas below.

## Three-phase base relationships

For a balanced three-phase system, choose three-phase apparent power base $S_{base}$ and line-to-line RMS voltage base $V_{LL,base}$. The corresponding current and impedance bases are:

$$
I_{base} = \frac{S_{base}}{\sqrt{3} V_{LL,base}}
$$

$$
Z_{base} = \frac{V_{LL,base}^2}{S_{base}}
$$

With power in MVA and voltage in kV, these formulas directly yield current in kA and impedance in ohms. The relationship follows from $S = \sqrt{3} V_{LL} I$ and $Z = V_{LL}^2/S_{3\phi}$ with consistent three-phase base definitions.

Then:

$$
V_{pu} = \frac{V_{LL}}{V_{LL,base}}, \qquad
I_{pu} = \frac{I}{I_{base}}, \qquad
Z_{pu} = \frac{Z}{Z_{base}}, \qquad
S_{pu} = \frac{S}{S_{base}}
$$

## Worked conversion

Use an illustrative system base of $S_{base}=100\,\mathrm{MVA}$ and a bus line-to-line base of $V_{LL,base}=11\,\mathrm{kV}$. These values are chosen only to make the arithmetic clear.

First calculate the base impedance:

$$
Z_{base} = \frac{(11\,\mathrm{kV})^2}{100\,\mathrm{MVA}}
= \frac{121}{100}\,\Omega
= 1.21\,\Omega
$$

Suppose an illustrative line has resistance $0.242\,\Omega/\mathrm{km}$ and length $2\,\mathrm{km}$. Its total resistance is:

$$
R = 0.242\,\frac{\Omega}{\mathrm{km}} \times 2\,\mathrm{km}
= 0.484\,\Omega
$$

Convert the total resistance to per-unit on the selected base:

$$
R_{pu} = \frac{0.484\,\Omega}{1.21\,\Omega} = 0.4\,pu
$$

The corresponding current base is:

$$
I_{base} = \frac{100\,\mathrm{MVA}}{\sqrt{3} \times 11\,\mathrm{kV}}
\approx 5.25\,\mathrm{kA}
$$

The contract stores line resistance as `r_ohm_per_km` together with `length_km`, rather than storing this derived per-unit value. A solver can derive the total impedance and then convert it using the bases associated with the connected buses.

## Changing a per-unit impedance base

For the same physical impedance, changing from an old power and voltage base to a new base gives:

$$
Z_{pu,new} = Z_{pu,old}
\left(\frac{S_{base,new}}{S_{base,old}}\right)
\left(\frac{V_{base,old}}{V_{base,new}}\right)^2
$$

When the voltage base is unchanged, only the ratio of power bases remains. Across an ideal transformer, if the voltage bases are chosen in the transformer turns ratio, the voltage-base ratio cancels the physical voltage change. A transformer impedance reported in per unit on its own rated MVA and nominal voltage base must be converted when the network uses a different system base.

## Reading the contracts

- `base_mva` is a positive system apparent-power base in MVA.
- `vn_kv` is a positive bus nominal line-to-line voltage base in kV.
- `vm_pu` is a voltage magnitude ratio to the bus base.
- `va_degree` is a voltage angle in degrees.
- `r_ohm_per_km` and `x_ohm_per_km` are line series impedance per unit length.
- `r_pu` and `x_pu` on a transformer are referenced to that transformer's `sn_mva` and nominal voltage bases.

These names prevent silent unit ambiguity, while the schema and loader provide separate structural and relationship checks.

# ecocalc
[![Build Status](https://github.com/johndoe31415/ecocalc/actions/workflows/CI.yml/badge.svg)](https://github.com/johndoe31415/ecocalc/actions/workflows/CI.yml)

This is a command-line based calculator that I had written in 2017 and
re-written in 2020. Its intention is that you can specify a target product in
your game economy after having specified specific recipes (e.g., for crafting)
and it will show you exactly how many of which part you need to perform that.

Typical games this works for is
[Skyrim](https://store.steampowered.com/agecheck/app/489830/),
[Factorio](https://store.steampowered.com/app/427520/Factorio/),
[Satisfactory](https://store.steampowered.com/app/526870/Satisfactory/),
[Dyson Sphere Program](https://store.steampowered.com/app/1366540/Dyson_Sphere_Program/).
All of which are fantastic games, by the way.

It can also calculate rate-based, e.g., if you want the exact amount of
smelters that is needed to smelt iron ore of a specific mine (and of course
much more complicated things). 

Another feature that the original calculator had (that is still missing in the
rewrite) is to identify profitable loops in the economy. E.g., buy product X
and Y for €100, craft product Z, sell Z for €200.

## Usage
Let's say you want to produce 100 Conveyor Belts MK.II in Dyson Sphere Program.
After definition of the economy (which I have already done for you in
'dyson_sphere_program.json'), you can enter:

```
$ ./print_recipes -e dyson_sphere_program.json -r  '100 >conveyor_mk2'
1 x {Pseudo-Recipe} [ 100 Conveyor belt MK.II →  Finished ]
========================================================================================================================
    1 x  [ 100 Conveyor belt MK.II →  Finished ]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    300 x {#1: Smelt Iron / Smelter} [ Iron Ore →  Iron Ingot ]
    100 x {#32: Produce Gear / Assembler} [ Iron Ingot →  Gear ]
    34 x {#44: Produce Conveyor MK1 / Assembler} [ Gear + 2 Iron Ingot →  3 Conveyor belt MK.I ]
    267 x {#10: Smelt Iron / Smelter} [ Iron Ore →  Magnet ]
    134 x {#2: Smelt Copper / Smelter} [ Copper Ore →  Copper Ingot ]
    134 x {#11: Produce Magnetic Coil / Assembler} [ Copper Ingot + 2 Magnet →  Magnetic Coil ]
    67 x {#22: Produce Electric Motor / Assembler} [ Magnetic Coil + Gear + 2 Iron Ingot →  Electric Motor ]
    34 x {#33: Produce Electromagnetic Turbine / Assembler} [ 2 Electric Motor + 2 Magnetic Coil →  Electromagnetic Turbine ]
    34 x {#45: Produce Conveyor MK2 / Assembler} [ Electromagnetic Turbine + 3 Conveyor belt MK.I →  3 Conveyor belt MK.II ]
    1 x  [ 100 Conveyor belt MK.II →  Finished ]
 ->  133.33 Copper Ore + 566.67 Iron Ore →  Finished
```

You can see that you require 133 copper ore and 566 iron ore as ultimately
irreducible resources to finish that job. Let's assume you already have
infinite gears available and want to consider gears as a basic irreducible
resource as well:

```
$ ./print_recipes -e dyson_sphere_program.json -r '100 >conveyor_mk2' --consider-irreducible gear
1 x {Pseudo-Recipe} [ 100 Conveyor belt MK.II →  Finished ]
========================================================================================================================
    1 x  [ 100 Conveyor belt MK.II →  Finished ]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    200 x {#1: Smelt Iron / Smelter} [ Iron Ore →  Iron Ingot ]
    34 x {#44: Produce Conveyor MK1 / Assembler} [ Gear + 2 Iron Ingot →  3 Conveyor belt MK.I ]
    267 x {#10: Smelt Iron / Smelter} [ Iron Ore →  Magnet ]
    134 x {#2: Smelt Copper / Smelter} [ Copper Ore →  Copper Ingot ]
    134 x {#11: Produce Magnetic Coil / Assembler} [ Copper Ingot + 2 Magnet →  Magnetic Coil ]
    67 x {#22: Produce Electric Motor / Assembler} [ Magnetic Coil + Gear + 2 Iron Ingot →  Electric Motor ]
    34 x {#33: Produce Electromagnetic Turbine / Assembler} [ 2 Electric Motor + 2 Magnetic Coil →  Electromagnetic Turbine ]
    34 x {#45: Produce Conveyor MK2 / Assembler} [ Electromagnetic Turbine + 3 Conveyor belt MK.I →  3 Conveyor belt MK.II ]
    1 x  [ 100 Conveyor belt MK.II →  Finished ]
 ->  100 Gear + 133.33 Copper Ore + 466.67 Iron Ore →  Finished
```

Now let's say you want to do continuous production and are interested in rates
of production instead of absolute values of resources. You want to fill a MK.I
belt (6 items/sec or 36 items/minute) with product:

```
$ ./print_recipes -e dyson_sphere_program.json -r -p '36 >conveyor_mk2'
1 x {Pseudo-Recipe} [ 36/min Conveyor belt MK.II →  Finished ]
========================================================================================================================
    1 x  [ 36/min Conveyor belt MK.II →  Finished ]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    2 x {#1: Smelt Iron / Smelter} [ 60/min Iron Ore →  60/min Iron Ingot ]
    1 x {#24: Produce Gear / Assembler} [ 60/min Iron Ingot →  60/min Gear ]
    1 x {#31: Produce Conveyor MK1 / Assembler} [ 60/min Gear + 120/min Iron Ingot →  180/min Conveyor belt MK.I ]
    3 x {#10: Smelt Iron / Smelter} [ 40/min Iron Ore →  40/min Magnet ]
    1 x {#2: Smelt Copper / Smelter} [ 60/min Copper Ore →  60/min Copper Ingot ]
    1 x {#11: Produce Magnetic Coil / Assembler} [ 60/min Copper Ingot + 120/min Magnet →  60/min Magnetic Coil ]
    1 x {#20: Produce Electric Motor / Assembler} [ 30/min Magnetic Coil + 30/min Gear + 60/min Iron Ingot →  30/min Electric Motor ]
    1 x {#25: Produce Electromagnetic Turbine / Assembler} [ 60/min Electric Motor + 60/min Magnetic Coil →  30/min Electromagnetic Turbine ]
    1 x {#32: Produce Conveyor MK2 / Assembler} [ 60/min Electromagnetic Turbine + 180/min Conveyor belt MK.I →  180/min Conveyor belt MK.II ]
    1 x  [ 36/min Conveyor belt MK.II →  Finished ]
 ->  48/min Copper Ore + 204/min Iron Ore →  Finished
```

## License
GNU GPL-3.

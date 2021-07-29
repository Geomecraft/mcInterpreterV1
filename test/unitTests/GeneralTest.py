from model.General import readFunctionUsage

assert(readFunctionUsage("try()") == ('try', ['']))
assert(readFunctionUsage("namespace.set(mutual_hunt)") == ('namespace.set', ['mutual_hunt']))
assert(readFunctionUsage("Manifest(perk for 1_17 manhunt, 7, by ItsGeomecraft)") == ('Manifest', ['perk for 1_17 manhunt', '7', 'by ItsGeomecraft']))
assert(readFunctionUsage("item.modifier.setNBT(compass_setup, tag, \"<{LodestoneDimension:\"minecraft:overworld\",LodestoneTracked:0b,LodestonePos:{X:1,Y:1,Z:1}}>\")") == ('item.modifier.setNBT', ['compass_setup', 'tag', '{LodestoneDimension:"minecraft:overworld",LodestoneTracked:0b,LodestonePos:{X:1,Y:1,Z:1}}']))
assert(readFunctionUsage("nbt(345, \"<I finally have \"<power!>\">\", \"<I finally have \"<power!>\">\", 543)") == ('nbt', ['345', 'I finally have "<power!>"', 'I finally have "<power!>"', '543']))

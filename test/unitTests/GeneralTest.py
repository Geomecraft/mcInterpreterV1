from model.Parser import parseFunctionUsage

assert(parseFunctionUsage("try()") == ('try', ['']))
assert(parseFunctionUsage("namespace.set(mutual_hunt)") == ('namespace.set', ['mutual_hunt']))
assert(parseFunctionUsage("Manifest(perk for 1_17 manhunt, 7, by ItsGeomecraft)") == ('Manifest', ['perk for 1_17 manhunt', '7', 'by ItsGeomecraft']))
assert(parseFunctionUsage("item.modifier.setNBT(compass_setup, tag, \"<{LodestoneDimension:\"minecraft:overworld\",LodestoneTracked:0b,LodestonePos:{X:1,Y:1,Z:1}}>\")") == ('item.modifier.setNBT', ['compass_setup', 'tag', '{LodestoneDimension:"minecraft:overworld",LodestoneTracked:0b,LodestonePos:{X:1,Y:1,Z:1}}']))
assert(parseFunctionUsage("nbt(345, \"<I finally have \"<power!>\">\", \"<I finally have \"<power!>\">\", 543)") == ('nbt', ['345', 'I finally have "<power!>"', 'I finally have "<power!>"', '543']))

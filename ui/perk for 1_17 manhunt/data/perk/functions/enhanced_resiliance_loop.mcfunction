execute as @a[scores={en_re=1}] run execute at @s run execute if score @s health matches 10.. run effect give @s resistance 3 0 true
execute as @a[scores={en_re=1}] run execute at @s run execute if score @s health matches ..10 run effect give @s resistance 3 1 true
schedule function perk:enhanced_resiliance_loop 1t

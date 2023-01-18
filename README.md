# Basic-RTS
The name inspiration from GitHub is "fluffy-fiesta" and I just love that name, but alas, it is not meant to be.

## Ideas
- Grid based
- Have a main base to protect
- Place spawners that gradually generate entities that move to the enemy base
- Can place walls that can be destroyed
  - Pathfinding may ignore walls but give them a higher weight
  - If pathing goes through walls then entities may destroy them
- Workers that are the building force
  - Spawned from worker spawners when work is queued
- Max number of workers from worker spawners
  - There is no max for entities
- Have trees that can be cut down by workers
  - Gives wood to produce basic buildings
    - Walls
    - Basic spawners
    - mines
- Stone deposits to mine stone from
  - Can be used for better buildings

## Player Interaction:
- All player actions create blueprints
- Blueprints are acted upon by workers
- The starting base has a certain number of workers
- The player needs to designate trees to be destroyed to get wood
- Wood can be used to build a couple of things
  - Wood walls
  - Wood spawners
  - Stone miners
- Each thing requires a minimum amount of free workers and will not start being worked on until this is met
- Workers cannot change tasks once a task has started
  - Includes canceling task for now at least
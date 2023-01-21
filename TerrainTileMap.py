from Environment import GridSquareTerrain
from pygame import Surface

TerrainTileMap = {
    GridSquareTerrain.CLEAR: Surface((16, 16)),
    GridSquareTerrain.HILL: Surface((16, 16)),
    GridSquareTerrain.MOUNTAIN: Surface((16, 16)),
    GridSquareTerrain.SNOW: Surface((16, 16))
}

TerrainTileMap[GridSquareTerrain.CLEAR].fill((70, 110, 45))
TerrainTileMap[GridSquareTerrain.HILL].fill((50, 80, 50))
TerrainTileMap[GridSquareTerrain.MOUNTAIN].fill((50, 55, 70))
TerrainTileMap[GridSquareTerrain.SNOW].fill((255, 255, 255))

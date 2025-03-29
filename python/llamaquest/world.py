"""
World module for LlamaQuest - Handles world generation, loading, and rendering
"""

import json
import os
import pyxel
import random
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum

class TileType(Enum):
    """Types of tiles in the world"""
    EMPTY = 0
    FLOOR = 1
    WALL = 2
    DOOR = 3
    WATER = 4
    GRASS = 5
    PATH = 6
    TREE = 7
    ROCK = 8
    BRIDGE = 9

class World:
    """Represents the game world with tiles, regions, and navigation"""
    
    def __init__(self, width: int = 128, height: int = 128, tile_size: int = 8):
        """Initialize the world grid"""
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.name = "World"
        
        # Create empty tile grid
        self.tiles = [[TileType.EMPTY for _ in range(width)] for _ in range(height)]
        self.tile_properties = {}  # Custom properties for specific tiles
        
        # Sprite mapping for each tile type
        self.tile_sprites = {
            TileType.EMPTY: (0, 0),
            TileType.FLOOR: (0, 8),
            TileType.WALL: (8, 8),
            TileType.DOOR: (16, 8),
            TileType.WATER: (0, 16),
            TileType.GRASS: (8, 16),
            TileType.PATH: (16, 16),
            TileType.TREE: (0, 24),
            TileType.ROCK: (8, 24),
            TileType.BRIDGE: (16, 24)
        }
        
        # List of regions in the world
        self.regions = {}
        
        # Camera position (for scrolling)
        self.camera_x = 0
        self.camera_y = 0
        
        # Walkability rules
        self.walkable_tiles = {
            TileType.FLOOR,
            TileType.GRASS,
            TileType.PATH,
            TileType.BRIDGE
        }
        
        # Special tile positions
        self.interactable_positions = set()  # Set of (x, y) tuples
    
    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if position is within world bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_tile(self, x: int, y: int) -> TileType:
        """Get the tile type at a position"""
        if not self.is_within_bounds(x, y):
            return TileType.EMPTY
        return self.tiles[y][x]
    
    def set_tile(self, x: int, y: int, tile_type: TileType):
        """Set the tile type at a position"""
        if self.is_within_bounds(x, y):
            self.tiles[y][x] = tile_type
    
    def get_tile_properties(self, x: int, y: int) -> Dict:
        """Get properties for the tile at a position"""
        pos = (x, y)
        return self.tile_properties.get(pos, {})
    
    def set_tile_properties(self, x: int, y: int, properties: Dict):
        """Set properties for the tile at a position"""
        pos = (x, y)
        self.tile_properties[pos] = properties
    
    def is_position_walkable(self, x: int, y: int) -> bool:
        """Check if a position is walkable"""
        # Convert from screen coordinates to tile coordinates
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        
        if not self.is_within_bounds(tile_x, tile_y):
            return False
            
        tile = self.get_tile(tile_x, tile_y)
        
        # Check general walkability
        if tile not in self.walkable_tiles:
            return False
            
        # Check specific tile properties
        properties = self.get_tile_properties(tile_x, tile_y)
        if properties.get("blocked", False):
            return False
            
        return True
    
    def is_position_interactable(self, x: int, y: int) -> bool:
        """Check if a position has an interactable element"""
        # Convert from screen coordinates to tile coordinates
        tile_x = x // self.tile_size
        tile_y = y // self.tile_size
        
        return (tile_x, tile_y) in self.interactable_positions
    
    def add_interactable_position(self, x: int, y: int):
        """Mark a position as interactable"""
        self.interactable_positions.add((x, y))
    
    def remove_interactable_position(self, x: int, y: int):
        """Remove a position from interactable set"""
        self.interactable_positions.discard((x, y))
    
    def add_region(self, region_id: str, name: str, x: int, y: int, width: int, height: int):
        """Add a region to the world"""
        self.regions[region_id] = {
            "name": name,
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
    
    def draw(self):
        """Draw the visible portion of the world"""
        # Calculate visible tile range based on camera position
        screen_width = pyxel.width
        screen_height = pyxel.height
        
        # Convert camera position to tile coordinates
        start_x = max(0, self.camera_x // self.tile_size)
        start_y = max(0, self.camera_y // self.tile_size)
        
        # Calculate how many tiles fit on screen
        tiles_x = (screen_width // self.tile_size) + 2
        tiles_y = (screen_height // self.tile_size) + 2
        
        # Ensure we don't go beyond the world boundaries
        end_x = min(start_x + tiles_x, self.width)
        end_y = min(start_y + tiles_y, self.height)
        
        # Draw visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                sprite_x, sprite_y = self.tile_sprites[tile]
                
                # Calculate screen position
                screen_x = (x * self.tile_size) - self.camera_x
                screen_y = (y * self.tile_size) - self.camera_y
                
                # Draw the tile
                pyxel.blt(
                    screen_x, screen_y,
                    0,  # Image bank
                    sprite_x, sprite_y,
                    self.tile_size, self.tile_size,
                    0  # Transparent color
                )
    
    def center_camera_on(self, x: int, y: int):
        """Center the camera on a position"""
        # Calculate desired camera position
        target_camera_x = x - (pyxel.width // 2)
        target_camera_y = y - (pyxel.height // 2)
        
        # Clamp camera within world bounds
        self.camera_x = max(0, min(target_camera_x, (self.width * self.tile_size) - pyxel.width))
        self.camera_y = max(0, min(target_camera_y, (self.height * self.tile_size) - pyxel.height))
    
    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert screen coordinates to world coordinates"""
        world_x = screen_x + self.camera_x
        world_y = screen_y + self.camera_y
        return (world_x, world_y)
    
    def world_to_screen(self, world_x: int, world_y: int) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        screen_x = world_x - self.camera_x
        screen_y = world_y - self.camera_y
        return (screen_x, screen_y)
    
    def generate_empty_world(self):
        """Generate an empty world with floor tiles"""
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = TileType.FLOOR
    
    def generate_random_world(self, seed: int = None):
        """Generate a random world with various terrain types"""
        if seed is not None:
            random.seed(seed)
        
        # First, fill with grass
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = TileType.GRASS
        
        # Generate some water bodies
        num_water_bodies = random.randint(3, 8)
        for _ in range(num_water_bodies):
            center_x = random.randint(5, self.width - 5)
            center_y = random.randint(5, self.height - 5)
            size = random.randint(3, 10)
            
            for y in range(center_y - size, center_y + size):
                for x in range(center_x - size, center_x + size):
                    if self.is_within_bounds(x, y):
                        # Create irregular water shapes
                        dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                        if dist < size * random.uniform(0.7, 1.0):
                            self.tiles[y][x] = TileType.WATER
        
        # Generate some paths
        num_paths = random.randint(3, 6)
        for _ in range(num_paths):
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)
            end_x = random.randint(0, self.width - 1)
            end_y = random.randint(0, self.height - 1)
            
            # Simple path generation
            x, y = start_x, start_y
            while (x, y) != (end_x, end_y):
                self.tiles[y][x] = TileType.PATH
                
                # Move closer to destination
                if x < end_x and random.random() < 0.7:
                    x += 1
                elif x > end_x and random.random() < 0.7:
                    x -= 1
                elif y < end_y and random.random() < 0.7:
                    y += 1
                elif y > end_y and random.random() < 0.7:
                    y -= 1
                else:
                    # Random movement to make paths less straight
                    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    dx, dy = random.choice(dirs)
                    new_x, new_y = x + dx, y + dy
                    if self.is_within_bounds(new_x, new_y):
                        x, y = new_x, new_y
        
        # Add some trees
        num_trees = random.randint(self.width * self.height // 50, self.width * self.height // 30)
        for _ in range(num_trees):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.tiles[y][x] == TileType.GRASS:
                self.tiles[y][x] = TileType.TREE
        
        # Add some rocks
        num_rocks = random.randint(self.width * self.height // 100, self.width * self.height // 70)
        for _ in range(num_rocks):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.tiles[y][x] == TileType.GRASS:
                self.tiles[y][x] = TileType.ROCK
    
    def generate_dungeon(self, num_rooms: int = 10, room_min_size: int = 3, room_max_size: int = 8):
        """Generate a dungeon with rooms and corridors"""
        # Start with all walls
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x] = TileType.WALL
        
        # Generate rooms
        rooms = []
        for _ in range(num_rooms):
            # Random room size and position
            w = random.randint(room_min_size, room_max_size)
            h = random.randint(room_min_size, room_max_size)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)
            
            # Check if this room overlaps with any existing room
            overlaps = False
            for room in rooms:
                rx, ry, rw, rh = room
                if (x < rx + rw and x + w > rx and
                    y < ry + rh and y + h > ry):
                    overlaps = True
                    break
            
            if not overlaps:
                # Create the room
                for room_y in range(y, y + h):
                    for room_x in range(x, x + w):
                        self.tiles[room_y][room_x] = TileType.FLOOR
                
                # Add room to list
                rooms.append((x, y, w, h))
        
        # Connect rooms with corridors
        for i in range(1, len(rooms)):
            # Connect each room to the previous room
            prev_room = rooms[i - 1]
            new_room = rooms[i]
            
            # Center points of rooms
            prev_x = prev_room[0] + prev_room[2] // 2
            prev_y = prev_room[1] + prev_room[3] // 2
            new_x = new_room[0] + new_room[2] // 2
            new_y = new_room[1] + new_room[3] // 2
            
            # Randomly decide to start horizontally or vertically
            if random.random() < 0.5:
                # First horizontal, then vertical
                self.create_horizontal_tunnel(prev_x, new_x, prev_y)
                self.create_vertical_tunnel(prev_y, new_y, new_x)
            else:
                # First vertical, then horizontal
                self.create_vertical_tunnel(prev_y, new_y, prev_x)
                self.create_horizontal_tunnel(prev_x, new_x, new_y)
        
        # Add some doors
        for room in rooms:
            x, y, w, h = room
            # Potentially add doors at room edges
            for room_x in range(x, x + w):
                if room_x > 0 and room_x < self.width - 1:
                    # Check north wall
                    if y > 1 and self.tiles[y-1][room_x] == TileType.WALL and self.tiles[y-2][room_x] == TileType.FLOOR:
                        if random.random() < 0.3:
                            self.tiles[y-1][room_x] = TileType.DOOR
                            self.add_interactable_position(room_x, y-1)
                    
                    # Check south wall
                    if y+h < self.height-1 and self.tiles[y+h][room_x] == TileType.WALL and self.tiles[y+h+1][room_x] == TileType.FLOOR:
                        if random.random() < 0.3:
                            self.tiles[y+h][room_x] = TileType.DOOR
                            self.add_interactable_position(room_x, y+h)
            
            for room_y in range(y, y + h):
                if room_y > 0 and room_y < self.height - 1:
                    # Check west wall
                    if x > 1 and self.tiles[room_y][x-1] == TileType.WALL and self.tiles[room_y][x-2] == TileType.FLOOR:
                        if random.random() < 0.3:
                            self.tiles[room_y][x-1] = TileType.DOOR
                            self.add_interactable_position(x-1, room_y)
                    
                    # Check east wall
                    if x+w < self.width-1 and self.tiles[room_y][x+w] == TileType.WALL and self.tiles[room_y][x+w+1] == TileType.FLOOR:
                        if random.random() < 0.3:
                            self.tiles[room_y][x+w] = TileType.DOOR
                            self.add_interactable_position(x+w, room_y)
    
    def create_horizontal_tunnel(self, x1: int, x2: int, y: int):
        """Create a horizontal tunnel between x1 and x2 at y"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if self.is_within_bounds(x, y):
                self.tiles[y][x] = TileType.FLOOR
    
    def create_vertical_tunnel(self, y1: int, y2: int, x: int):
        """Create a vertical tunnel between y1 and y2 at x"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if self.is_within_bounds(x, y):
                self.tiles[y][x] = TileType.FLOOR


def load_world(level_name: str) -> World:
    """Load a world from file or generate one if file doesn't exist"""
    world_file = f"assets/worlds/{level_name}.json"
    
    if os.path.exists(world_file):
        try:
            with open(world_file, 'r') as f:
                data = json.load(f)
                
            # Create world with specified dimensions
            world = World(
                width=data.get("width", 128),
                height=data.get("height", 128),
                tile_size=data.get("tile_size", 8)
            )
            world.name = data.get("name", level_name)
            
            # Load tiles
            tile_data = data.get("tiles", [])
            for y, row in enumerate(tile_data):
                for x, tile_value in enumerate(row):
                    world.tiles[y][x] = TileType(tile_value)
            
            # Load tile properties
            properties_data = data.get("tile_properties", {})
            for pos_str, props in properties_data.items():
                x, y = map(int, pos_str.split(","))
                world.tile_properties[(x, y)] = props
            
            # Load regions
            regions_data = data.get("regions", {})
            for region_id, region_data in regions_data.items():
                world.regions[region_id] = region_data
            
            # Load interactable positions
            interactable_data = data.get("interactable_positions", [])
            for pos_data in interactable_data:
                x, y = pos_data
                world.interactable_positions.add((x, y))
            
            return world
        except Exception as e:
            print(f"Error loading world {level_name}: {str(e)}")
    
    # If file doesn't exist or loading failed, generate a world
    print(f"Generating world for {level_name}")
    world = World()
    world.name = level_name
    
    if "dungeon" in level_name.lower():
        world.generate_dungeon()
    else:
        world.generate_random_world()
    
    return world


def save_world(world: World, level_name: str):
    """Save a world to file"""
    world_file = f"assets/worlds/{level_name}.json"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(world_file), exist_ok=True)
    
    # Convert tile grid to serializable format
    tile_data = []
    for row in world.tiles:
        tile_data.append([tile.value for tile in row])
    
    # Convert tile properties to serializable format
    properties_data = {}
    for pos, props in world.tile_properties.items():
        x, y = pos
        properties_data[f"{x},{y}"] = props
    
    # Convert interactable positions to serializable format
    interactable_data = []
    for pos in world.interactable_positions:
        interactable_data.append(pos)
    
    # Create world data
    data = {
        "name": world.name,
        "width": world.width,
        "height": world.height,
        "tile_size": world.tile_size,
        "tiles": tile_data,
        "tile_properties": properties_data,
        "regions": world.regions,
        "interactable_positions": interactable_data
    }
    
    # Save to file
    with open(world_file, 'w') as f:
        json.dump(data, f) 
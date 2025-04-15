"""
LlamaQuest - A modern, retro-style adventure game with AI-driven NPCs
"""

__version__ = "0.1.0"

from .entities import Enemy, InteractiveObject, Item

# Import core modules for easier access
from .game import GameEngine, run_game
from .player import Player
from .world import World, load_world, save_world

# Check for Rust core availability
try:
    from llamaquest_core import (
        PhysicsEngine,
        calculate_field_of_view,
        calculate_pathfinding,
        collision_detection,
    )

    _has_rust_core = True
except ImportError:
    _has_rust_core = False

    # Provide Python fallbacks for core functionality
    def calculate_pathfinding(
        start_x, start_y, end_x, end_y, walkable_map, max_steps=None
    ):
        """Python fallback for pathfinding"""
        import heapq

        # A* pathfinding implementation
        if max_steps is None:
            max_steps = 1000

        # Create a grid for tracking visited cells
        height = len(walkable_map)
        width = len(walkable_map[0]) if height > 0 else 0

        # If start or end is out of bounds or not walkable, return empty path
        if (
            start_x >= width
            or start_y >= height
            or end_x >= width
            or end_y >= height
            or not walkable_map[start_y][start_x]
            or not walkable_map[end_y][end_x]
        ):
            return []

        # A* algorithm
        open_set = [(0, 0, start_x, start_y, [])]  # (f_score, g_score, x, y, path)
        closed_set = set()

        while open_set and len(closed_set) < max_steps:
            f_score, g_score, x, y, path = heapq.heappop(open_set)

            # Check if we reached the goal
            if x == end_x and y == end_y:
                return path + [(x, y)]

            # Skip if already visited
            if (x, y) in closed_set:
                continue

            # Mark as visited
            closed_set.add((x, y))
            path = path + [(x, y)]

            # Check neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and walkable_map[ny][nx]
                    and (nx, ny) not in closed_set
                ):
                    ng_score = g_score + 1
                    nh_score = abs(nx - end_x) + abs(ny - end_y)  # Manhattan distance
                    nf_score = ng_score + nh_score

                    heapq.heappush(open_set, (nf_score, ng_score, nx, ny, path))

        return []

    def collision_detection(
        entity1_x,
        entity1_y,
        entity1_width,
        entity1_height,
        entity2_x,
        entity2_y,
        entity2_width,
        entity2_height,
    ):
        """Python fallback for collision detection"""
        return (
            entity1_x < entity2_x + entity2_width
            and entity1_x + entity1_width > entity2_x
            and entity1_y < entity2_y + entity2_height
            and entity1_y + entity1_height > entity2_y
        )

    def calculate_field_of_view(origin_x, origin_y, radius, obstacle_map):
        """Python fallback for FOV calculation"""
        import math

        height = len(obstacle_map)
        width = len(obstacle_map[0]) if height > 0 else 0

        # Create visibility map
        visibility_map = [[False for _ in range(width)] for _ in range(height)]

        # Origin is always visible
        if 0 <= origin_y < height and 0 <= origin_x < width:
            visibility_map[origin_y][origin_x] = True

        # Cast rays in a circle
        for angle in range(0, 360, 5):  # Step by 5 degrees for performance
            angle_rad = math.radians(angle)
            ray_x, ray_y = float(origin_x), float(origin_y)

            for step in range(1, radius + 1):
                ray_x += math.cos(angle_rad)
                ray_y += math.sin(angle_rad)

                # Round to get tile coordinates
                tile_x, tile_y = round(ray_x), round(ray_y)

                # Check boundaries
                if not (0 <= tile_y < height and 0 <= tile_x < width):
                    break

                # Mark as visible
                visibility_map[tile_y][tile_x] = True

                # Stop if hit obstacle
                if obstacle_map[tile_y][tile_x]:
                    break

        return visibility_map

    class PhysicsEngine:
        """Python fallback for physics engine"""

        def __init__(self, gravity=9.8, friction=0.1):
            self.gravity = gravity
            self.friction = friction

        def update_entity(
            self,
            position_x,
            position_y,
            velocity_x,
            velocity_y,
            is_on_ground,
            delta_time,
        ):
            """Update entity position and velocity"""
            # Apply gravity if not on ground
            new_velocity_y = velocity_y
            if not is_on_ground:
                new_velocity_y += self.gravity * delta_time

            # Apply friction
            new_velocity_x = velocity_x
            if is_on_ground:
                # Apply friction only when on ground
                if velocity_x > 0.0:
                    new_velocity_x = max(0.0, velocity_x - self.friction * delta_time)
                elif velocity_x < 0.0:
                    new_velocity_x = min(0.0, velocity_x + self.friction * delta_time)

            # Update position
            new_position_x = position_x + new_velocity_x * delta_time
            new_position_y = position_y + new_velocity_y * delta_time

            return ((new_position_x, new_position_y), (new_velocity_x, new_velocity_y))


def has_rust_core():
    """Check if Rust core is available"""
    return _has_rust_core

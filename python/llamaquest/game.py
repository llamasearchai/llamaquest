"""
Core game module for LlamaQuest - Main gameplay loop and game state management
"""

import time
import pyxel
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

from .ai import create_npc_manager, NPCBehavior
from .world import World, load_world
from .player import Player
from .entities import Entity, Item, InteractiveObject

@dataclass
class GameState:
    """Represents the complete game state"""
    player: Player
    world: World
    npcs: Dict[str, NPCBehavior]
    entities: List[Entity] = field(default_factory=list)
    items: List[Item] = field(default_factory=list)
    interactive_objects: List[InteractiveObject] = field(default_factory=list)
    
    # Game state flags
    paused: bool = False
    game_over: bool = False
    current_quest: Optional[str] = None
    
    # Time tracking
    game_time: float = 0.0
    last_update: float = 0.0
    
    def update_game_time(self):
        """Update the in-game time counter"""
        current_time = time.time()
        if self.last_update > 0:
            self.game_time += current_time - self.last_update
        self.last_update = current_time


class GameEngine:
    """Main game engine for LlamaQuest"""
    
    def __init__(self, config: Dict = None):
        """Initialize the game engine with optional configuration"""
        self.config = config or {
            "screen_width": 160,
            "screen_height": 120,
            "scale": 4,
            "fps": 60,
            "title": "LlamaQuest",
            "start_level": "village"
        }
        
        # Initialize game components
        self.world = load_world(self.config["start_level"])
        self.player = Player(x=80, y=60)
        self.npcs = create_npc_manager(num_npcs=5)
        
        # Create game state
        self.state = GameState(
            player=self.player,
            world=self.world,
            npcs=self.npcs
        )
        
        # Initialize Pyxel
        pyxel.init(
            width=self.config["screen_width"],
            height=self.config["screen_height"],
            title=self.config["title"],
            fps=self.config["fps"],
            display_scale=self.config["scale"]
        )
        
        # Load resources
        pyxel.load("assets/resource.pyxres")
    
    def start(self):
        """Start the game loop"""
        self.state.last_update = time.time()
        pyxel.run(self.update, self.draw)
    
    def update(self):
        """Update game state - called every frame"""
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        if self.state.paused:
            if pyxel.btnp(pyxel.KEY_P):
                self.state.paused = False
            return
            
        if pyxel.btnp(pyxel.KEY_P):
            self.state.paused = True
            return
        
        self.state.update_game_time()
        
        # Update player
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.move(-1, 0, self.world)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.move(1, 0, self.world)
        if pyxel.btn(pyxel.KEY_UP):
            self.player.move(0, -1, self.world)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.move(0, 1, self.world)
            
        # Interaction key
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.handle_interaction()
            
        # Update NPCs and other entities
        self.update_npcs()
        self.update_entities()
        
        # Check quest progress
        self.check_quests()
    
    def draw(self):
        """Render the game - called every frame after update"""
        pyxel.cls(0)
        
        # Draw world
        self.world.draw()
        
        # Draw entities
        for entity in self.state.entities:
            entity.draw()
            
        # Draw interactive objects
        for obj in self.state.interactive_objects:
            obj.draw()
            
        # Draw NPCs
        for npc_id, npc in self.state.npcs.items():
            # This assumes NPCs have a position and sprite in the world
            # You would need to connect the AI behavior with actual entity positions
            pass
            
        # Draw player
        self.player.draw()
        
        # Draw UI
        self.draw_ui()
        
        # Draw pause screen if needed
        if self.state.paused:
            self.draw_pause_screen()
            
        # Draw game over screen if needed
        if self.state.game_over:
            self.draw_game_over_screen()
    
    def handle_interaction(self):
        """Handle player interaction with the world"""
        # Find what's in front of the player
        interact_x, interact_y = self.player.get_interaction_position()
        
        # Check for NPC interactions
        for npc_id, npc in self.state.npcs.items():
            # This assumes NPCs have a position in the world
            # You would need to check if the NPC is at the interaction position
            # If found, trigger dialogue or other interaction
            pass
            
        # Check for interactive objects
        for obj in self.state.interactive_objects:
            if obj.x == interact_x and obj.y == interact_y:
                obj.interact(self.player, self.state)
                return
    
    def update_npcs(self):
        """Update all NPCs based on their AI behavior"""
        for npc_id, npc in self.state.npcs.items():
            # Create a context for the NPC's decision making
            game_context = {
                "player_nearby": self.is_player_near_npc(npc_id),
                "time_of_day": self.get_time_of_day(),
                # Add other relevant context
            }
            
            # Get the NPC's decision
            action = npc.decide_action(game_context)
            
            # Execute the action (in a real implementation, this would move the NPC, etc.)
            self.execute_npc_action(npc_id, action)
    
    def is_player_near_npc(self, npc_id: str) -> bool:
        """Check if the player is near a specific NPC"""
        # This would need actual positions for NPCs
        return False
    
    def get_time_of_day(self) -> str:
        """Get the current time of day in the game world"""
        # Calculate based on game_time
        day_cycle = (self.state.game_time % 1200) / 1200  # 20-minute day cycle
        
        if 0.0 <= day_cycle < 0.25:
            return "morning"
        elif 0.25 <= day_cycle < 0.5:
            return "afternoon"
        elif 0.5 <= day_cycle < 0.75:
            return "evening"
        else:
            return "night"
    
    def execute_npc_action(self, npc_id: str, action: str):
        """Execute an action for an NPC"""
        # This would involve updating the NPC's position, animation state, etc.
        pass
    
    def update_entities(self):
        """Update all game entities"""
        for entity in self.state.entities:
            entity.update(self.state)
    
    def check_quests(self):
        """Check and update quest progress"""
        if self.state.current_quest:
            # Check completion conditions for the current quest
            pass
    
    def draw_ui(self):
        """Draw game UI elements"""
        # Draw health bar
        pyxel.rect(5, 5, 5 + self.player.health, 10, 8)
        pyxel.rectb(5, 5, 5 + 100, 10, 7)
        
        # Draw current quest indicator if any
        if self.state.current_quest:
            pyxel.text(5, 20, f"Quest: {self.state.current_quest}", 7)
    
    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        pyxel.rect(40, 40, 80, 40, 0)
        pyxel.rectb(40, 40, 80, 40, 7)
        pyxel.text(60, 55, "PAUSED", 7)
        pyxel.text(45, 70, "Press P to continue", 7)
    
    def draw_game_over_screen(self):
        """Draw the game over screen"""
        pyxel.rect(40, 40, 80, 40, 0)
        pyxel.rectb(40, 40, 80, 40, 7)
        pyxel.text(55, 55, "GAME OVER", 7)
        pyxel.text(45, 70, "Press R to restart", 7)


def run_game():
    """Entry point to start the game"""
    game = GameEngine()
    game.start() 
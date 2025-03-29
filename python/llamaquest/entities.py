"""
Entities module for LlamaQuest - Defines game objects, items, NPCs and interactive elements
"""

import pyxel
from typing import Dict, List, Tuple, Optional, Callable
from abc import ABC, abstractmethod
from enum import Enum

class EntityType(Enum):
    """Types of entities in the game"""
    PLAYER = 0
    NPC = 1
    ITEM = 2
    INTERACTIVE = 3
    ENEMY = 4
    PROJECTILE = 5
    EFFECT = 6

class Entity(ABC):
    """Base class for all game entities"""
    
    def __init__(self, x: int, y: int, entity_type: EntityType, sprite_x: int, sprite_y: int):
        """Initialize the entity"""
        self.x = x
        self.y = y
        self.entity_type = entity_type
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.sprite_width = 8
        self.sprite_height = 8
        self.sprite_bank = 0  # Default image bank
        self.is_visible = True
        self.is_active = True
        self.collision_enabled = True
        
    def update(self, game_state):
        """Update entity state - to be overridden by subclasses"""
        pass
    
    def draw(self):
        """Draw the entity at its current position"""
        if self.is_visible:
            pyxel.blt(
                self.x, self.y,
                self.sprite_bank,
                self.sprite_x, self.sprite_y,
                self.sprite_width, self.sprite_height,
                0  # Transparent color
            )
    
    def collides_with(self, other) -> bool:
        """Check if this entity collides with another"""
        if not (self.collision_enabled and other.collision_enabled):
            return False
            
        # Simple box collision
        return (
            self.x < other.x + other.sprite_width and
            self.x + self.sprite_width > other.x and
            self.y < other.y + other.sprite_height and
            self.y + self.sprite_height > other.y
        )
    
    def distance_to(self, other) -> float:
        """Calculate distance to another entity"""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2)**0.5


class ItemType(Enum):
    """Types of items in the game"""
    WEAPON = 0
    ARMOR = 1
    POTION = 2
    KEY = 3
    QUEST = 4
    TREASURE = 5
    CONSUMABLE = 6

class Item(Entity):
    """Represents an item that can be picked up and used"""
    
    def __init__(self, x: int, y: int, item_id: str, name: str, 
                 item_type: ItemType, sprite_x: int, sprite_y: int,
                 value: int = 0, description: str = ""):
        """Initialize an item"""
        super().__init__(x, y, EntityType.ITEM, sprite_x, sprite_y)
        self.id = item_id
        self.name = name
        self.item_type = item_type
        self.value = value
        self.description = description
        self.properties = {}  # Additional item properties
        
    def use(self, player, game_state) -> bool:
        """Use the item - to be overridden by subclasses"""
        return False
    
    def pick_up(self, player) -> bool:
        """Handle item being picked up"""
        if player.add_to_inventory(self):
            self.is_active = False
            self.is_visible = False
            return True
        return False


class Weapon(Item):
    """A weapon item with attack properties"""
    
    def __init__(self, x: int, y: int, item_id: str, name: str, 
                 sprite_x: int, sprite_y: int, damage: int, 
                 attack_speed: float, attack_range: int,
                 value: int = 0, description: str = ""):
        """Initialize a weapon"""
        super().__init__(x, y, item_id, name, ItemType.WEAPON, 
                        sprite_x, sprite_y, value, description)
        self.damage = damage
        self.attack_speed = attack_speed
        self.attack_range = attack_range
        
    def use(self, player, game_state) -> bool:
        """Use the weapon (equip it)"""
        player.equip_weapon(self)
        return True


class Armor(Item):
    """An armor item with defense properties"""
    
    def __init__(self, x: int, y: int, item_id: str, name: str, 
                 sprite_x: int, sprite_y: int, defense: int,
                 value: int = 0, description: str = ""):
        """Initialize armor"""
        super().__init__(x, y, item_id, name, ItemType.ARMOR, 
                        sprite_x, sprite_y, value, description)
        self.defense = defense
        
    def use(self, player, game_state) -> bool:
        """Use the armor (equip it)"""
        player.equip_armor(self)
        return True


class Potion(Item):
    """A consumable potion with effects"""
    
    def __init__(self, x: int, y: int, item_id: str, name: str, 
                 sprite_x: int, sprite_y: int, effect_type: str, 
                 effect_amount: int, value: int = 0, description: str = ""):
        """Initialize a potion"""
        super().__init__(x, y, item_id, name, ItemType.POTION, 
                        sprite_x, sprite_y, value, description)
        self.effect_type = effect_type
        self.effect_amount = effect_amount
        
    def use(self, player, game_state) -> bool:
        """Use the potion (consume it)"""
        if self.effect_type == "health":
            player.heal(self.effect_amount)
        elif self.effect_type == "energy":
            player.restore_energy(self.effect_amount)
        # Remove from inventory (handled by the inventory system)
        return True


class InteractiveObject(Entity):
    """An object in the world that can be interacted with"""
    
    def __init__(self, x: int, y: int, obj_id: str, name: str, 
                 sprite_x: int, sprite_y: int, interaction_type: str,
                 description: str = ""):
        """Initialize an interactive object"""
        super().__init__(x, y, EntityType.INTERACTIVE, sprite_x, sprite_y)
        self.id = obj_id
        self.name = name
        self.interaction_type = interaction_type
        self.description = description
        self.is_interactable = True
        self.interaction_handlers = {}
        
    def interact(self, player, game_state) -> bool:
        """Handle interaction with this object"""
        if not self.is_interactable:
            return False
            
        if self.interaction_type in self.interaction_handlers:
            return self.interaction_handlers[self.interaction_type](player, game_state)
            
        # Default interaction types
        if self.interaction_type == "door":
            return self.open_door(player, game_state)
        elif self.interaction_type == "chest":
            return self.open_chest(player, game_state)
        elif self.interaction_type == "sign":
            return self.read_sign(player, game_state)
            
        return False
    
    def add_interaction_handler(self, interaction_type: str, handler: Callable):
        """Add a custom interaction handler"""
        self.interaction_handlers[interaction_type] = handler
    
    def open_door(self, player, game_state) -> bool:
        """Handle opening a door"""
        # Check if door is locked and player has key
        # For now, just make the door passable
        self.collision_enabled = False
        self.sprite_x += self.sprite_width  # Switch to open door sprite
        return True
    
    def open_chest(self, player, game_state) -> bool:
        """Handle opening a chest"""
        # Could spawn items, trigger events, etc.
        self.sprite_x += self.sprite_width  # Switch to open chest sprite
        return True
    
    def read_sign(self, player, game_state) -> bool:
        """Handle reading a sign"""
        # Show dialog with sign message
        # This would integrate with a dialog system
        return True


class Enemy(Entity):
    """An enemy entity with AI behavior"""
    
    def __init__(self, x: int, y: int, enemy_id: str, name: str, 
                 sprite_x: int, sprite_y: int, health: int, damage: int):
        """Initialize an enemy"""
        super().__init__(x, y, EntityType.ENEMY, sprite_x, sprite_y)
        self.id = enemy_id
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.movement_speed = 1
        self.detection_range = 80
        self.attack_range = 10
        self.attack_cooldown = 30
        self.attack_timer = 0
        self.state = "idle"  # idle, patrol, chase, attack
        self.patrol_points = []
        self.current_patrol_index = 0
        
    def update(self, game_state):
        """Update enemy state"""
        # Update attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1
        
        # Update behavior based on state
        if self.state == "idle":
            # Chance to start patrolling
            if pyxel.frame_count % 180 == 0 and len(self.patrol_points) > 0:
                self.state = "patrol"
                
            # Check for player detection
            player_distance = self.distance_to(game_state.player)
            if player_distance <= self.detection_range:
                self.state = "chase"
        
        elif self.state == "patrol":
            self.patrol_behavior(game_state)
            
            # Check for player detection
            player_distance = self.distance_to(game_state.player)
            if player_distance <= self.detection_range:
                self.state = "chase"
        
        elif self.state == "chase":
            self.chase_behavior(game_state)
            
            # Check if in attack range
            player_distance = self.distance_to(game_state.player)
            if player_distance <= self.attack_range:
                self.state = "attack"
            elif player_distance > self.detection_range * 1.5:
                # Lost player, go back to idle
                self.state = "idle"
        
        elif self.state == "attack":
            self.attack_behavior(game_state)
            
            # Check if still in attack range
            player_distance = self.distance_to(game_state.player)
            if player_distance > self.attack_range:
                self.state = "chase"
    
    def patrol_behavior(self, game_state):
        """Handle patrol behavior"""
        if not self.patrol_points:
            self.state = "idle"
            return
            
        # Move toward current patrol point
        target_x, target_y = self.patrol_points[self.current_patrol_index]
        self.move_toward(target_x, target_y, game_state)
        
        # Check if reached patrol point
        if abs(self.x - target_x) < self.movement_speed and abs(self.y - target_y) < self.movement_speed:
            # Move to next patrol point
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
    
    def chase_behavior(self, game_state):
        """Handle chase behavior"""
        # Move toward player
        self.move_toward(game_state.player.x, game_state.player.y, game_state)
    
    def attack_behavior(self, game_state):
        """Handle attack behavior"""
        if self.attack_timer == 0:
            # Attack the player
            game_state.player.take_damage(self.damage)
            self.attack_timer = self.attack_cooldown
    
    def move_toward(self, target_x: int, target_y: int, game_state):
        """Move toward a target position"""
        dx = 0
        dy = 0
        
        if self.x < target_x:
            dx = self.movement_speed
        elif self.x > target_x:
            dx = -self.movement_speed
            
        if self.y < target_y:
            dy = self.movement_speed
        elif self.y > target_y:
            dy = -self.movement_speed
        
        # Simple collision check with world
        new_x = self.x + dx
        new_y = self.y + dy
        
        if game_state.world.is_position_walkable(new_x, self.y):
            self.x = new_x
            
        if game_state.world.is_position_walkable(self.x, new_y):
            self.y = new_y
    
    def take_damage(self, amount: int) -> bool:
        """Handle enemy taking damage, returns True if still alive"""
        self.health = max(0, self.health - amount)
        
        # If damaged, become aggressive
        if self.state != "attack" and self.state != "chase":
            self.state = "chase"
            
        return self.health > 0 
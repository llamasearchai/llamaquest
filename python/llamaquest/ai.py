"""
AI module for LlamaQuest - Provides NPC behavior and dialogue generation
"""

import random
from enum import Enum
from typing import Dict, List, Optional, Tuple


class NPCMood(Enum):
    FRIENDLY = "friendly"
    NEUTRAL = "neutral"
    HOSTILE = "hostile"
    SCARED = "scared"
    CURIOUS = "curious"


class NPCPersonality:
    def __init__(self, traits: Dict[str, float] = None):
        self.traits = traits or {
            "friendliness": random.uniform(0.2, 0.8),
            "intelligence": random.uniform(0.3, 0.9),
            "courage": random.uniform(0.2, 0.9),
            "patience": random.uniform(0.3, 0.8),
            "curiosity": random.uniform(0.2, 0.9),
        }

    def get_dominant_trait(self) -> Tuple[str, float]:
        return max(self.traits.items(), key=lambda x: x[1])


class DialogueGenerator:
    """Generates contextual dialogue for NPCs based on their personality and situation"""

    TEMPLATES = {
        NPCMood.FRIENDLY: [
            "Hello there, adventurer! Can I help you with anything?",
            "It's a pleasure to meet you! What brings you to these parts?",
            "Welcome, friend! I've been hoping to meet someone new.",
            "Ah, a visitor! We don't get many of those around here.",
        ],
        NPCMood.NEUTRAL: [
            "Yes? What do you want?",
            "I'm a bit busy right now.",
            "Do you need something?",
            "State your business, traveler.",
        ],
        NPCMood.HOSTILE: [
            "Back off if you know what's good for you.",
            "I don't take kindly to strangers.",
            "You've got some nerve coming here.",
            "Keep your distance, outsider.",
        ],
        NPCMood.SCARED: [
            "P-please don't hurt me!",
            "I don't want any trouble!",
            "Stay back! I'm warning you!",
            "Oh no, please just leave me alone!",
        ],
        NPCMood.CURIOUS: [
            "Interesting... where did you come from?",
            "I've never seen someone like you before. Tell me more!",
            "What strange items you're carrying! May I take a closer look?",
            "You seem to have traveled far. What stories can you share?",
        ],
    }

    @classmethod
    def generate_greeting(
        cls, personality: NPCPersonality, current_mood: NPCMood
    ) -> str:
        """Generate an appropriate greeting based on NPC personality and mood"""
        templates = cls.TEMPLATES.get(current_mood, cls.TEMPLATES[NPCMood.NEUTRAL])
        return random.choice(templates)


class NPCBehavior:
    """Controls NPC behavior, decisions, and reactions to player actions"""

    def __init__(self, npc_id: str, name: str):
        self.npc_id = npc_id
        self.name = name
        self.personality = NPCPersonality()
        self.mood = NPCMood.NEUTRAL
        self.memory = []  # track interactions with player

    def update_mood(self, player_action: str, context: Dict) -> NPCMood:
        """Update NPC mood based on player actions and context"""
        # Simple mood simulation based on personality traits
        friendliness = self.personality.traits["friendliness"]

        if "attack" in player_action.lower():
            self.mood = (
                NPCMood.HOSTILE
                if self.personality.traits["courage"] > 0.7
                else NPCMood.SCARED
            )
        elif "gift" in player_action.lower() or "help" in player_action.lower():
            self.mood = NPCMood.FRIENDLY
        elif "question" in player_action.lower():
            if self.personality.traits["curiosity"] > 0.6:
                self.mood = NPCMood.CURIOUS
            else:
                self.mood = NPCMood.NEUTRAL

        # Record interaction in memory
        self.memory.append({"action": player_action, "resulting_mood": self.mood})

        return self.mood

    def decide_action(self, game_state: Dict) -> str:
        """Decide what action the NPC should take based on game state and personality"""
        # Simple decision tree based on personality and mood
        if self.mood == NPCMood.HOSTILE:
            if "player_nearby" in game_state and game_state["player_nearby"]:
                return "attack_player"
            else:
                return "patrol_aggressively"

        elif self.mood == NPCMood.SCARED:
            return "flee_from_player"

        elif self.mood == NPCMood.FRIENDLY:
            if random.random() < self.personality.traits["helpfulness"]:
                return "offer_help"
            else:
                return "engage_conversation"

        # Default behavior for neutral or curious
        return "idle_activity"

    def generate_dialogue(self, dialogue_type: str = "greeting") -> str:
        """Generate appropriate dialogue based on NPC's current state"""
        if dialogue_type == "greeting":
            return DialogueGenerator.generate_greeting(self.personality, self.mood)

        # Can be expanded for different dialogue types
        return "Hello, traveler."


def create_npc_manager(num_npcs: int = 5) -> Dict[str, NPCBehavior]:
    """Create and initialize a group of NPCs with random personalities"""
    npc_names = [
        "Elwin",
        "Gorm",
        "Thalia",
        "Zeph",
        "Mira",
        "Krag",
        "Lyra",
        "Finn",
        "Orla",
        "Vex",
    ]
    npcs = {}

    for i in range(min(num_npcs, len(npc_names))):
        npc_id = f"npc_{i+1}"
        name = npc_names[i]
        npcs[npc_id] = NPCBehavior(npc_id, name)

    return npcs

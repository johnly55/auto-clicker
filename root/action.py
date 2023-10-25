"""TODO"""
from enum import Enum


class Action:
    """Automated action"""
    class ActionType(Enum):
        CLICK = 1
    
    action_name: str = ...
    action: dict = ...

    def __init__(self, value: ActionType) -> None:
        """TODO"""
        self._set_action(value)
    
    def _set_action(self, value: ActionType):
        action = {}

        match value:
            # Action of a mouse click.
            case self.ActionType.CLICK:
                action_name = 'click'
                action[action_name] = self._get_presets()
            # Default case.
            case _:
                pass
        
        self.action_name = action_name
        self.action = action
        
    def _get_presets(self) -> dict:
        presets = {
            'occurrences' : 1,
            'delay' : 0,
            'delay_per_occurrence': 0,
            'mouse_position': {
                'x_position': None,
                'y_position': None
            },
            'conditions': [],
        }

        return presets

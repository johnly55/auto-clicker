"""Action deals with automatable actions.

TODO
"""
from enum import Enum


class Action:
    """Automated action."""
    class ActionType(Enum):
        """Type of automatable actions."""
        CLICK = 1

    action_name: str = ...
    action: dict = ...

    def __init__(self, value: ActionType) -> None:
        """Sets action to a preset action type."""
        self._set_action(value)

    def _set_action(self, value: ActionType):
        """Set certain presets based on action type."""
        action = {}

        match value:
            case self.ActionType.CLICK:
                action_name = 'click'
                action = self._get_presets()
                action['action_type'] = action_name
            case _:
                pass

        self.action_name = action_name
        self.action = action

    def _get_presets(self) -> dict:
        """Return presets every action should have."""
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

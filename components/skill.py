class Skill:
    def __init__(self, use_function=None, skill_targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.skill_targeting = skill_targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
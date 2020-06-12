from hypothesis import settings

settings.register_profile('default', deadline=None)
settings.register_profile('ci', max_examples=1000)

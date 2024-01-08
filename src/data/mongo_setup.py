import mongoengine


def global_init():
    # mongoengine.register_connection(alias="core", name="budget")
    mongoengine.connect("budget", alias="core", )

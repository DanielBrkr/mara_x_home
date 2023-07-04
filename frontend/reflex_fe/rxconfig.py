import reflex as rx

class ReflexfeConfig(rx.Config):
    pass

config = ReflexfeConfig(
    app_name="reflex_fe",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
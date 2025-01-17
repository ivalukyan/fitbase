from pydantic import BaseModel


class NormativeSchemas(BaseModel):
    id: int
    username: str
    telegram_id: int | None = None
    grom: str | None = None
    turkish_barbell_lifting: int | None = None
    jump_rope: int | None = None
    bench_press: int | None = None
    rod_length: int | None = None
    shuttle_run: int | None = None
    glute_bridge: int | None = None
    pull_ups: int | None = None
    cubic_jumps: int | None = None
    lifting_barbell_on_the_chest_count: int | None = None
    axel_deadlift: int | None = None
    handstand: str | None = None
    classic_squat: int | None = None
    turkish_kettlebell_lifting: int | None = None
    push_ups: int | None = None
    lifting_barbell_on_the_chest_kilo: int | None = None
    walking_kettlebells: int | None = None
    deadlift: int | None = None
    long_jump: int | None = None
    barbell_jerk: int | None = None
    axel_hold: str | None = None
    front_squat: int | None = None
    msg: str | None = None

    class Config:
        from_attributes = True
from pydantic import BaseModel


class NormativeSchemas(BaseModel):
    id: int
    username: str
    telegram_id: int
    grom: str
    turkish_barbell_lifting: int
    jump_rope: int
    bench_press: int
    rod_length: int
    shuttle_run: int
    glute_bridge: int
    pull_ups: int
    cubic_jumps: int
    lifting_barbell_on_the_chest_count: int
    axel_deadlift: int
    handstand: str
    classic_squat: int
    turkish_kettlebell_lifting: int
    push_ups: int
    lifting_barbell_on_the_chest_kilo: int
    walking_kettlebells: int
    deadlift: int
    long_jump: int
    barbell_jerk: int
    axel_hold: str
    front_squat: int

    class Config:
        from_attributes = True
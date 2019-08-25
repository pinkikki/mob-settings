from peewee import *

from mob_settings.db.proxy import BaseModel


class Scene(BaseModel):
    id = AutoField()
    code = CharField()
    lang = CharField()
    name = CharField()


def scene_save(values):
    for row in values:
        scene = Scene(code=row[0], lang='ja', name=row[1])
        scene.save()


def scene_list():
    return Scene.select()


class ScenePoint(BaseModel):
    id = AutoField()
    scene_code = CharField()
    point = IntegerField()
    x = FloatField()
    y = FloatField()
    z = FloatField()

    class Meta:
        db_table = 'scene_point'


class SceneGameObject(BaseModel):
    id = AutoField()
    scene_code = CharField()
    scene_section = IntegerField()
    game_object_name = CharField()
    scene_point = IntegerField()
    direction = IntegerField()

    def __init__(self, scene_code=None, scene_section=None, game_object_name=None,
                 scene_point=None,
                 direction=None, *args, **kwargs):
        super().__init__(scene_code=scene_code, scene_section=scene_section, game_object_name=game_object_name,
                         scene_point=scene_point,
                         direction=direction, *args, *kwargs)

    @classmethod
    def of(cls, scene_code, scene_section, game_object_name, scene_point, direction):
        return cls(scene_code=scene_code, scene_section=scene_section, game_object_name=game_object_name,
                   scene_point=scene_point,
                   direction=direction)

    class Meta:
        db_table = 'scene_game_object'


class SceneMapping(BaseModel):
    id = AutoField()
    from_scene_code = CharField()
    from_scene_point = IntegerField()
    to_scene_code = CharField()
    to_scene_point = IntegerField()

    def __init__(self, from_scene_code=None, from_scene_point=None, to_scene_code=None, to_scene_point=None, *args,
                 **kwargs):
        super().__init__(from_scene_code=from_scene_code, from_scene_point=from_scene_point,
                         to_scene_code=to_scene_code, to_scene_point=to_scene_point, *args, *kwargs)

    @classmethod
    def of(cls, from_scene_code, from_scene_point, to_scene_code, to_scene_point):
        return cls(from_scene_code=from_scene_code, from_scene_point=from_scene_point,
                   to_scene_code=to_scene_code,
                   to_scene_point=to_scene_point)

    class Meta:
        db_table = 'scene_mapping'


class Position(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def scene_point_save(scene_code, positions):
    count = 0
    for position in positions:
        count += 1
        scene_point = ScenePoint(scene_code=scene_code, point=1, x=position.x, y=position.y, z=0)
        scene_point.save()


def scene_game_object_save(scene_game_objects):
    for scene_game_object in scene_game_objects:
        scene_game_object.save()


def scene_game_object_list():
    return SceneGameObject.select()

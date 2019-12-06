import model
from random import uniform
    
def get_debug(fs):
    st = ""
    for item in fs:
        nm  = "" 
        st = st+ str(item) + " "
    return st
class MyStrategy:
    def __init__(self):
        self.vv = 1;
        self.px = -1;
        pass

    def get_action(self, unit, game, debug):
        # Replace this code with your own
        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)
        target_pos = unit.position
        if unit.weapon is None and nearest_weapon is not None:
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position
        debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        velo = (target_pos.x - unit.position.x)*uniform(-1,2)
        debug.draw(model.CustomData.Log("velo: {:f}".format(velo)))
        debug.draw(model.CustomData.Log("dx: {:f}".format(self.px - unit.position.x)))

        debug.draw(model.CustomData.Log(repr(game.properties)))
        tmp = game.level.tiles
        debug.draw(model.CustomData.Log(get_debug([tmp[int(unit.position.x)][int(unit.position.y)],tmp[int(unit.position.x - 1)][int(unit.position.y)],tmp[int(unit.position.x)][int(unit.position.y+1)],tmp[int(unit.position.x + 1)][int(unit.position.y)],tmp[int(unit.position.x)][int(unit.position.y-1)]])))
        aim = model.Vec2Double(0, 0)
        if nearest_enemy is not None:
            aim = model.Vec2Double(
                nearest_enemy.position.x - unit.position.x,
                nearest_enemy.position.y - unit.position.y)
        jump = target_pos.y > unit.position.y
        
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if unit.position.x >= (len(game.level.tiles)-2):
            self.vv = -1
        if unit.position.x <= 2:
            self.vv = 1
        jump = True
        if game.level.tiles[int(unit.position.x)][int(unit.position.y)] == model.Tile.PLATFORM and self.px - unit.position.x:
            jump = False
        self.px = unit.position.x;
        return model.UnitAction(
            velocity=game.properties.unit_max_horizontal_speed * self.vv,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot=True,
            reload=False,
            swap_weapon=False,
            plant_mine=False)


if __name__ == '__main__':
    from subprocess import call
    call("python3 /home/user/Documents/aicup/aicup-python/main.py",shell=True)
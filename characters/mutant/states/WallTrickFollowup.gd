extends BeastState

const GO_FRAME = 16
const MOVE_X_1 = "2"
const MOVE_Y_1 = "0.5"
const MOVE_X_2 = "1.5"
const MOVE_Y_2 = "1"
const MOVE_X_3 = "0"
const MOVE_Y_3 = "1"


export  var move_x_ = "2"
export  var move_y_ = "0.5"
export  var move_speed = "37"

var move_x = "0"
var move_y = "0"

func _enter():
	var move = fixed.normalized_vec_times(move_x_, move_y_, move_speed)
	move_x = fixed.mul(move.x, str(host.get_facing_int()))
	move_y = move.y


func _frame_0():
	var wall = host.touching_which_wall()
	if wall != 0:
		host.set_facing( - wall)
		if host.reverse_state:
			host.set_facing(wall)

func _tick():
	if current_tick > 3:
		host.set_vel(move_x, move_y)
		if host.is_grounded() or host.get_pos().y > - 2:
			host.set_pos(host.get_pos().x, 0)
			return "Landing"





	

func _exit():
	host.set_vel(move_x, move_y)
	if host.is_grounded():
		var vel = host.get_vel()
		host.set_vel(fixed.mul(vel.x, "0.33"), vel.y)

extends RobotState

func _frame_0():

	host.start_magnetizing()






func is_usable():
	return host.magnet_ticks_left <= 0 and .is_usable() and host.grenade_object != null

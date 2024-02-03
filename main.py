from RealTimeListener import RealTimeKeyListener

online_listener = RealTimeKeyListener()


print(online_listener.get_sentence())

online_listener.keyboard_listener.join()
online_listener.mouse_listener.join()


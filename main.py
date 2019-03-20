import sched, time
s = sched.scheduler(time.time, time.sleep)
def print_time(a='default'):
	print("From print_time", time.time(), a)

def print_some_times():
	print(time.time())
	s.enter(10, 1, print_time)
	print("hi")
	s.enter(5, 2, print_time, argument=('positional',))
	print("hi")
	s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
	print("hi")
	s.run()
	print("hi")
	print(time.time())

print_some_times()
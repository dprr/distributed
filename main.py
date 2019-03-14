import ssss_lib

if __name__ == "__main__":
	print("enter your msg: ")
	msg = input()
	points = ssss_lib.generate_secret_from_msg(msg, 3, 4)
	print(ssss_lib.recover_secret(points))
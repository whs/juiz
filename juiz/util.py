import hashlib
import random

def random_id():
	return hashlib.sha256(str(random.random())).hexdigest()[:6]
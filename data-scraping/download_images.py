# USAGE
# python download_images.py --urls urls.txt --output images/santa

# import the necessary packages
from imutils import paths
import argparse
import requests
import cv2
import os

PATHS_FOLDER = "paths"
CAR_CLASSES_NAMES_PATH = "../data/cars_classes.names"
PICTURE_PATH = "../images/train2019"
LABEL_PATH = "../labels/train2019"


car_parts = {
"wheel": 1,
"door":2,
"frontbumper":3,
"rearbumper":4,
"headkight":5,
"brakelight":6,
"hood":7,
"mirror":8,
"windshield":9,
"grill":10,
"licenseplate":11,
"window":12}

FOLDER_NOT_FOUND = 2
FILE_NOT_FOUND = 3

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-u", "--urls", required=True,
# 	help="path to file containing image URLs")
# ap.add_argument("-o", "--output", required=True,
# 	help="path to output directory of images")
# args = vars(ap.parse_args())
#
# # grab the list of URLs from the input file, then initialize the
# # total number of images downloaded thus far
# rows = open(args["urls"]).read().strip().split("\n")
# total = 0
def verify_image(imagePath):
	try:
		image = cv2.imread(imagePath)

		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			print("None")
			delete = True
		else:
			return True

	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True

	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)
		return False


def get_number(number):
	seq_number = "0000000"
	digits = len(str(number))
	temp_number = seq_number[:-digits]
	return temp_number+str(number)



def make_request(url, timeout):
	try:
		r = requests.get(url, timeout=timeout)
		return r
	except:
		return 1

def save_picture(r, total, category):
	picture_name = "CARS_train2019_{}.jpg".format(get_number(total))
	label_name = "CARS_train2019_{}.txt".format(get_number(total))
	print(picture_name)
	if os.path.exists("{}".format(PICTURE_PATH)):
		p = os.path.sep.join(PICTURE_PATH, picture_name)
	else:
		os.mkdir("{}".format(PICTURE_PATH))
		p = os.path.sep.join(PICTURE_PATH, picture_name)

	f = open(p, "wb")
	f.write(r.content)
	f.close()

	valid = verify_image(p)

	if valid:
		if os.path.exists("{}".format(LABEL_PATH)):
			q = os.path.sep.join(LABEL_PATH, label_name)
		else:
			os.mkdir("{}".format(LABEL_PATH))
			q = os.path.sep.join(LABEL_PATH, label_name)

		f = open(q, "wb")
		f.write("{} {} {} {}".format(category, ))
		f.close()

	#update the counter
	print("[INFO] downloaded: {}".format(p))

# # loop the URLs
# for url in rows:
# 	try:
# 		# try to download the image
# 		#r = requests.get(url, timeout=60)
# 		r = make_request(url, 60)
# 		if r == 1:
# 			raise Exception('retry')
# 		else:
# 			# save the image to disk
# 			save_pictures(r, total)
# 			total += 1
#
# 	# handle if any exceptions are thrown during the download process
# 	except Exception as e:
# 		if e.args == 'retry':
# 			for x in range(1,4,1):
# 				r = make_request(url, 60 * x)
# 				if r == 1:
# 					continue
# 				else:
# 					save_pictures(r, total)
# 					total += 1
# 					break
# 		else:
# 			print("[INFO] error downloading {}...skipping".format(str(e)))
#
# 		print("error found {}".format(str(e)))
#
# # loop over the image paths we just downloaded
# for imagePath in paths.list_images(args["output"]):
# 	# initialize if the image should be deleted or not
# 	delete = False
#
# 	# try to load the image
# 	try:
# 		image = cv2.imread(imagePath)
#
# 		# if the image is `None` then we could not properly load it
# 		# from disk, so delete it
# 		if image is None:
# 			print("None")
# 			delete = True
#
# 	# if OpenCV cannot load the image then the image is likely
# 	# corrupt so we should delete it
# 	except:
# 		print("Except")
# 		delete = True
#
# 	# check to see if the image should be deleted
# 	if delete:
# 		print("[INFO] deleting {}".format(imagePath))
# 		os.remove(imagePath)

def open_file(file):
	# grab the list of URLs from the input file, then initialize the
	# total number of images downloaded thus far
	rows = open(file).read().strip().split("\n")
	# print(rows)
	return rows

def create_parts_order(car_parts):
	parts_order = {}

	for index, part in enumerate(car_parts):
		parts_order[part] = index

	return parts_order



def download_images(paths, total, category):

	for url in paths:
		print(url)
		try:
			# try to download the image
			#r = requests.get(url, timeout=60)
			r = make_request(url, 60)
			if r == 1:
				raise Exception('retry')
			else:
				# save the image to disk
				save_picture(r.content, total, category)
				total += 1

		# handle if any exceptions are thrown during the download process
		except Exception as e:
			if e.args == 'retry':
				for x in range(1,4,1):
					r = make_request(url, 60 * x)
					if r == 1:
						continue
					else:
						save_picture(r.content, total)
						total += 1
						break

			else:
				print("[INFO] error downloading {}...skipping".format(str(e)))

			print("error found {}".format(str(e)))

def main():
	""" Main program """
	if os.path.exists(CAR_CLASSES_NAMES_PATH):
		car_parts = open_file(CAR_CLASSES_NAMES_PATH)
		parts_order = create_parts_order(car_parts)
		print(parts_order)

	else:
		raise Exception(FOLDER_NOT_FOUND)

	#check folder exist
	if os.path.exists(PATHS_FOLDER):
		file_list = os.listdir(PATHS_FOLDER)

		counter = 10
		for file in file_list:
			filename=""
			label = ""
			# print(file)
			for part in parts_order.keys():
				if part in file:
					label = parts_order.get(part)
					print(label)

			paths = open_file(PATHS_FOLDER+'/'+file)

			download_images(paths, counter, label)
			#create the file_name for the picture

			#create the filename for the label

			#create the label_file

			#save it in the right location



		# print(paths)
	else:
		raise Exception(FOLDER_NOT_FOUND)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error = e.args
        print(str(e))

from os import listdir, remove
from os.path import *
import subprocess
import sys

# Some instance variables
save_tests = False
mypath = dirname(abspath(__file__))
tests_passed = 0
tests_failed = 0
failed_tests_list = {}
# initizlize this one to 1, in case the user doesn't specify a number
num_reps = 1

# Hella string slicing: we get the username of the user and the pathname of the file without the username, all from the current directory of the user
# This way, we can use this script for any project or user without hardcoding any values
username = mypath.split('/')[2]
current_project_name = mypath.split('/')[-1]
current_project_name = current_project_name[:current_project_name.index(username)] + current_project_name[current_project_name.index(username) + len(username) + 1:]
gheith_project_path = '/u/gheith/public/' + current_project_name

# Here's where we get the lists of tests to run
file_names = [f for f in listdir(gheith_project_path) if isfile(join(gheith_project_path, f))]
# We can add to the 'endswith' list to get as many file extensions as we want
tests = list(filter(lambda file: file.lower().endswith(('.cc', '.ok')), file_names))

# Here we clean up all of the tests that we downloaded
def cleanup():
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	tests_to_remove = list(filter(lambda file: file.lower().endswith(('.cc', '.ok', '.raw', '.diff')) and not file.lower().startswith(('t', username)), files))
	for test in tests_to_remove:
		remove(test)

# If we called this with the 'cleanup' argument, all we do is clean and terminate
if '-c' in sys.argv or '-C' in sys.argv:
	cleanup()
	exit()

# If we called this with the 'save' argument, we set a flag telling us not to clean up at the end
if '-s' in sys.argv or '-S' in sys.argv:
	save_tests = True

# If we called this with the 'repetitions' argument, we update the number of times to run the code, which is '1' by default
if '-r' in sys.argv:
	num_reps = int(sys.argv[sys.argv.index("-r") + 1])
if '-R' in sys.argv:
	num_reps = int(sys.argv[sys.argv.index("-R") + 1])

# Here we gotta copy over all of the tests from Gheith's directory. The names of all of the files we need to copy are in the 'tests' list
# For some reason this command won't work with the wildcard selector, so we have to grab each test manually :/
# @TODO: Fix this so that we can cp all of the tests with one call
# For now, we just have a big loop that runs through each test, grabs the output, and tells us whether we failed or not.
for test in tests:
	out = subprocess.Popen(['cp', gheith_project_path + '/' + test, '.'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output, err = out.communicate()
	if(err):
		print("Error copying test " + test + ": " + err)
		break

# Now that we're here, we have our test files downloaded, and we can run our stuff. We have both cc files and ok files in our list, so we only run half of them, it's easier than filtering the list
# I probably could have condensed both of these loops, but there was weird behavior where it would try to test the file before it was fully downloaded, and it was weird
for i in range (0, num_reps):
	print("\nTesting Round " + str(i + 1) + "\n")
	for test in tests:
		if test[-1] is 'c':
			# We run 'make clean -s <test>.result' and write the output to the console
			out = subprocess.Popen(['make', 'clean', '-s', test[0:test.index('.')] + ".result"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			output, err = out.communicate()
			if(err):
				print("Error copying test " + test + ": " + err)
				break
			# Track a fail/pass
			if "fail" in output:
				tests_failed += 1
				# We keep track of the specific test that failed, as well as how many times each specific test was failed
				# This makes it really easy to see if you or the test have race conditions, because times failed will be less than the times run
				if test in failed_tests_list:
					failed_tests_list[test] = failed_tests_list[test] + 1
				else:
					failed_tests_list[test] = 1
				if "recipe for target" in output:
					print("--- " + test + " failed due to a syntax error in the test ---")
				else:
					sys.stdout.write(output)
			else:
				tests_passed += 1
				sys.stdout.write(output)


print("\n*** FINISHED ***\n")
print("Tests Passed: " + str(tests_passed))
print("Tests Failed: " + str(tests_failed) + "\n")
if tests_failed > 0:
	for test, num in failed_tests_list.items():
		print("Failed test " + test + " a total of " + str(num) + "/" + str(num_reps) + " times")

if(not save_tests):
	cleanup()

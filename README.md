# gheith-testing-script
Automates the testing of code for Professor Gheith's 429 and 439 classes by downloading all tests from the website and running them on a local machine.

## Description
This script will download all of the files currently on Gheith's website and test them on a local machine immediately, skipping the wait period to run tests on his server. 

## Usage
Using this thing is super easy. Just put it in the root directory of a project folder, like `cs439_sp19_p5` and type `python runTests.py`. It will see which directory you called it from and find the right tests to use. Easy. 

## Important
For this to work, you have to be running it in a file that hasn't been renamed. For instance, if the lab was cloned onto your computer as "cs439_sp19_<CSID>_p5", that's what the directory name has to be for the script to work.

## Optional Flags
There are a couple of things that you can do to use different functionality of the script. 
* `python runTests.py -s`
  * By default, the script will delete the tests when it is finished and leave your folder the way it was. If you use the `-s` flag, it will save the tests when you're done.
* `python runTests.py -c`
  * Alternately, if you have the tests saved on your machine and want to get rid of them, the `-c` flag will just clean up your directory without actually running the tests. However, this **WILL NOT** delete any test that is named with your UTCS ID, and it will not delete any of the default tests, like t0, t1, etc.
* `python runTests.py -r 10`
  * By default, the script runs the tests 1 time. If you use the `-r` flag with a value specified, like the example above, the script will take that value and run it that many times. In the example above, the script will loop through the tests 10 times.
### Note
You can combine the 'save' and 'repetition' flags, like `python runTests.py -s -r 10` and it will work. The only rule is that the value of repetitions has to go directly after the `-r`. Remember that if you call the script with the cleanup flag, `-c`, it will clean up your directory and immediately terminate, not testing anything.
  
## Disclaimer
I'm not sure if this will work on Docker machines, because it relies on having access the the ~Gheith folder that is on lab machines.

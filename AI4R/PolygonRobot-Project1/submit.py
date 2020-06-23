#  This script allows you to submit your code to the Udacity hosted autograder
#  for automated testing & grading.
#
#  NOTE: You MUST submit your code via the Canvas Assignment before the 
#  stated deadline to receive credit.
#
# The Udacity autograder is very similar to the testing_suite_full.py script
# which allows you to test your code, except it may have different test
# cases, and it also makes sure that you have not accidentually imported
# any modules that exist on your local machine but do not exist in the
# "official" testing environment.
#
# We encourage you to use the remote Udacity autorgrader via this submit
# script, in addition to testing your work locally.
#
# How to use the script:
# 1. `pip install nelson`   (See:  https://pypi.org/project/nelson/ ) 
# 2. If your account is setup with two-factor, follow the instructions here:
#     https://bonnie.udacity.com/auth_tokens/two_factor 
#     Note, you must be logged into bonnie before using the above URL or you
#     will receive a 404 error.
# 3. Create the files studentMain[1-4].py in the same directory
# 4. Run `python submit.py` from within the same directory

#
#


import argparse
from nelson.gtomscs import submit

def main():
  parser = argparse.ArgumentParser(description='submits test code to the helloworld test quiz.')
  parser.add_argument('--environment', default='production', help="webserver environment")
  parser.add_argument('--id_provider', default='gt', help="identity provider (gt for OMSCS TAs)")
  parser.add_argument('--jwt_path', default=None, help="path to file containing auth information")

  args = parser.parse_args()

  course = 'cs8803-01'
  quiz = 'polygonrobot'
  filenames = ['studentMain1.py', 'studentMain2.py', 'studentMain3.py', 'studentMain4.py']

  submit(course,
         quiz,
         filenames,
         environment = args.environment,
         id_provider = args.id_provider,
         jwt_path = args.jwt_path)

if __name__ == '__main__':
    main()

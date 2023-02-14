import re


class TestPlan:
    '''
    TestPlan class that contians a test plan.  A test plan is basicly a lists of unit tests that can be run in a sequental order
    test should have an assertion
    '''
    def __init__(self,insurments=None):
        if type(insurments) == 'list':
            self._insurment = insurments # make a list of insturments
        else:
            self._insurment = [insurments]
        pass

    def _setup(self):
        '''
            private helper for running setup
            ... if it exsists, otherwise just run something else usefull if needed
        '''
        if 'setup' in dir(self):
            self.setup()
        else:
            pass # TODO: add some defult test setup stuff

    def _findTestMethods(self):
        '''
            private method for finding lists of test function names 
        '''
        #validMethodRegEx = r'[\_][^_]*$'
        validMethodRegEx = r'[\_][^_][0-9]{2}'
        # iterate through all the methods and see if they match with our search regex 
        for method in dir(self):
            match = re.search(validMethodRegEx,method)
            if match is not None:
                try:
                    getattr(self,method)()
                except:
                    print("failed to run a test")


    def run(self):
        '''
        run will iterate through all the test_### methods and find all the test in sequntal order
        '''
        self._setup()
        testMethods = self._findTestMethods() # get a list of test methods 

        pass

    def sayHi(self):
        print("HI there!")


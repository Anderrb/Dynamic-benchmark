import unittest
from quick.application.parallel.TaskQueue import MultilevelFeedbackQueue

class TestMultilevelFeedBackQueue(unittest.TestCase):
    class setUp(object):
        self.queue = MultilevelFeedbackQueue()
        
    class tearDown(object):
        pass
    
    class testInsertion():
        pass

if __name__ == '__main__':
    unittest.main()
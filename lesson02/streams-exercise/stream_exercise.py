class StreamProcessor(object):

    def __init__(self, stream):
        self._stream = stream

    def process(self):
        """
        :return: int
        """

        count = 0
        total = 0

        while count < 10 and total < 200:
            digits = self._stream.read(2)
            if len(digits) < 2:
                break

            count += 1

            n = int(digits)
            total += n

        return count
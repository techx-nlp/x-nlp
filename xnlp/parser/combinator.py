from typing import List


class Parser:
    """
    An interface for all parser combinators.
    """

    def parse(self, content: str) -> List[str]:
        raise NotImplementedError
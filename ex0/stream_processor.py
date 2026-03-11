#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  stream_processor.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/11 08:29:09 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/11 13:52:46 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataProcessor(ABC):

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):

    def process(self, data: Any) -> str:

        sumt = sum(data)
        avg = sumt / len(data)
        rst = (f"Processed {len(data)} numeric values, sum={sumt}"
               f", avg={avg}")
        return self.format_output(rst)

    def validate(self, data: Any) -> bool:
        for i in range(len(data)):
            try:
                int(data[i])
            except ValueError as e:
                print(f"{e}\nn is not an (int): {data[i]} [KO]")
                return False
        print("Validation: Numeric data verified")
        return True

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


def main():
    rst = NumericProcessor().process([1, 2, 3, 4, 5])
    print(rst)


if __name__ == "__main__":
    main()

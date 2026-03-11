#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  stream_processor.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/11 08:29:09 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/11 18:43:04 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any


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
               f", avg={avg:.2f}")
        return self.format_output(rst)

    def validate(self, data: Any) -> bool:

        for i in range(len(data)):
            try:
                isinstance(data[i], (int, float))
            except ValueError as e:
                print(f"{e} [KO]")
                return False
        return True

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):

    def process(self, data: Any) -> str:

        try:
            list_word = data.split()
        except AttributeError as e:
            print(e)

        nb_c = len(data)
        nb_word = len(list_word)
        rst = (f"Processed text: {nb_c} characters, {nb_word} words")
        return self.format_output(rst)

    def validate(self, data: any) -> bool:

        try:
            _ = data.split()
        except (AttributeError) as e:
            print(f"{e} [KO]")
            return False
        return True

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


def main():

    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("\nInitializing Numeric Processor...")

    num = [1, 2, 3, 4, 5]
    proc = NumericProcessor()

    if proc.validate(num):
        print(f"Processing data: {num}")
        print("Validation: Numeric data verified")
        print(proc.process(num))

    print("\nInitializing Text Processor...")

    s = 42
    proc = TextProcessor()

    if proc.validate(s):
        print(f"Processing data: {s}")
        print("Validation: Text data verified")
        print(proc.process(s))


if __name__ == "__main__":
    main()

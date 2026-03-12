#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  stream_processor.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/11 08:29:09 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/12 10:57:26 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if len(data) <= 0:
            return False

        for i in range(len(data)):
            if isinstance(data[i], (int, float)) is False:
                return False
        return True

    def process(self, data: Any) -> str:

        sumt = sum(data)
        avg = sumt / len(data)
        rst = (f"Processed {len(data)} numeric values, sum={sumt}"
               f", avg={avg:.2f}")
        return self.format_output(rst)

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:

        try:
            list_word = data.split()
        except AttributeError as e:
            print(f"{e} def process [KO]")

        nb_c = len(data)
        nb_word = len(list_word)
        rst = (f"Processed text: {nb_c} characters, {nb_word} words")
        return self.format_output(rst)

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:

        try:
            log = data.split(':')
        except AttributeError as e:
            print(f"{e} def process [KO]")

        s1 = log[0]
        s2 = log[1]

        if s1 == "ERROR":
            prefix = "[ALERT]"
        else:
            prefix = "[INFO]"
        rst = (f"{prefix} {s1} level detected:{s2}")
        return self.format_output(rst)

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


def main():

    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("\nInitializing Numeric Processor...")

    num = [1, 2, 3, 4, 5]
    proc = NumericProcessor()
    try:
        if proc.validate(num):
            print(f"Processing data: {num}")
            print("Validation: Numeric data verified")
            print(proc.process(num))
    except TypeError as e:
        print(f"{e} Valueprocess [KO]")

    print("\nInitializing Text Processor...")

    s = "Hello Nexus World"
    proc = TextProcessor()
    try:
        if proc.validate(s):
            print(f"Processing data: {s}")
            print("Validation: Text data verified")
            print(proc.process(s))
    except AttributeError as e:
        print(f"{e}Textprocess [KO]")

    print("\nInitializing Log Processor...")

    s = "ERROR: Connection timeout"
    proc = LogProcessor()
    try:
        if proc.validate(s):
            print(f"Processing data: {s}")
            print("Validation: Log entry verified")
            print(proc.process(s))
    except AttributeError as e:
        print(f"{e} Logprocess [KO]")

    print("\n=== Polymorphic Processing Demo ===")

    proc = (NumericProcessor(), TextProcessor(), LogProcessor())
    data = ([1, 2, 3], "hello world", "INFO: System ready")
    x = zip(proc, data)

    try:

        for i, (p, d) in enumerate(x):
            if p.validate(d):
                result = p.process(d)
                print(f"Result {i+1}: {result}")
    except (TypeError, AttributeError) as e:
        print(f"{e} Polyprocess")


if __name__ == "__main__":
    main()

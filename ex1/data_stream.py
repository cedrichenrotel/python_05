#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 11:26:07 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/12 18:38:28 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Environmental Data"
        self.temp = 0.0
        self.len_tab = 0

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        self.len_tab = len(data_batch)

        for i in range(self.len_tab):
            data = data_batch[i].split(':')
            if data[0] == 'temp':
                self.temp = float(data[1])

        return (f"Sensor analysis: {len(data_batch)} readings "
                f"processed, avg temp: {self.temp}°C")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        lst_err = []
        for i in range(self.len_tab):
            data = data_batch[i].split(':')
            if data[0] == 'temp':
                self.temp = float(data[1])

        if self.temp >= 100:
            lst_err.append(self.temp)

        return lst_err

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"type": self.type, "temp": self.temp, "len_tab": self.len_tab}


def main() -> None:

    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print("\nInitializing Sensor Stream...")

    stream_id = "SENSOR_001"
    capteur = ["temp:22.5", "humidity:65", "pressure:1013"]
    proc = SensorStream(stream_id)
    print(f"Processing sensor batch: [{', '.join(capteur)}]")
    print(proc.process_batch(capteur))


if __name__ == "__main__":
    main()

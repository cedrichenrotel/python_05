#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 11:26:07 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/13 19:44:26 by cehenrot        ###   ########.fr        #
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
        self.lst_err: list[Any] = []

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        self.len_tab = len(data_batch)

        for i in data_batch:
            try:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if data[0] == 'temp':
                        self.temp = float(data[1])
            except ValueError as e:
                print(f"Error process_batch : {e}")

        return (f"Sensor analysis: {self.len_tab} readings "
                f"processed, avg temp: {self.temp}°C")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        error = []
        limittemperature = float(criteria) if criteria else 100.0

        for i in data_batch:
            try:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if (data[0] == 'temp' and float(data[1]) >=
                            limittemperature):
                        error.append(i)
                        self.lst_err.append(i)
            except ValueError as e:
                print(f"Error filter_data: {e}")
        return error

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
                "type": self.type,
                "temp": self.temp,
                "len_tab": self.len_tab,
                "number error": len(self.lst_err)
                }


class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Financial Data"
        self.nb_sell = 0
        self.lst_err: list[Any] = []
        self.nb_transaction = 0
        self.sum_total = 0

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        total = 0

        for i in data_batch:
            try:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if data[0] == "buy":
                        total += int(data[1])
                    elif data[0] == "sell":
                        total -= int(data[1])
                        self.nb_sell += 1
            except ValueError as e:
                print(f"Error process_batch: {e}")

        if total > 0:
            sign = '+'
        else:
            sign = ''

        return (f"Transaction analysis: {len(data_batch)} operations, net "
                f"flow: {sign}{total} units")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:

        error = []
        total = 0
        accountneg = int(criteria) if criteria else 0

        for i in data_batch:
            try:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if data[0] == "buy":
                        total += int(data[1])
                    elif data[0] == "sell":
                        total -= int(data[1])
                        self.nb_sell += 1
            except ValueError as e:
                print(f"Error filter_data: {e}")
        if total <= accountneg:
            error.append(total)
            self.lst_err.append(f"Flow Alert: {total}")
        self.nb_transaction = len(data_batch)
        self.sum_total = total
        return error

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
                "type": self.type,
                "number sell": self.nb_sell,
                "number transaction": self.nb_transaction,
                "total sum": self.sum_total,
                "number error": len(self.lst_err)
                }


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "System Events"
        self.lst_err: list[Any] = []
        self.len_tab = 0

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        total_err = 0
        self.len_tab = len(data_batch)

        for i in data_batch:
            try:
                if i == 'error':
                    total_err += 1
            except TypeError as e:
                print(f"Error process_batch: {e}")

        return (f"Event analysis: {self.len_tab} events, {total_err} error "
                "detected")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:

        rst = []
        target = criteria if criteria else "error"
        for i in data_batch:
            if i == target:
                rst.append(i)
            if i == "error":
                self.lst_err.append(target)
        return rst

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "type": self.type,
            "len_tab": self.len_tab,
            "number error": len(self.lst_err)
                }


def main() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    
    print("Initializing Sensor Stream...")
    s = SensorStream("SENSOR_001")
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    print(s.process_batch(["temp:22.5", "humidity:65", "pressure:1013"]))

    print("\nInitializing Transaction Stream...")
    t = TransactionStream("TRANS_001")
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    print(t.process_batch(["buy:100", "sell:150", "buy:75"]))

    print("\nInitializing Event Stream...")
    e = EventStream("EVENT_001")
    print("Processing event batch: [login, error, logout]")
    print(e.process_batch(["login", "error", "logout"]))

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")

    streams: List[DataStream] = [s, t, e]

    payloads = [
        ["temp:22.5", "temp:25.0"],
        ["buy:50", "sell:20", "buy:10", "buy:5"],
        ["login", "error", "logout"]
    ]

    print("\nBatch 1 Results:")
    for i, stream in enumerate(streams):
        stream.process_batch(payloads[i])

        if "Environmental" in stream.type:
            name, unit, count = "Sensor", "readings", stream.len_tab
        elif "Financial" in stream.type:
            name, unit, count = "Transaction", "operations", stream.nb_transaction
        else:
            name, unit, count = "Event", "events", stream.len_tab

        print(f"- {name} data: {count} {unit} processed")

    print("Stream filtering active: High-priority data only")

    f_sensor = s.filter_data(["temp:110", "temp:120"], "100")
    f_trans = t.filter_data(["buy:1000"], "500")
    
    print(f"Filtered results: {len(f_sensor)} critical sensor alerts, "
          f"{len(f_trans)} large transaction")

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()

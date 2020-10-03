import os

from .exceptions import TDSRuntimeError, TDSValueError
from .helpers import get_temp_file_path
from .processors import processors_dict


class Loader:

    def __init__(self, config: dict, input_file: str, output_file: str):
        self.config = config
        self.input_file = input_file
        self.output_file = output_file

        self.previous_temp_file = None

    def file_processing(self, stage: str):
        # TODO: tqdm + logger
        for processor_name in self.config[stage]:
            processor = processors_dict[processor_name]()

            temp_file_path = get_temp_file_path(self.config)
            try:
                result = processor.process_file(self.input_file, temp_file_path)
            except OSError as e:
                # TODO: logging
                os.remove(temp_file_path)
                raise e

            if not result:
                raise TDSRuntimeError(f'After "{stage}" stage by "{processor_name}" processor result file is empty')

            # TODO: log lines count

            self._remove_previous_temp(temp_file_path)
            self.input_file = temp_file_path

    def line_processing(self):
        processors = []
        for processor_data in self.config['PROCESSING']:
            params = {}
            if isinstance(processor_data, dict):
                # HACK: processor with parameters for __init__
                processor_name = list(processor_data)[0]
                params = processor_data[processor_name]
            elif isinstance(processor_data, str):
                processor_name = processor_data
            else:
                # TODO: own exceptions
                raise TDSValueError(f'Wrong processor: {processor_data}')

            processor = processors_dict[processor_name](**params)
            processors.append(processor)

        temp_file_path = get_temp_file_path(self.config)

        # TODO: codecs?
        with open(self.input_file, encoding='utf-8') as fdr, open(temp_file_path, 'w', encoding='utf-8') as fdw:
            # TODO: tqdm + logger.debug
            for line in fdr:
                if not line:
                    continue

                for processor in processors:
                    line = processor.process_line(line)
                    # TODO: log processed line
                    if not line:    # empty or is None
                        break

                # save after all processors
                if line:    # not empty and is not None
                    fdw.write(line + '\n')

        # TODO: check need remove old input_file
        self.input_file = temp_file_path

    def finish(self):
        # FIXME: find another way
        os.rename(self.input_file, self.output_file)

    def _remove_previous_temp(self, new_temp_file_path: str = None):
        if self.previous_temp_file:
            os.remove(self.previous_temp_file)

        if new_temp_file_path is not None:
            self.previous_temp_file = new_temp_file_path

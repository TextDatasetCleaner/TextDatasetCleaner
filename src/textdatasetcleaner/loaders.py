import os
import tempfile

from .processors import processors_dict


class Loader:

    def __init__(self, config: dict, input_file: str, output_file: str):
        self.config = config
        self.input_file = input_file
        self.output_file = output_file

        self.previous_temp_file = None

    def pre_processing(self):
        # TODO: tqdm + logger
        for processor_name in self.config['PRE_PROCESSORS']:
            processor = processors_dict[processor_name]()

            _, temp_file_path = tempfile.mkstemp()
            try:
                result = processor.process_file(self.input_file, temp_file_path)
            except OSError as e:
                # TODO: logging
                os.remove(temp_file_path)
                raise e

            if not result:
                raise RuntimeError(f'After pre-processing by {processor_name} result file is empty')

            self._remove_previuos_temp(temp_file_path)
            self.input_file = temp_file_path

        # after last execution remove previous file
        self._remove_previuos_temp()

    def _remove_previuos_temp(self, new_temp_file_path: str = None):
        if self.previous_temp_file:
            os.remove(self.previous_temp_file)

        if new_temp_file_path is not None:
            self.previous_temp_file = new_temp_file_path

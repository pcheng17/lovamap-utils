import io
import itertools
import os
import sys
import threading
import time
import matlab.engine

VALID_INPUT_FILES = ['.json', '.dat']

bar = [
    "[=       ]",
    "[ =      ]",
    "[  =     ]",
    "[   =    ]",
    "[    =   ]",
    "[     =  ]",
    "[      = ]",
    "[       =]",
    "[      = ]",
    "[     =  ]",
    "[    =   ]",
    "[   =    ]",
    "[  =     ]",
    "[ =      ]",
]

class WaitAnimation:
    def __init__(self):
        self.work_title = ''
        self.thread = None
        self.running = False
        return

    def start(self, work_title: str):
        self.work_title = work_title
        self.thread = threading.Thread(target=self.animate)
        self.thread.daemon = True
        self.running = True
        self.thread.start()

    def animate(self):
        for c in itertools.cycle(bar):
            if not self.running:
                print("\r\033[K", end='')
                print(f'\r[Complete] {self.work_title}', end='\n')
                break
            print(f'\r{c} Running LOVAMAP on {self.work_title}', end='')
            time.sleep(0.1)

    def stop(self):
        self.running = False


""" def join_excel_files(dir_of_files: str, full_output_file: str):
    dfs = []
    for file in os.listdir(dir_of_files):
        # After the first _, before the extension, trucate if longer than 30
        dfs.append(pd.read_excel(io=file, sheet_name=''))

    with pd.ExcelWriter(full_output_file) as writer:
        for df in dfs:
            df.to_excel(writer, sheet_name='', index=False) """


if __name__ == '__main__':
    eng = matlab.engine.start_matlab()
    out = io.StringIO()

    dirs_of_species = os.path.abspath(sys.argv[1])
    # For each species of domains...
    for species in sorted(os.listdir(dirs_of_species)):
        dirpath1 = os.path.join(dirs_of_species, species)

        # We will dump all outputs of a species into a single directory
        output_path = os.path.join(dirpath1, "output")
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # For each domain type of that species...
        for domain_type in sorted(os.listdir(dirpath1)):
            if domain_type == 'output':
                continue

            dirpath2 = os.path.join(dirpath1, domain_type)

            # For each replicate of that domain type...
            for replicate in sorted(os.listdir(dirpath2)):
                if not replicate.endswith(tuple(VALID_INPUT_FILES)):
                    continue
                full_filename = os.path.join(dirpath2, replicate)

                wait = WaitAnimation()
                wait.start(full_filename)
                eng.run_lovamap_function(full_filename, domain_type, replicate, output_path, \
                    nargout=0, stdout=out)
                wait.stop()

        # Then, we create final sheet of each excel file and the one single big excel file.
        eng.organize_lovamap_data(output_path, species, nargout=0)

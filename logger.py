import logging
import os

import paths


def _setup_logger():
    log_path = os.path.join(paths.get_app_dir(), 'virtual_scaler.log')
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    )
    return logging.getLogger('virtual_scaler')


logger = _setup_logger()

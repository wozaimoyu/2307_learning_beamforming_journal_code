
from pathlib import Path
import gzip
import pickle

import numpy as np
from keras.models import load_model

import src
from src.analysis.helpers.test_precoder_error_sweep import (
    test_precoder_error_sweep,
)
from src.data.calc_sum_rate import (
    calc_sum_rate,
)
from src.models.precoders.learned_precoder import get_learned_precoder_normalized


def test_sac_precoder_error_sweep(
        config: 'src.config.config.Config',
        model_path: Path,
        error_sweep_parameter: str,
        error_sweep_range: np.ndarray,
        monte_carlo_iterations: int,
) -> None:
    """Test the learned SAC precoder for a range of error configuration with monte carlo average."""

    def get_precoder_function_learned(
        config: 'src.config.config.Config',
        satellite_manager: 'src.data.satellite_manager.SatelliteManager',
    ):

        state = config.config_learner.get_state(
            satellite_manager=satellite_manager,
            norm_factors=norm_factors,
            **config.config_learner.get_state_args
        )

        w_precoder_normalized = get_learned_precoder_normalized(
            state=state,
            precoder_network=precoder_network,
            **config.learned_precoder_args,
        )

        return w_precoder_normalized

    precoder_network = load_model(model_path)

    with gzip.open(Path(model_path, '..', 'config', 'norm_dict.gzip')) as file:
        norm_dict = pickle.load(file)
    norm_factors = norm_dict['norm_factors']

    test_precoder_error_sweep(
        config=config,
        error_sweep_parameter=error_sweep_parameter,
        error_sweep_range=error_sweep_range,
        precoder_name='learned',
        monte_carlo_iterations=monte_carlo_iterations,
        get_precoder_func=get_precoder_function_learned,
        calc_sum_rate_func=calc_sum_rate,
    )

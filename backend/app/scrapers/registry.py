from .mad_lab import scrape_mad_lab
from .pr_lab import scrape_pr_lab
from .lstm_lab import scrape_lstm_lab
from .chair_auto_control import scrape_chair_auto_control
from .asm_lab import scrape_asm_lab
from .i_meet_lab import scrape_i_meet
from .chair_info_sys_1 import scrape_information_systems
from .dds_lab import scrape_dds_lab
from .lhft_lab import scrape_lhft_lab
from .nhr_lab import scrape_nhr_lab
from .like_lab import scrape_like_lab


# Register scraper functions here, keyed by lab name.
SCRAPER_REGISTRY = {
    "MAD": scrape_mad_lab,
    "PR": scrape_pr_lab,
    "LSTM": scrape_lstm_lab,
    "AC": scrape_chair_auto_control,
    "ASM": scrape_asm_lab,
    "I-Meet": scrape_i_meet,
    "IIVC": scrape_information_systems,
    "DDS": scrape_dds_lab,
    "LHFT": scrape_lhft_lab,
    "NHR": scrape_nhr_lab,
    "LIKE": scrape_like_lab


}


# Function to retrieve scraper function by lab name.
def get_scraper_func(lab_name: str):
    return SCRAPER_REGISTRY.get(lab_name)

# Code inspired by https://github.com/tamarott/SinGAN
from train import train
from mario.tokens import REPLACE_TOKENS as MARIO_REPLACE_TOKENS
from mario.special_mario_downsampling import special_mario_downsampling
from mario.level_utils import read_level, read_level_from_file
from config import get_arguments, post_config
from loguru import logger
import wandb
import sys
import torch


def get_tags(opt):
    """ Get Tags for logging from input name. Helpful for wandb. """
    return [opt.input_name.split(".")[0]]


def main():
    """ Main Training funtion. Parses inputs, inits logger, trains, and then generates some samples. """

    # torch.autograd.set_detect_anomaly(True)

    # Logger init
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                      + "<level>{level}</level> | "
                      + "<light-black>{file.path}:{line}</light-black> | "
                      + "{message}")

    # Parse arguments
    opt = get_arguments().parse_args()
    opt = post_config(opt)

    # Init wandb
    run = wandb.init(project="mario", tags=get_tags(opt),
                     config=opt, dir=opt.out)
    opt.out_ = run.dir

    # Init game specific inputs
    replace_tokens = {}
    sprite_path = opt.game + '/sprites'
    if opt.game == 'mario':
        replace_tokens = MARIO_REPLACE_TOKENS
        downsample = special_mario_downsampling
    elif opt.game == 'mariokart':
        replace_tokens = MARIOKART_REPLACE_TOKENS
        downsample = special_mariokart_downsampling
    else:
        NameError("name of --game not recognized. Supported: mario, mariokart")

    # Read level according to input arguments
    real = read_level(opt, None, replace_tokens).to(opt.device)

    # Train!
    generators, noise_maps, reals, noise_amplitudes = train(real, opt)

if __name__ == "__main__":
    main()

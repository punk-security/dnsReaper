import colorama
import argparse
from os import linesep, environ
import sys

import providers
import inspect

runtime = environ.get("SM_COMMAND", f"{sys.argv[0]}")

banner = """\
          ____              __   _____                      _ __       
         / __ \__  ______  / /__/ ___/___  _______  _______(_) /___  __
        / /_/ / / / / __ \/ //_/\__ \/ _ \/ ___/ / / / ___/ / __/ / / /
       / ____/ /_/ / / / / ,<  ___/ /  __/ /__/ /_/ / /  / / /_/ /_/ / 
      /_/    \__,_/_/ /_/_/|_|/____/\___/\___/\__,_/_/  /_/\__/\__, /  
                                             PRESENTS         /____/
                              DNS Reaper ☠️

             Scan all your DNS records for subdomain takeovers!
        """

banner_with_colour = (
    colorama.Fore.GREEN
    + """\
          ____              __   _____                      _ __       
         / __ \__  ______  / /__/ ___/___  _______  _______(_) /___  __
        / /_/ / / / / __ \/ //_/\__ \/ _ \/ ___/ / / / ___/ / __/ / / /
       / ____/ /_/ / / / / ,<  ___/ /  __/ /__/ /_/ / /  / / /_/ /_/ / 
      /_/    \__,_/_/ /_/_/|_|/____/\___/\___/\__,_/_/  /_/\__/\__, /  
                                             PRESENTS         /____/"""
    + colorama.Fore.RED
    + """  
                              DNS Reaper ☠️"""
    + colorama.Fore.CYAN
    + """

             Scan all your DNS records for subdomain takeovers!
        """
    + colorama.Fore.RESET
)


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stdout.write(f" ❌ error: {message}{linesep}{linesep}")
        self.print_usage()
        sys.exit(2)


parser = CustomParser(
    usage=f"""
{runtime} provider [options] 

output:
  findings output to screen and (by default) results.csv 

help:
{runtime} --help

providers:
{ linesep.join([f"  > {provider} - {getattr(providers, provider).description}" for provider in providers.__all__ ]) }
""",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="",
    add_help=False
)

parser.add_argument(
    "provider",
    type=str,
    choices=providers.__all__,
)

for provider in providers.__all__:
    group = parser.add_argument_group(provider)
    module = getattr(providers, provider)
    group.description = module.description
    for arg in inspect.getfullargspec(module.fetch_domains)[0]:
        group.add_argument(
            f"--{arg.replace('_','-')}",
            type=str,
        )

parser.add_argument(
    "-h",
    "--help",
    action='help',
    help="Show this help message and exit",
)

parser.add_argument(
    "--out",
    type=str,
    default="results",
    help="Output file (default: %(default)s) - use 'stdout' to stream out",
)

parser.add_argument(
    "--out-format",
    type=str,
    default="csv",
    choices=["csv", "json"],
)

parser.add_argument(
    "--parallelism",
    type=int,
    default=30,
    help="Number of domains to test in parallel - too high and you may see odd DNS results (default: %(default)s)",
)

parser.add_argument(
    "--disable-probable",
    action="store_true",
    help="Do not check for probable conditions",
)

parser.add_argument(
    "--enable-unlikely",
    action="store_true",
    help="Check for more conditions, but with a high false positive rate",
)

parser.add_argument(
    "--signature",
    action="append",
    help="Only scan with this signature (multiple accepted)",
)

parser.add_argument(
    "--exclude-signature",
    action="append",
    help="Do not scan with this signature (multiple accepted)",
)

parser.add_argument(
    "--pipeline",
    action="store_true",
    help="Exit Non-Zero on detection (used to fail a pipeline)",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="-v for verbose, -vv for extra verbose",
)

parser.add_argument("--nocolour", help="Turns off coloured text", action="store_true")


def parse_args():
    args = parser.parse_args()
    module = getattr(providers, args.provider)
    for arg in inspect.getfullargspec(module.fetch_domains)[0]:
        if args.__dict__[arg] == None:
            parser.error(f" {args.provider} provider requires --{arg.replace('_','-')}")
    return args

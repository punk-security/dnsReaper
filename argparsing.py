import argparse
from os import linesep, environ
import sys

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


class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stdout.write(f" ❌ error: {message}{linesep}{linesep}")
        self.print_usage()
        sys.exit(2)


providers = ["file", "stdin", "aws", "azure", "cloudflare"]

parser = CustomParser(
    usage=f"{linesep} {runtime} {{ {'/'.join(providers) }}} [options] {linesep}",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="",
)

parser.add_argument(
    "provider",
    type=str,
    choices=providers,
)

file_group = parser.add_argument_group("file")
file_group.add_argument(
    "--filename", type=str, help="filename containing domains, one per line"
)

aws_group = parser.add_argument_group("aws")
aws_group.add_argument("--aws-access-key-id")
aws_group.add_argument("--aws-access-key-secret")

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
    "--disable-unlikely",
    action="store_true",
    help="Do not check for unlikely conditions",
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


def parse_args():
    args = parser.parse_args()
    if "file" == args.provider and (args.filename is None):
        parser.error("file inputs requires --filename")

    if "aws" == args.provider and (
        args.aws_access_key_id is None or args.aws_access_key_secret is None
    ):
        parser.error("aws requires --aws-access_key_id and --aws-access_key_secret")

    return args

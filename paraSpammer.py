"""
   _ (`-.    ('-.     _  .-')     ('-.      .-')     _ (`-.    ('-.     _   .-')    _   .-')       ('-.  _  .-')   
  ( (OO  )  ( OO ).-.( \( -O )   ( OO ).-. ( OO ).  ( (OO  )  ( OO ).-.( '.( OO )_ ( '.( OO )_   _(  OO)( \( -O )  
 _.`     \  / . --. / ,------.   / . --. /(_)---\_)_.`     \  / . --. / ,--.   ,--.),--.   ,--.)(,------.,------.  
(__...--''  | \-.  \  |   /`. '  | \-.  \ /    _ |(__...--''  | \-.  \  |   `.'   | |   `.'   |  |  .---'|   /`. ' 
 |  /  | |.-'-'  |  | |  /  | |.-'-'  |  |\  :` `. |  /  | |.-'-'  |  | |         | |         |  |  |    |  /  | | 
 |  |_.' | \| |_.'  | |  |_.' | \| |_.'  | '..`''.)|  |_.' | \| |_.'  | |  |'.'|  | |  |'.'|  | (|  '--. |  |_.' | 
 |  .___.'  |  .-.  | |  .  '.'  |  .-.  |.-._)   \|  .___.'  |  .-.  | |  |   |  | |  |   |  |  |  .--' |  .  '.' 
 |  |       |  | |  | |  |\  \   |  | |  |\       /|  |       |  | |  | |  |   |  | |  |   |  |  |  `---.|  |\  \  
 `--'       `--' `--' `--' '--'  `--' `--' `-----' `--'       `--' `--' `--'   `--' `--'   `--'  `------'`--' '--' 

 Web URL parameter spammer
 ~ Wahalez

"""
import re
import os
import sys
import argparse
import urllib.request

ARG_N = 4
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36'

class ArgumentParserError(Exception): pass
class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def arg_init():
    ap = CustomArgumentParser(
        description='paraSpammer | Web url parameter spammer',
        prog=os.path.basename(__file__),
        allow_abbrev=False
    )

    ap._action_groups.pop()
    required = ap.add_argument_group('required arguments')
    optional = ap.add_argument_group('optional arguments')

    required.add_argument('-u', type=str, metavar="URL", action='store', nargs=1, required=True, help='Url of the website to spam. Must be surrounded by quotes.')
    required.add_argument('-p', type=str, metavar="PARAM", action='store', nargs=1, required=True, help='The parameter to spam.')
    required.add_argument('-r', type=str, metavar="REGEX", action='store', nargs=1, required=True, help='Regex expression to look for in the web page. If found, will save current iteration to a file of successful finds.')
    optional.add_argument('--min-iter', type=int, metavar='MIN', action='store', nargs=1, default=0, help="Minimum number to iterate from.")
    optional.add_argument('--max-iter', type=int, metavar='MAX', action='store', nargs=1, default=sys.maxsize, help="Maximum number to iterate to.")
    optional.add_argument('--cookie', type=str, metavar="COOKIE", action='store', nargs=1, default='', help='Custom cookie to be using.')
    return ap

def lookForRegex(pageContent, regex):
    pass

def openUrl(url, cookie):
    page = ''
    req = urllib.request.Request(url, headers={'User-Agent': user_agent,
                                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                               'Cookie': str(cookie)})
    with urllib.request.urlopen(req) as res:
        page = res.read()
        page = page.decode('utf-8')
    return page
    
def build_url(url, param, iter):
    return re.sub(str(param) + "=[a-zA-Z0-9\'\"\`+.-/:]*",
                  str(param) + "=" + str(iter),
                  url)

def spam(url, param, min_iter, max_iter, regex, cookie):
    success_search = []
    for iter in range(min_iter, max_iter):
        url_iter = build_url(url, param, iter)
        print("[Info] testing: " + url_iter)
        page = openUrl(url_iter, cookie)
        if bool(re.search(str(regex), page)):
            print("Found, adding iteration to success list.")
            success_search.append(iter)
    print('\n\n')
    if success_search:
        print("Successful searches found: ", end='')
        print('[%s]' % ', '.join(map(str, success_search)))
    else:
        print("No successful searches for the specified regex found.")

def main():
    ap = arg_init()
    try:
        args = ap.parse_args()
        url = args.u[0]; param = args.p[0]
        min_iter = args.min_iter[0] if isinstance(args.min_iter, list ) else int(args.min_iter)
        max_iter = args.max_iter[0] if isinstance(args.max_iter, list ) else int(args.max_iter)
        regex = args.r[0]; cookie = args.cookie[0]
        spam(url, param, min_iter, max_iter, regex, cookie)

    except ArgumentParserError as e:
        ap.print_help()
        print('\n')
        print(e)
        exit(2)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
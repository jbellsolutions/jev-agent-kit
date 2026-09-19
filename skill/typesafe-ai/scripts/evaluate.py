#!/usr/bin/env python3
"""Use the existing authenticated Super Browser connection; never calls TypeSafe directly."""
import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


def connection():
    values={}
    path=Path.home()/'.super-browser.env'
    if path.exists():
        for line in path.read_text().splitlines():
            key,sep,value=line.partition('=')
            if sep and key.strip() in ('SUPER_BROWSER_TOKEN','SUPER_BROWSER_URL'):
                values[key.strip()]=value.strip().strip('"\'')
    for key in ('SUPER_BROWSER_TOKEN','SUPER_BROWSER_URL'):
        if os.environ.get(key):values[key]=os.environ[key]
    if not values.get('SUPER_BROWSER_TOKEN'):raise ValueError('Missing Super Browser connection')
    base=urlsplit(values.get('SUPER_BROWSER_URL','https://superbrowser.online'))
    if base.scheme!='https' or not base.netloc or base.username or base.password:
        raise ValueError('Super Browser connection requires an HTTPS origin')
    return urlunsplit((base.scheme,base.netloc,'/mcp/','','')),values['SUPER_BROWSER_TOKEN']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--status',action='store_true',help='Inspect the shared budget without evaluating')
    args=parser.parse_args()
    try:
        url,token=connection()
        arguments={'operation':'typesafe_status','arguments':{}} if args.status else json.load(sys.stdin)
        name='advisor_manage' if args.status else 'typesafe_evaluate'
        body=json.dumps({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':name,'arguments':arguments}}).encode()
        request=Request(url,data=body,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json',
            'Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'})
        with urlopen(request,timeout=35) as response:data=json.load(response)
        result=data['result']
        if result.get('isError'):raise ValueError('Evaluation unavailable')
        value=json.loads(result['content'][0]['text'])
        print(json.dumps(value,ensure_ascii=False))
    except Exception:
        # Do not echo credentials, URLs, provider bodies or supplied source text.
        print(json.dumps({'status':'unavailable','reason':'super_browser_connection_or_request_failure',
            'advisory':True,'note':'Retry with the same request_id; never use a local TypeSafe key.'}))
        return 1
    return 0


if __name__=='__main__':raise SystemExit(main())

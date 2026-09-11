#!/usr/bin/env python3
"""Run frozen traces against oracle, candidates, and deliberate mutants."""
import csv, importlib.util, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(label,path):
    sys.path.insert(0,str(path.parent))
    spec=importlib.util.spec_from_file_location(label,path); m=importlib.util.module_from_spec(spec)
    sys.modules[label]=m; spec.loader.exec_module(m); return m
ORACLE=module('mission_oracle',ROOT/'oracle/protocol.py')
CANDIDATES={x:module('mission_'+x,ROOT/x/'protocol.py') for x in ('candidate_a','candidate_b','candidate_c')}
def norm(s):
    # Candidate layouts differ; retain only requirement-observable state.
    retry=s.get('retries',{})
    outstanding=s.get('outstanding')
    return {'state':s['state'],'session_id':s.get('session_id',s.get('sid')),
      'next_send':s.get('next_send',s.get('next_tx_seq',s.get('send_next'))),
      'expected_recv':s.get('expected_recv',s.get('expected_rx_seq',s.get('recv_expected'))),
      'last_delivered':s.get('last_delivered',s.get('last_delivered_seq')),
      'last_acked':s.get('last_acked',s.get('last_acked_seq')),
      'outstanding':None if outstanding is None else {'seq':outstanding['seq'],'payload_id':outstanding.get('payload_id')},
      'open_retries':s.get('open_retries',retry.get('open_timer',0)),
      'data_retries':s.get('data_retries',retry.get('data_timer',outstanding.get('retries',0) if outstanding else 0)),
      'close_retries':s.get('close_retries',retry.get('close_timer',0))}
def run_api(api,events):
    st=api.initial(); rows=[]
    for i,e in enumerate(events):
        r=api.step(st,e); st=r['snapshot']
        actions=r.get('actions',[])
        flattened=' '.join(str(x).lower() for x in actions)
        delivered=('deliver_data' in flattened or 'data_delivered' in flattened)
        rows.append((r['valid'],norm(st),delivered))
    return rows
def traces():
    out=[('design',x) for x in json.loads((ROOT/'design_traces/traces.json').read_text())]
    out += [('mutation_probe',x) for x in json.loads((ROOT/'design_traces/mutation_probes.json').read_text())]
    out += [('held_out',json.loads(p.read_text())) for p in sorted((ROOT/'held_out_traces').glob('*.json'))]
    return out
def compare(api, corpus):
    failures=[]
    for group,t in corpus:
        expected=run_api(ORACLE,t['events']); actual=run_api(api,t['events'])
        for n,(a,b) in enumerate(zip(expected,actual),1):
            if a!=b: failures.append({'group':group,'trace':t['name'],'event_index':n,'oracle_valid':a[0],'candidate_valid':b[0],'oracle_state':a[1],'candidate_state':b[1],'oracle_delivered':a[2],'candidate_delivered':b[2]});break
    return failures
def main():
    corpus=traces(); report={'candidates':{}}
    for name,api in CANDIDATES.items(): report['candidates'][name]=compare(api,corpus)
    # Mutants use their own class state API and the frozen corpus.
    sys.path.insert(0,str(ROOT)); from mutants.mutants import MUTANTS
    mutation=[]
    for ident,cls in MUTANTS.items():
        class Adapter:
            @staticmethod
            def initial(): return cls().snapshot()
            @staticmethod
            def step(state,event):
                p=cls.from_snapshot(state); return p.step(event)
        failures=compare(Adapter,corpus)
        mutation.append({'MUTANT_ID':ident,'KILLED':bool(failures),'FIRST_KILL':(failures[0]['group']+'/'+failures[0]['trace'] if failures else ''),'SURVIVOR_REASON':'' if failures else 'No discriminating frozen trace'})
    (ROOT/'results/conformance.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    with (ROOT/'mutation_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=mutation[0].keys());w.writeheader();w.writerows(mutation)
    print(json.dumps({'candidate_failures':{n:len(v) for n,v in report['candidates'].items()},'mutants_killed':sum(x['KILLED'] for x in mutation),'mutants_total':len(mutation)},sort_keys=True))
    return 1 if any(report['candidates'].values()) or not all(x['KILLED'] for x in mutation) else 0
if __name__=='__main__': raise SystemExit(main())

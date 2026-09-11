"""Candidate C: declarative policy rules evaluated by event family."""
from copy import deepcopy
def initial(): return {"state":"IDLE","sid":None,"send_next":0,"outstanding":None,"last_acked":None,"recv_expected":0,"last_delivered":None,"open_retries":0,"close_retries":0}
def result(d,v,c,a=()):return {"valid":v,"code":c,"actions":list(a),"snapshot":deepcopy(d)}
def apply(before,e):
 d=deepcopy(before);s=d['state'];k=e.get('type');same=d['sid']==e.get('session_id')
 def no(c='invalid_event'):return result(before,False,c)
 rules={
  'OPEN_REQ':lambda: (no() if s!='IDLE' else no('invalid_session_id') if not isinstance(e.get('session_id'),int) or isinstance(e.get('session_id'),bool) or e['session_id']<=0 else (d.update(state='OPEN_SENT',sid=e['session_id'],open_retries=0) or result(d,True,'opened',('send_open','start_open_timer')))),
  'OPEN_ACK':lambda: (no() if s!='OPEN_SENT' else no('wrong_session') if not same else (d.update(state='OPEN',send_next=0,recv_expected=0,open_retries=0) or result(d,True,'open',('stop_open_timer',)))),
 }
 if k in rules:return rules[k]()
 if k=='DATA':
  q=e.get('seq');z=e.get('direction')
  if s!='OPEN':return no()
  if not same:return no('wrong_session')
  if not isinstance(q,int) or isinstance(q,bool) or q<0:return no('invalid_sequence')
  if z=='LOCAL':
   if d['outstanding'] is not None:return no('data_outstanding')
   if q!=d['send_next']:return no('unexpected_send_sequence')
   d['outstanding']={'seq':q,'payload_id':e.get('payload_id'),'retries':0};d['send_next']+=1;return result(d,True,'data_sent',('send_data','start_data_timer'))
  if z=='PEER':
   if q==d['recv_expected']:d['last_delivered']=q;d['recv_expected']+=1;return result(d,True,'data_delivered',('deliver_data','send_data_ack'))
   if q==d['recv_expected']-1:return result(d,True,'duplicate_data',('send_data_ack',))
   return no('out_of_order_data')
  return no('invalid_direction')
 if k=='DATA_ACK':
  if s!='OPEN':return no()
  if not same:return no('wrong_session')
  if d['outstanding'] and e.get('seq')==d['outstanding']['seq']:d['last_acked']=e['seq'];d['outstanding']=None;return result(d,True,'data_acked',('stop_data_timer',))
  return result(d,True,'duplicate_data_ack') if e.get('seq')==d['last_acked'] else no('future_or_unexpected_data_ack')
 if k=='CLOSE_REQ':
  if s!='OPEN':return no()
  if not same:return no('wrong_session')
  if d['outstanding'] is not None:return no('data_outstanding')
  d.update(state='CLOSE_SENT',close_retries=0);return result(d,True,'close_sent',('send_close','start_close_timer'))
 if k=='CLOSE_ACK':
  if s=='CLOSED' and same:return result(d,True,'duplicate_close_ack')
  if s!='CLOSE_SENT':return no()
  if not same:return no('wrong_session')
  d.update(state='CLOSED',close_retries=0);return result(d,True,'closed',('stop_close_timer',))
 if k=='ABORT':
  if s not in {'OPEN_SENT','OPEN','CLOSE_SENT'}:return no()
  d['state']='ABORTED';return result(d,True,'aborted',('stop_timers',))
 if k=='RESET':return result(initial(),True,'reset') if s in {'ABORTED','CLOSED'} else no()
 if k=='TIMEOUT':
  facts={'open_timer':('OPEN_SENT','open_retries',None,'open','send_open'),'data_timer':('OPEN','outstanding','retries','data','send_data'),'close_timer':('CLOSE_SENT','close_retries',None,'close','send_close')}.get(e.get('timer_name'))
  if not facts:return no()
  required,f,n,label,act=facts
  if s!=required or (n and not d[f]):return no()
  if n:d[f][n]+=1;cnt=d[f][n]
  else:d[f]+=1;cnt=d[f]
  if cnt>=3:d['state']='ABORTED';return result(d,True,label+'_timeout_abort',('stop_'+label+'_timer',))
  return result(d,True,label+'_retransmit',(act,'restart_'+label+'_timer'))
 return no()

def step(state,event):
 return apply(state,event)

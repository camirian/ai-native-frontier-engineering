"""Candidate A: explicit state/event guarded transition table."""
from copy import deepcopy
ACTIVE={"OPEN_SENT","OPEN","CLOSE_SENT"}
def initial(): return {"state":"IDLE","sid":None,"send_next":0,"outstanding":None,"last_acked":None,"recv_expected":0,"last_delivered":None,"open_retries":0,"close_retries":0}
def out(d,v,c,a=()): return {"valid":v,"code":c,"actions":list(a),"snapshot":deepcopy(d)}
def step(before,e):
 d=deepcopy(before);s=d["state"];k=e.get("type");same=e.get("session_id")==d["sid"]
 def bad(c="invalid_event"): return out(before,False,c)
 if (s,k)==("IDLE","OPEN_REQ"):
  x=e.get("session_id")
  if not isinstance(x,int) or isinstance(x,bool) or x<=0:return bad("invalid_session_id")
  d.update(state="OPEN_SENT",sid=x,open_retries=0);return out(d,True,"opened",("send_open","start_open_timer"))
 if (s,k)==("OPEN_SENT","OPEN_ACK"):
  if not same:return bad("wrong_session")
  d.update(state="OPEN",send_next=0,recv_expected=0,open_retries=0);return out(d,True,"open",("stop_open_timer",))
 if s=="OPEN" and k=="DATA":
  if not same:return bad("wrong_session")
  q=e.get("seq");z=e.get("direction")
  if not isinstance(q,int) or isinstance(q,bool) or q<0:return bad("invalid_sequence")
  if z=="LOCAL":
   if d["outstanding"] is not None:return bad("data_outstanding")
   if q!=d["send_next"]:return bad("unexpected_send_sequence")
   d["outstanding"]={"seq":q,"payload_id":e.get("payload_id"),"retries":0};d["send_next"]+=1;return out(d,True,"data_sent",("send_data","start_data_timer"))
  if z=="PEER":
   if q==d["recv_expected"]:d["last_delivered"]=q;d["recv_expected"]+=1;return out(d,True,"data_delivered",("deliver_data","send_data_ack"))
   if q==d["recv_expected"]-1:return out(d,True,"duplicate_data",("send_data_ack",))
   return bad("out_of_order_data")
  return bad("invalid_direction")
 if s=="OPEN" and k=="DATA_ACK":
  if not same:return bad("wrong_session")
  q=e.get("seq")
  if d["outstanding"] and q==d["outstanding"]["seq"]:d["last_acked"]=q;d["outstanding"]=None;return out(d,True,"data_acked",("stop_data_timer",))
  if q==d["last_acked"]:return out(d,True,"duplicate_data_ack")
  return bad("future_or_unexpected_data_ack")
 if (s,k)==("OPEN","CLOSE_REQ"):
  if not same:return bad("wrong_session")
  if d["outstanding"] is not None:return bad("data_outstanding")
  d.update(state="CLOSE_SENT",close_retries=0);return out(d,True,"close_sent",("send_close","start_close_timer"))
 if (s,k)==("CLOSE_SENT","CLOSE_ACK"):
  if not same:return bad("wrong_session")
  d.update(state="CLOSED",close_retries=0);return out(d,True,"closed",("stop_close_timer",))
 if s=="CLOSED" and k=="CLOSE_ACK" and same:return out(d,True,"duplicate_close_ack")
 if k=="ABORT" and s in ACTIVE:d["state"]="ABORTED";return out(d,True,"aborted",("stop_timers",))
 if k=="RESET" and s in {"ABORTED","CLOSED"}:return out(initial(),True,"reset")
 if k=="TIMEOUT":
  spec={"open_timer":("OPEN_SENT","open_retries",None,"open","send_open"),"data_timer":("OPEN","outstanding","retries","data","send_data"),"close_timer":("CLOSE_SENT","close_retries",None,"close","send_close")}.get(e.get("timer_name"))
  if not spec:return bad()
  required,f,n,label,act=spec
  if s!=required or (n and not d[f]):return bad()
  if n:d[f][n]+=1;count=d[f][n]
  else:d[f]+=1;count=d[f]
  if count>=3:d["state"]="ABORTED";return out(d,True,label+"_timeout_abort",("stop_"+label+"_timer",))
  return out(d,True,label+"_retransmit",(act,"restart_"+label+"_timer"))
 return bad()

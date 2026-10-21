#!/usr/bin/env python3
"""Build the marketplace git-flow page (one self-contained HTML file) from GitHub PR dumps plus the local git history.

usage: python3 scripts/git-flow/build.py [PRS1.json PRS2.json ...]

PRS*.json are the JSON arrays returned by the GitHub list_pull_requests tool (state=all, with `body`),
one file per page. With no files it reads the PRs itself with `gh api` (needs a working gh login
or a session with the repo attached). Output goes to $GITFLOW_OUT, default <tmpdir>/git-flow.html.
It fetches origin first and un-shallows the clone, because the fork points need full history.

Adapted from spanner-planner's scripts/git-flow (same template and graph code). This repo has no app,
no release branch and no database, so those parts are gone; areas are skills and plugins instead.
The SpannerSans font is read from a spanner-planner checkout ($SPANNER_FONT, default
~/Developer/spanner-planner/app/(os)/fonts/SpannerSans.woff2); without it the page falls back to system fonts."""
import json,subprocess,re,sys,base64,datetime,os,tempfile
from datetime import datetime as DT
here=os.path.dirname(os.path.abspath(__file__))
repo=subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True,cwd=here).stdout.strip()
tpl=os.path.join(here,'template.html')
font=os.environ.get('SPANNER_FONT') or os.path.expanduser('~/Developer/spanner-planner/app/(os)/fonts/SpannerSans.woff2')
slug=re.sub(r'(\.git)?$','',re.sub(r'^.*github\.com[:/]','',subprocess.run(['git','remote','get-url','origin'],capture_output=True,text=True,cwd=repo).stdout.strip()))
out=os.environ.get('GITFLOW_OUT') or os.path.join(tempfile.gettempdir(),'git-flow.html')
dumps=sys.argv[1:]
def sh(*a): return subprocess.run(a,capture_output=True,text=True,cwd=repo).stdout
ts=lambda s: DT.fromisoformat(s.replace('Z','+00:00'))
if subprocess.run(['git','rev-parse','--is-shallow-repository'],capture_output=True,text=True,cwd=repo).stdout.strip()=='true':
    subprocess.run(['git','fetch','--unshallow','origin'],cwd=repo,check=True)
subprocess.run(['git','fetch','origin','--prune'],cwd=repo,check=True)
prs={}
if dumps:
    for f in dumps:
        for p in json.load(open(f)): prs[p['number']]=p
else:
    page=1   # page by hand: --paginate follows Link headers that use numeric repo ids, which the proxy refuses
    while True:
        r=subprocess.run(['gh','api',f'repos/{slug}/pulls?state=all&per_page=100&page={page}'],capture_output=True,text=True,cwd=repo)
        if r.returncode: sys.exit('gh api failed: '+(r.stderr or r.stdout)[:500])
        batch=json.loads(r.stdout)
        for p in batch: prs[p['number']]=p
        if len(batch)<100: break
        page+=1
prs=sorted(prs.values(),key=lambda p:p['number'])
commits={}
for l in sh('git','log','--all','--date=iso-strict','--pretty=%H|%aI|%an|%P|%s').splitlines():
    H,d,a,P,s=l.split('|',4); commits[H]=dict(h=H[:7],d=d,a=a,P=P.split(),s=s)
short={c['h']:H for H,c in commits.items()}
# The commit graph, once, in memory. Everything that used to be one git call per PR or per branch
# (git log P0..P1, rev-list --count, merge-base --is-ancestor, rev-parse) is a bitmask lookup here.
order=list(commits)                      # git log --all order: newest first
idx={H:i for i,H in enumerate(order)}
anc={}
for root in order:                       # git log --all is date order, not topological: walk parents first (iterative DFS)
    if root in anc: continue
    stack=[root]
    while stack:
        H=stack[-1]
        if H in anc: stack.pop(); continue
        todo=[P for P in commits[H]['P'] if P in commits and P not in anc]
        if todo: stack.extend(todo); continue
        a=1<<idx[H]
        for P in commits[H]['P']:
            if P in anc: a|=anc[P]
        anc[H]=a; stack.pop()
def reach(H): return anc.get(H,0)
def rng(a,b):
    """git log a..b: commits reachable from b and not from a, in git log order."""
    m=reach(b)&~reach(a); out=[]
    while m:
        low=m&-m; out.append(order[low.bit_length()-1]); m^=low
    return out
def count(a,b): return bin(reach(b)&~reach(a)).count('1')
tips={}
for l in sh('git','for-each-ref','--format=%(objectname) %(refname:short)','refs/remotes/origin').splitlines():
    sha,ref=l.split(' ',1)
    if ref!='origin' and not ref.endswith('/HEAD'): tips[ref]=sha
SES=re.compile(r'claude\.ai/code/(session_[A-Za-z0-9]+)')
for rec in sh('git','log','--all','--format=%H%x1f%B%x1e').split('\x1e'):
    if '\x1f' not in rec: continue
    H,msg=rec.strip().split('\x1f',1)
    if H in commits:
        m=SES.search(msg); commits[H]['ss']=m.group(1) if m else None
merge={}
for H,c in commits.items():
    m=re.match(r'Merge pull request #(\d+)',c['s'])
    if m: merge[int(m.group(1))]=H
mainH=tips['origin/main']
# no release branch here: what ships is the org Skills Library upload, done by hand from main
relH=None
relset={H for H in order if relH and reach(relH)>>idx[H]&1}
fp=set(); _h=mainH
while _h in commits and _h not in fp:
    fp.add(_h); _h=(commits[_h]['P'] or [None])[0]
out_prs=[]
for p in prs:
    n=p['number']; cl=[]
    if n in merge and len(commits[merge[n]]['P'])==2:
        P=commits[merge[n]]['P']
        for h in rng(P[0],P[1]):
            c=commits[h]; cl.append(dict(h=c['h'],d=c['d'],a=c['a'],s=c['s'],ss=c.get('ss')))
    out_prs.append(dict(n=n,rel=bool(n in merge and merge[n] in relset),t=p['title'],ref=p['head']['ref'],base=p['base']['ref'],cr=p['created_at'],mg=p.get('merged_at'),cx=p.get('closed_at'),
        body=(p.get('body') or '').strip(),sessions=sorted({c['ss'] for c in cl if c.get('ss')}|set(SES.findall(p.get('body') or ''))|({commits[merge[n]].get('ss')} if n in merge and commits[merge[n]].get('ss') else set())),cowork=sum(1 for c in cl if c['a'].startswith('Claude (Cowork')),mc=commits[merge[n]]['h'] if n in merge else None,commits=cl,state=p['state']))
open_prs=[p for p in out_prs if p['state']=='open']
brs=[]
for b,tip in tips.items():
    name=b.replace('origin/','',1)
    if name=='main': continue
    c=commits[tip]
    ahead=count(mainH,tip); behind=count(tip,mainH); merged=ahead==0
    brs.append(dict(name=name,tip=tip[:7],d=c['d'],s=c['s'],merged=merged,ahead=ahead,behind=behind,prs=[p['n'] for p in out_prs if p['ref']==name]))
brnames={b['name'] for b in brs}
owner={}
for p in out_prs:
    for c in p['commits']: owner.setdefault(c['h'],[]).append(p['n'])
def fork_of(full):
    R=set(full); roots=[h for h in R if not commits[h]['P'] or commits[h]['P'][0] not in R]
    roots.sort(key=lambda h:commits[h]['d']); r=roots[0]; ps=commits[r]['P']
    return ps[0] if ps else None
byN={p['n']:p for p in out_prs}
for p in out_prs:
    cs=p['commits']; F=None; cd=[c['d'] for c in cs]
    if cs: F=fork_of([short[c['h']] for c in cs])
    elif p['ref'] in brnames:
        cl=rng(mainH,tips['origin/'+p['ref']])
        if cl: F=fork_of(cl); cd=[commits[h]['d'] for h in cl]
    par='main'; fh=None
    if F:
        fh=F[:7]
        if F not in fp:
            own=[x for x in owner.get(fh,[]) if x!=p['n']]
            par=own[-1] if own else 'main'
    if p['base']!='main':
        o=[q['n'] for q in out_prs if q['ref']==p['base']]; par=o[0] if o else 'main'
    first=min(cd,key=ts) if cd else None
    ft=min([x for x in [first,p['cr']] if x],key=ts)
    if isinstance(par,int):
        pm=byN[par]; pend=pm['mg'] or pm['cx']
        if pend and ts(pend)<ts(ft): par='main'   # parent already closed when this branched
    p['fk']=dict(par=par,F=fh,Fd=commits[F]['d'] if F else None,ft=ft)
ghost=[]
for b in brs:
    if not b['prs'] and not b['merged']:
        cl=[dict(h=commits[h]['h'],d=commits[h]['d'],a=commits[h]['a'],s=commits[h]['s']) for h in rng(mainH,tips['origin/'+b['name']])]
        ghost.append(dict(name=b['name'],tip=b['tip'],commits=cl,fk=dict(par='main',ft=min(c['d'] for c in cl))))
# ---- what changed: a type (branch prefix, then title, then files), the areas touched, and the size ----
# One git log --numstat for everything (merge commits list no files, so a PR is the sum of its own commits).
numstat={}; _cur=None
for l in sh('git','log','--all','--numstat','--format=@%H').splitlines():
    if l.startswith('@'): _cur=l[1:]; numstat[_cur]=[]
    elif l.strip() and _cur:
        parts=l.split('\t',2)
        if len(parts)==3: numstat[_cur].append((0 if parts[0]=='-' else int(parts[0]),0 if parts[1]=='-' else int(parts[1]),parts[2]))
squash={}
for H,c in commits.items():
    m=re.search(r'\(#(\d+)\)$',c['s'])
    if m: squash[int(m.group(1))]=H
PREFIX={'feat':'feat','feature':'feat','fix':'fix','bugfix':'fix','hotfix':'fix','docs':'docs','doc':'docs','chore':'chore','ci':'chore','build':'chore','deps':'chore',
        'skill':'skill','skills':'skill','brand':'skill','design':'design','refactor':'refactor','perf':'refactor','test':'test','tests':'test','schema':'db','db':'db','migration':'db'}
def area_of(path):
    # a skill's own name for anything under plugins/<plugin>/skills/<skill>/, else the plugin's name
    parts=path.split('/')
    if parts[0]=='plugins' and len(parts)>3 and parts[2]=='skills': return parts[3]
    if parts[0]=='plugins' and len(parts)>2: return parts[1]
    if parts[0] in ('scripts','docs'): return parts[0]
    if parts[0]=='.github': return 'ci'
    if parts[0]=='.claude-plugin': return 'config'
    if '/' not in path: return 'docs' if path.lower().endswith('.md') else 'config'
    return 'other'
def summarize(fulls):
    seen={}; ad=dl=0
    for H in fulls:
        for a,d,path in numstat.get(H,[]): seen[path]=1; ad+=a; dl+=d
    areas={}
    for path in seen: areas[area_of(path)]=areas.get(area_of(path),0)+1
    return dict(fs=len(seen),ad=ad,dl=dl,ar=sorted(areas.items(),key=lambda x:-x[1]),paths=list(seen))
def classify(ref,title,info):
    pre=re.split(r'[/_-]',ref.lower())[0]
    if pre in PREFIX: return PREFIX[pre]
    m=re.match(r'^(\w+)(\([^)]*\))?!?:',title.lower())
    if m and m.group(1) in PREFIX: return PREFIX[m.group(1)]
    w=re.split(r'\W+',title.lower().strip())[0] if title else ''
    if w in ('fix','fixes','fixed','bug','repair','correct','patch','revert'): return 'fix'
    if w in ('add','adds','build','create','implement','introduce','ship','new','start','wire','move','show','make','support','enable'): return 'feat'
    if w in ('docs','document','readme','runbook'): return 'docs'
    ar=dict(info['ar'])
    if info['fs'] and set(ar)<={'docs'}: return 'docs'
    if info['fs'] and set(ar)<={'scripts','ci','config'}: return 'chore'
    if info['fs'] and not set(ar)&{'docs','scripts','ci','config','other'}: return 'skill'   # only skill or plugin files
    return 'other'
for p in out_prs:
    if not p['rel'] and p['n'] in squash and squash[p['n']] in relset: p['rel']=True   # squash merges land as one ordinary commit
    if not p['rel'] and p['mg'] and tips.get('origin/'+p['ref']) in relset: p['rel']=True      # landed another way (stacked, rebased): its branch tip is in release
    fulls=[short[c['h']] for c in p['commits'] if c['h'] in short]
    if not fulls and p['n'] in squash: fulls=[squash[p['n']]]
    info=summarize(fulls); p['ty']=classify(p['ref'],p['t'],info)
    p.update(fs=info['fs'],ad=info['ad'],dl=info['dl'],ar=info['ar'])
for g in ghost:
    info=summarize([short[c['h']] for c in g['commits'] if c['h'] in short]); g['ty']=classify(g['name'],'',info)
    g.update(fs=info['fs'],ad=info['ad'],dl=info['dl'],ar=info['ar'])
merged_n=sum(1 for p in out_prs if p['mg'])
meta=dict(open=len(open_prs),commits_all=len(commits),commits_main=bin(reach(mainH)).count('1'),pushed=len(brs),
  asof=DT.now(datetime.timezone.utc).isoformat())
envs=None   # no staging/prod environments or release branch in this repo
data=dict(envs=envs,prs=out_prs,branches=brs,ghost=ghost,commits={c['h']:c for c in commits.values()},meta=meta)
t=open(tpl).read()
t=t.replace('/*FONT*/',base64.b64encode(open(font,'rb').read()).decode() if os.path.exists(font) else '')
t=t.replace('__GH__',slug)
t=t.replace('/*DATA*/',json.dumps(data,separators=(',',':'),ensure_ascii=False).replace('</','<\\/'))
t=t.replace('__ASOF__',DT.now().strftime('%B %-d, %Y'))
open(out,'w').write(t)
print(f'{len(out_prs)} PRs ({merged_n} merged, {len(open_prs)} open), {len(brs)} branches ({sum(not b["merged"] for b in brs)} unmerged), {len(commits)} commits, {len(ghost)} ghost; fork parents:',sum(isinstance(p["fk"]["par"],int) for p in out_prs),'stacked')

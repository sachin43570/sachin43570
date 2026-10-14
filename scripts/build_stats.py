"""Builds assets/stats.svg from live GitHub + LeetCode data. Run daily by .github/workflows/update-stats.yml."""
import json,os,re,datetime,urllib.request
USER='sachin43570';LC='sachinmaurya43570'
OUT=os.environ.get('OUT','assets/stats.svg');HERO=os.environ.get('HERO','assets/hero.svg')
N,B,R,T,M,C,L='#070b16','#247bff','#ff354f','#f2f4fb','#9aa4c7','#0b1325','#1d2a52'
COL={'JavaScript':'#f1e05a','HTML':'#e34c26','CSS':'#563d7c','C++':'#f34b7d','C':'#aaaaaa','Python':'#3572A5','TypeScript':'#3178c6','Java':'#b07219','C#':'#178600','Shell':'#89e051','Verilog':'#b2b7f8','SystemVerilog':'#DAE1C2','Jupyter Notebook':'#DA5B0B','Other':'#8d97b8'}
def gh(u):
    h={'User-Agent':'stats','Accept':'application/vnd.github+json'}
    if os.environ.get('GITHUB_TOKEN'):h['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com'+u,headers=h),timeout=25))
def leetcode():
    q={'query':'query($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}}','variables':{'u':LC}}
    r=urllib.request.Request('https://leetcode.com/graphql',data=json.dumps(q).encode(),headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0','Referer':'https://leetcode.com'})
    d=json.load(urllib.request.urlopen(r,timeout=25))
    return next(x['count'] for x in d['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum'] if x['difficulty']=='All')
live=not os.environ.get('PLACEHOLDER')
tiles=[('PUBLIC REPOS','--'),('LANGUAGES','--'),('TOP LANGUAGE','--'),('LEETCODE SOLVED','--')];main=[];tot=1
if live:
    me=gh(f'/users/{USER}');repos=[r for r in gh(f'/users/{USER}/repos?per_page=100') if not r['fork']];lang={}
    for r in repos:
        for k,v in gh(f'/repos/{USER}/{r["name"]}/languages').items():lang[k]=lang.get(k,0)+v
    try:solved=leetcode()
    except Exception:solved=None
    top=sorted(lang.items(),key=lambda x:-x[1]);tot=sum(lang.values()) or 1;main=top[:6]
    if len(top)>6:main.append(('Other',sum(v for _,v in top[6:])))
    tiles=[('PUBLIC REPOS',str(len(repos))),('LANGUAGES',str(len(lang))),('TOP LANGUAGE',top[0][0] if top else '--'),('LEETCODE SOLVED',str(solved)) if solved else ('MEMBER SINCE',me['created_at'][:4])]
FONTS=re.search(r'<style>(@font-face.*?)\.d\{',open(HERO).read(),re.S).group(1)
b=''
for i,(l,v) in enumerate(tiles):
    x=52+i*203;nc=B if i%2==0 else R
    b+=f'<rect x="{x}" y="220" width="185" height="112" rx="18" fill="{C}" stroke="{L}"/><text class="m" x="{x+18}" y="248" font-size="12" fill="{nc}">0{i+1}</text><text class="d" x="{x+18}" y="304" font-size="{54 if len(v)<7 else 34}" fill="{T}">{v}</text><text class="m" x="{x+18}" y="322" font-size="10.5" fill="{M}">{l}</text>'
b+=f'<text class="m" x="52" y="376" font-size="12.5" fill="{R}">// TOP LANGUAGES BY CODE SIZE</text><clipPath id="stc"><rect x="52" y="390" width="796" height="18" rx="9"/></clipPath><rect x="52" y="390" width="796" height="18" rx="9" fill="{L}"/><g clip-path="url(#stc)">'
x=52.0;lg=''
for i,(k,v) in enumerate(main):
    w=796*v/tot;c=COL.get(k,'#8d97b8')
    b+=f'<rect x="{x:.1f}" y="390" width="{w:.1f}" height="18" fill="{c}"><animate attributeName="width" values="0;0;{w:.1f}" keyTimes="0;{i*.08:.2f};1" dur="1.6s" fill="freeze"/></rect>'
    lx=52+(i%4)*199;ly=444+(i//4)*28
    lg+=f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{c}"/><text class="m" x="{lx+16}" y="{ly}" font-size="12.5" fill="{T}">{k}</text><text class="m" x="{lx+16+len(k)*7.6+8:.0f}" y="{ly}" font-size="12.5" fill="{M}">{100*v/tot:.1f}%</text>'
    x+=w
b+='</g>'+lg
if not live:b+=f'<text class="s" x="52" y="450" font-size="16" fill="{M}">Live numbers appear after the first workflow run (Actions tab: Update profile stats).</text>'
d=datetime.date.today()
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 560" width="900" height="560" role="img" aria-label="GitHub and LeetCode stats">
<!-- Fonts: Barlow Condensed, Barlow, JetBrains Mono (SIL OFL 1.1). -->
<style>{FONTS}.d{{font-family:BarlowC,'Barlow Condensed','Arial Narrow',Impact,sans-serif;font-weight:800}}.s{{font-family:BarlowB,Barlow,'Segoe UI',Helvetica,Arial,sans-serif;font-weight:500}}.m{{font-family:JBMono,'JetBrains Mono',Consolas,'Liberation Mono',monospace;font-weight:500}}</style>
<defs><linearGradient id="sx_g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{B}"/><stop offset="1" stop-color="{R}"/></linearGradient><pattern id="sx_dt" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1" fill="#fff" opacity=".07"/></pattern><clipPath id="sx_cl"><rect width="900" height="560" rx="22"/></clipPath></defs>
<rect width="900" height="560" rx="22" fill="{N}"/><rect width="900" height="560" rx="22" fill="url(#sx_dt)"/><rect x=".75" y=".75" width="898.5" height="558.5" rx="21.5" fill="none" stroke="url(#sx_g)" stroke-opacity=".7" stroke-width="1.5"/>
<g clip-path="url(#sx_cl)"><rect width="450" height="8" fill="{B}"/><rect x="450" width="450" height="8" fill="{R}"/></g>
<text class="d" x="52" y="56" font-size="19" fill="{T}" letter-spacing=".6">SACHIN MAURYA</text><text class="m" x="214" y="55" font-size="13" fill="{M}">/  STATS</text><text class="d" x="848" y="64" font-size="32" text-anchor="end"><tspan fill="{B}">S</tspan><tspan fill="{R}">M</tspan></text>
<text class="d" x="50" y="150" font-size="72" fill="{T}">BY THE <tspan fill="{B}">NUMBERS.</tspan></text><text class="s" x="52" y="186" font-size="17" fill="{M}">Pulled live from GitHub and LeetCode, updated daily.</text>
{b}
<line x1="52" y1="500" x2="848" y2="500" stroke="{L}"/><text class="m" x="52" y="528" font-size="12" fill="{M}">UPDATED {d:%d %b %Y}</text><text class="m" x="848" y="528" font-size="12" fill="{M}" text-anchor="end">STATS  /  04</text>
</svg>'''
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True);open(OUT,'w').write(svg);print('wrote',OUT,'live' if live else 'placeholder')

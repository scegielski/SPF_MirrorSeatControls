"""Copy old SPF settings into the renamed plugin without overwriting saved choices."""
import argparse,json
from pathlib import Path
NEW='SPF_MirrorSeatControls'
OLD=('SPF_MirrorControls','SPF_AdjustmentHotkeys')
def rename_keys(value):
 if isinstance(value,list):return [rename_keys(item) for item in value]
 if not isinstance(value,dict):return value
 result={}
 # Exact new keys win if a file already contains both old and new namespaces.
 for key,item in value.items():
  renamed=key
  for old in OLD:
   if key==old or key.startswith(old+'.'):renamed=NEW+key[len(old):];break
  if renamed not in result or renamed==key:result[renamed]=rename_keys(item)
 return result
def migrate(plugins_root):
 destination=plugins_root/NEW/'config/settings.json'
 if destination.exists():return 'New settings already exist; preserved.'
 for old in OLD:
  source=plugins_root/old/'config/settings.json'
  if source.exists():
   settings=json.loads(source.read_text(encoding='utf-8-sig'))
   if not isinstance(settings,dict):raise ValueError('Expected a settings object')
   destination.parent.mkdir(parents=True,exist_ok=True)
   with destination.open('x',encoding='utf-8') as output:json.dump(rename_keys(settings),output,indent=2)
   return f'Copied {source} to {destination}; old config retained.'
 return 'No legacy config found; new plugin will use fresh defaults.'
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--plugins-root',type=Path,required=True)
 print(migrate(parser.parse_args().plugins_root))

import json,tempfile,unittest
from pathlib import Path
from MigrateSettings import migrate,rename_keys,NEW
class MigrationTests(unittest.TestCase):
 def test_empty_bindings_and_new_namespace_win(self):
  data={'keybinds':{'SPF_MirrorControls.Select':{'left':{'bindings':[]}},NEW+'.Move':{'up':1},'SPF_MirrorControls.Move':{'up':2}},'settings':{'servo_sound':False}}
  result=rename_keys(data);self.assertEqual(result['keybinds'][NEW+'.Select']['left']['bindings'],[]);self.assertEqual(result['keybinds'][NEW+'.Move']['up'],1);self.assertFalse(result['settings']['servo_sound'])
 def test_copy_preserves_legacy_and_existing_destination(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);old=root/'SPF_MirrorControls/config/settings.json';old.parent.mkdir(parents=True);old.write_text('{"settings":{"hold_selectors":true}}')
   before=old.read_bytes();migrate(root);new=root/NEW/'config/settings.json';self.assertTrue(json.loads(new.read_text())['settings']['hold_selectors']);self.assertEqual(old.read_bytes(),before)
   new.write_text('{"keep":true}');migrate(root);self.assertEqual(json.loads(new.read_text()),{'keep':True})
if __name__=='__main__':unittest.main()

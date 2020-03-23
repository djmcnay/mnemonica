#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Supporting script for Mnemonica App

For JSON Imports
"""
# %%

import json

# %%

gifs = {
    
   'boobs':[{'link':'https://media.giphy.com/media/tGbhyv8Wmi4EM/giphy.gif'},
            {'link':'https://media.giphy.com/media/12WgrmWEDsKN7q/giphy.gif'},
            {'link':'https://media.giphy.com/media/cwHQOWenYfnQA/giphy.gif'},
            {'link':'https://media.giphy.com/media/13746CZnj9zQwo/giphy.gif'},
            {'link':'https://media.giphy.com/media/50cjS4l1tm8ne/giphy.gif'},
            {'link':'https://media.giphy.com/media/PApKgKr6r20mc/giphy.gif'},
            {'link':'https://media.giphy.com/media/7FgtaDSpeuS1q/giphy.gif'},
            {'link':'https://media.giphy.com/media/54Z5yRMdCB2og/giphy.gif'},
            {'link':'https://media.giphy.com/media/fqu8dnXGXkvio/giphy.gif'},
            {'link':'https://media.giphy.com/media/NgLM8pecbMJvq/giphy.gif'},
            {'link':'https://media.giphy.com/media/M8gheIhsLcttS/giphy.gif'},
            {'link':'https://media.giphy.com/media/qW76IdtQdCJPi/giphy.gif'},
            {'link':'https://media.giphy.com/media/50i6YRZxEiqkM/giphy.gif'},
            {'link':'https://media.giphy.com/media/h0yZVLoXKJKb6/giphy.gif'},
            {'link':'https://media.giphy.com/media/rURpGLsAzr4re/giphy.gif'},
            {'link':'https://media.giphy.com/media/e3ju7ALSHtJmM/giphy.gif'},
            {'link':'https://media.giphy.com/media/pYRYdnMICWmti/giphy.gif'},
            {'link':'https://media.giphy.com/media/xuMu0HuHlXiQ8/giphy.gif'},
            {'link':'https://media.giphy.com/media/nZvxbksUffPUI/giphy.gif'},
            {'link':'https://media.giphy.com/media/BIOMe8sws741G/giphy.gif'},
            {'link':'https://media.giphy.com/media/GJttUmwgh5UpG/giphy.gif'},
            {'link':'https://media.giphy.com/media/aZ9thuwFYNjHO/giphy.gif'},
            {'link':'https://media.giphy.com/media/jrD4gAorYjbW/giphy.gif'},
            {'link':'https://media.giphy.com/media/ehlAgT04i9G6c/giphy.gif'},
            {'link':'https://media.giphy.com/media/hq4iYXKfyKMik/giphy.gif'},
            {'link':'https://media.giphy.com/media/eJBAB5D1e7qMM/giphy.gif'},
            {'link':'https://media.giphy.com/media/WvtVUShnvMDn2/giphy.gif'},
            {'link':'https://media.giphy.com/media/pxbEO1EudaSc/giphy.gif'},
            {'link':'https://media.giphy.com/media/6D0dubMvJUtAA/giphy.gif'},
            {'link':''},
            ],
            
   'strong':[
           {'link':'https://media.giphy.com/media/WrBSHRLE9gEgM/giphy.gif',
            'disc':'Captain America splits log',},
            {'link':'https://media.giphy.com/media/pHXhn8Ee6lRO0KZtM1/giphy.gif',
             'disc':'cartoon hand in a heart'},
            {'link':'https://media.giphy.com/media/20HHkJ3UpFZCt4nQwZ/giphy.gif',
             'disc':'cute kid showing guns'},
            {'link':'https://media.giphy.com/media/xT9Igf2wBfQ8ClCDNC/giphy.gif',
             'disc':'Ali showing fist'},
            {'link':'https://media.giphy.com/media/hV0pccEE0jLfelZPCC/giphy.gif',
             'disc':'cartoon cat lifting weights'},
            {'link':'https://media.giphy.com/media/lPdnkrxkqnS48/giphy.gif',
             'disc':'red panda muscle up'},
            {'link':'https://media.giphy.com/media/cO0dlKKyFGc5q/giphy.gif'},
            {'link':'DC dancing to cakes'},
            {'link':'https://media.giphy.com/media/26FKVSfPIYlZUJngc/giphy.gif'},
            {'link':'cowboy dancing'},
            {'link':'https://media.giphy.com/media/l2JhuG3G56WPngPK0/giphy.gif'},
            {'link':'romero salute'},
            {'link':'https://media.giphy.com/media/5x8am8FstswV2/giphy.gif',
             'disc':'ronda'},
            {'link':'https://media.giphy.com/media/8F32Q0H0L8zyTSCCYI/giphy.gif',
             'disc':'joe rogan commentating'},
            {'link':'https://media.giphy.com/media/aUhEBE0T8XNHa/giphy.gif',
             'disc':'panda dj'},
            {'link':'https://media.giphy.com/media/d1vaWA1lsbIdy/giphy.gif',
             'disc':'kid parks bike'},
            {'link':'https://media.giphy.com/media/Xw6yFn7frR3Y4/giphy.gif',
             'disc':'baby dancing'},
            {'link':'https://media.giphy.com/media/22ZVpCkODW36w/giphy.gif',
             'disc':'DC Dancing with belt'},
             
          ],
             
   'lose':[
           {'link':'https://media.giphy.com/media/127h8dMHnk5H5C/giphy.gif'},
            {'link':'https://media.giphy.com/media/jrmB4IURyv2ik/giphy.gif',
             'disc':'fish face slap'},
            {'link':'https://media.giphy.com/media/3ePb1CHEjfSRhn6r3c/giphy.gif',
             'disc':'loki you had one job'},
            {'link':'https://media.giphy.com/media/NQL7Wuo2JSQSY/giphy.gif',},
            {'link':'https://media.giphy.com/media/PqdfIrXEza6fC/giphy.gif',
             'disc':'yoga kitten crotch bite'},
            {'link':'https://media.giphy.com/media/11StaZ9Lj74oCY/giphy.gif',
             'disc':'penhuin slap'},
            {'link':'https://media.giphy.com/media/47KjwlPVpnQOs/giphy.gif'},
            {'link':'https://media.giphy.com/media/Qc8GJi3L3Jqko/giphy.gif',
             'disc':'sausages to the face'},
            {'link':'https://media.giphy.com/media/fthYZQx5c7hiU/giphy.gif',
             'disc':'archer slap'},
            {'link':'https://media.giphy.com/media/EPcvhM28ER9XW/giphy.gif',
             'disc':'panda smash office'},
            {'link':'https://media.giphy.com/media/vO4ik3XWjkQ2A/giphy.gif',
             'disc':'panda supermarket'},
            {'link':'https://media.giphy.com/media/ZeB4HcMpsyDo4/giphy.gif',
             'disc':'panda falls off log'},
            {'link':'https://media.giphy.com/media/pOeuPPvO3Lbxu/giphy.gif',
             'disc':'panda holding ball'},
            {'link':'https://media.giphy.com/media/47CvsUWHvbmgg/giphy.gif',
             'disc':'panda oh god what have i done'}
          ],            
}
      
   
# %% SAVE
   
json.dump(gifs, open('json_gifs', 'w'))
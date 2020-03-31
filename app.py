#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dash Based Mnemonica Training App

Built as a training toy to better understand how to use Dash-by-Plotly, as well
as to reinforce my 'loci' or 'memory palace' for the Tamariz Mnemonic Stack.

This first version allows the user to select between the 'card' or 'position'
within the stack. 

Things still to fix:
    - write images profiles for each loci
    - random gif sequence based on hastag
    - update layout
    - make image overwrite saveable to json
    - hint box
    """
# %% DEPENDENCIES & DASH SET UP

import pandas as pd
import random
import json
import requests

# Dash & Plotly
import dash
import dash_table as dt
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

# Initialise app object
# Note that we use an internal CSS stylesheet so no external CSS is added
app = dash.Dash('Mnemonica')
app.title='Mnemonica'
server = app.server
    
# GIF Image direectory
# Imported as a JSON file (look at the jsoning.py file)
gifs = json.load(open('assets/json_gifs', 'r'))
gif_wins, gif_loss = [], []

gif_wins.extend([i['link'] for i in gifs['boobs']]+[i['link'] for i in gifs['strong']])
gif_loss.extend([i['link'] for i  in gifs['lose']])

# because I'm an overgrown child, lets add some random hashtags to the gifs
def giphy(hashtag=['boobs', 'sexy'], limit=25, rating=""):
    
    data_list = []
    
    for h in hashtag:
        querystring = {"limit":limit, "q":h, "rating":rating, "api_key":"A9mWPStSmNIqnZQ8QHLLnPj9wR6ioi6u"}    
        response = requests.request("GET", url="https://giphy.p.rapidapi.com/v1/gifs/search",
                                    headers={'x-rapidapi-host':"giphy.p.rapidapi.com",
                                             'x-rapidapi-key':"acc33661bemshee9e80b6508b83bp17261ejsn2ce1309f0c17"},
                                    params=querystring)        
        data_list.extend(json.loads(response.text)['data'])
    
    return ['https://media.giphy.com/media/'+i['id']+'/giphy.gif' for i in data_list]

# extend with popular hastags
gif_wins.extend(giphy(['sexy', 'amazing', 'epic', 'win', 'knockout', 'champion',
                       'strong', 'boobs', 'tits', 'boom']))
gif_loss.extend(giphy(['fail', 'slap', 'no']))

# Dictionaries
# Really just to assist in converting shorthand i.e. AS to Ace of Spades
suits = {'C':'Clubs', 'H':'Hearts', 'D':'Diamonds', 'S':'Spades'}
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
          'J':'Jack','Q':'Queen','K':'King', 'A':'Ace'}

### Stacks are saved in a JSON file
# Currently to edit a stack you need to edit jsoning.py & run that script
stacks = json.load(open('assets/json_stacks', 'r'))
tamariz= pd.DataFrame(stacks['tamariz'], columns=['posn','card','loci','image'])

# %% MARKDOWN BLOCKS

# Note we use a hack with CSS to centralise the image!
# within the CSS I've embedded the line:
#       img[src*='#center'] {display: block; margin: auto;}

md_about = """
    The inspiration for this came from [David & Sarah Trustman]
    (https://www.trustmancreations.com/about-us) and their excellent 
    book ['The Memory Arts'](https://www.vanishingincmagic.com/magic-books/the-memory-arts-book/). 
    
    ![The Memory Arts Book](assets/images/the-memory-arts1.jpeg#center)
    
    The Trustman's convention is to place two-cards in each location, which is something 
    I have followed in my own memory-palace. In the future I hope to add sketches of my 
    each room in my memory palace... or maybe the world doesn't need that.
    
    App was developed by the Pontificating Panada using [Dash](https://plot.ly/dash/) 
    and the source code is available on [GitHub](https://github.com/djmcnay). I don't believe 
    I've infringed any copyrights, but if you believe I have then please let me know and 
    I'll take any offending material down."""
        
# %% LAYOUT

app.layout = html.Div([
    
    ### MEMORY STORE - dash reequires this inside the layout
    # These don't show up on the web app
    # Can live outside the Tabs
    dcc.Store(id='stack_store', data=tamariz.to_dict()),
    dcc.Store(id='problem_data', data={'posn':0, 'type':0}),
    dcc.Store(id='log', data={'n_clicks':0,
                              'n_submits':0,
                              'wins':0,
                              'stack':'tamariz',  # default stack
                              'pTypeRadio':99,    # triggers auto load of problem
                              }),
    
    html.Datalist(id='datalist',
                  children=['Ace of Spades']),
        
    ### HEADER & RANDOM CHAT
    html.H2('Mnemonica Trainer', style={'margin-bottom':'5px',
                                        'text-align':'center'}),

    ### Master Tabs
    dcc.Tabs(id='tabs_master',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             children=[
                     
        # %%  ### MAIN TAB
        dcc.Tab(id='tabs_main',
                className='custom-tab',
                selected_className='custom-tab--selected',
                label='MAIN',
                children=[
            
            # MAIN DIV - Only really exists for CSS
            html.Div([
                
                html.Div([

                    # reload button
                    html.Button(id='button', children='RELOAD', 
                                style={'display':'inline-block',
                                       'width':'25%',
                                       'margin-left':'5%',
                                       'text-align':'center',
                                       'height':'50px',}),
    
                    # Solution Box
                    dcc.Input(id='solution',
                              type='text',
                              placeholder='Answer...',
                              autoComplete='off',
                              maxLength=3,
                              debounce=True,
                              style={'display':'inline-block',
                                     'width':'60%',
                                     'height':'52px',
                                     'margin-left':'2.5%',
                                     'text-align':'justify'}),
                        
                ], style={'width':'100%',
                          'padding-top':'10px',
                          'padding-bottom':'10px',
                          'display':'inline-block',
                          #'border':'1px solid blue',
                            }),
                
                ## PROBLEM DIV
                html.Div([
                    html.Img(id='image_card', style={'maxHeight':'100%',
                                                     'display':'inline-block',}),
                ], style={'width':'100%',
                          'height':'325px',
                          'text-align':'center',
                          'display':'inline-block',
                          #'border':'1px solid green',
                            }),  # END of Problem Div
                        
                ## RESULTS
                # Text with written correct or incorrect
                # Rolling score i.e. 50% correct from 10 attempts
                # GIFs - could be removed in future versions
                html.Div([
                    
                    html.Div(id='solution_written'),
                    html.Div(id='rolling_score'),
                    
                    # Silly little Gif Thing - could easily be deleted or simplifed
                    # uses 2 lists of gifs defined elsewhere for win/loss gifs
                    html.Img(id='image_result', src='',),
                    
                ], style={'text-align':'center',
                          #'border':'1px solid pink',
                          'display':'block'}),    # END Results Div
    
            ], className='tab-div-custom', ), # END of MAIN Div
        ]), # END of MAIN tab
    
        # %% ### STACK TABLE TAB
        dcc.Tab(id='tabs_stack',
                label='STACK',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                        
            html.Div([
                    
                # These seem really easy till you style the f*ckers
                dt.DataTable(
                    id='stack_table',
                    columns=[{'name':i, 'id':i} for i in tamariz.columns],
                    style_table={'maxHeight': '600px',    # 500px is my google browser
                                 'overflowY': 'scroll'},
                    style_as_list_view=True,
                    style_cell_conditional=[
                        {'if':{'column_id':'posn'}, 'text-align':'center', 'width':'15%'},
                        {'if':{'column_id':'card'}, 'text-align':'center', 'width':'15%'},
                        {'if':{'column_id':'loci'}, 'text-align':'center', 'width':'15%'},
                        {'if':{'column_id':'image'}, 'text-align':'center'}],
                    style_data_conditional=[
                        {'if':{'row_index':'odd'}, 'backgroundColor': 'floralwhite'}],
                    style_header={'backgroundColor': 'burlywood',
                                  'fontWeight': 'bold'},
                ),
            ], className='tab-div-custom',),
        ]), # END of STACK tab
    
        # %% ### SETUP TAB
        dcc.Tab(id='tabs_setup',
                label='SETUP',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
            
            html.Div([
            
                # Pre-loaded Stacks
                dcc.Markdown('Choice of Stack:', style={'padding-left':'2%'}),
                dcc.Dropdown(id='dropdown_stack',
                             options=[{'label':'Tamariz Mnemonic Stack', 'value':'tamariz'},
                                      {'label':'Aronson Stack', 'value':'aronson'},],
                             value='tamariz',
                             style={'margin-bottom':'10px',
                                    'padding-left':'5%',
                                    'width':'95%'}),
                             
                # Type of Question
                dcc.Markdown('Test yourself by:', style={'padding-left':'2%'}),
                dcc.RadioItems(id='radio_type',
                               options=[{'label':'posn ','value':0},
                                        {'label':'card  ','value':1},
                                        {'label':'both  ','value':2}],
                                   value=1,
                                   labelStyle={'display': 'inline'},
                                   style={'padding-left':'5%',
                                          }),
    
                # Toggle Button for GIFs
                html.Div([
                    daq.BooleanSwitch(id='switch_gifs', 
                                      label='Display Silly GIFs:',
                                      on=True, color='BURLYWOOD',),
                ], style={'padding-left':'2%',
                          'width':'40%'}),

            ], className='tab-div-custom'), # END of DIV
        
        ]), # END of SETUP TAB
        
        # %% ### NOTES TAB
        dcc.Tab(id='tab_notes',
                label='NOTES',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[dcc.Markdown(md_about,
                                       className='tab-div-custom',
                                       style={'margin':'2%',
                                              'font-size':'13px',
                                              'text-align':'justify',},)],)                     
    
    # %%
    ]), # END of Master TABS
    
    dcc.Markdown('a Pontificating Panda Plaything from 2020',
                 className='markdown-outside-tabs'),
    
    # HIDDEN IN PRODUCTION
    html.Div(id='HIDDEN_DIV', 
             className='markdown-outside-tabs',
             style={'display':'none', 'font-size':'15px', 'margin-top':'100px'})  

# end master Layout
# styling of master-layout done withing 'container' in the CSS file
], className='container') 
    
# %% CALLBACKS
    
### These essentially control the interactions in the apps:
# Originally this was broken into lots of sub-callbacks but now we only have 2
# This probably uses marginally more processing time, but really simplifies stuff
#   1. Store selected stack as a dict() in a dcc.Store()
#   2. MEGA-CALLBACK - which does all the processing

### Setup Stack (Store & Table)
# Source df of stack from stack2df function using the name from the dropdown
# Convert to dict() twice in output; 1. for dcc.Store() and 2. for dash_table
# on dash_table need to convert with 'records' so need to do this op twice
@app.callback([dd.Output('stack_store', 'data'),
               dd.Output('stack_table', 'data')],
              [dd.Input('dropdown_stack', 'value')])
def stack2store(stack):
    #df = stack2df(stack=stack)    
    df = pd.DataFrame(stacks[stack], columns=['posn', 'card', 'loci', 'image'])
    return df.to_dict(), df.to_dict('records')

### MEGA-CALLBACK OF DOOM
# An issue with Dash is a dd.Output(X) can only be triggered in 1 callback
# This is a pain for eg when we want to re-load a problem via a "reload" button
# or after the user submits their solution; we try & fix with the MEGA CALLBACK
    
## Helper functions
def _problem_setup(df, pType):
    
    # random slice of stack 
    s = df.iloc[random.randint(0, df.shape[0]-1),:].to_list()
    
    # Problem Type: 0 is Index, 1 is Card, 2 is either
    pType = random.randint(0,1) if pType not in [0, 1] else pType
        
    return {'posn':s[0], 'card':s[1], 'loci':s[2], 'suit':s[1][-1],
            'value':s[1][0:-1], 'type':pType}    # return dictionary    

## MEGA-CALLBACK
@app.callback([dd.Output('problem_data', 'data'),
               dd.Output('log', 'data'),
               dd.Output('image_card', 'src'),
               dd.Output('solution_written', 'children'),
               dd.Output('solution', 'value'),
               dd.Output('image_result', 'src'),
               dd.Output('image_result', 'style'),
               dd.Output('rolling_score', 'children'),
               dd.Output('HIDDEN_DIV', 'children'),], 
              [dd.Input('button', 'n_clicks'),
               dd.Input('solution', 'n_submit'),    # soln input box on-click
               dd.Input('radio_type', 'value'),     # problem-type radio button
               dd.Input('stack_store', 'data')],    # stack stored as dict()    
              [dd.State('solution', 'value'),       # solution input box
               dd.State('problem_data', 'data'),
               dd.State('log', 'data'),
               dd.State('image_card', 'src'),
               dd.State('switch_gifs', 'on'),
               dd.State('dropdown_stack', 'value')])
def mega_callback(n_clicks, n_submit, pType, stack,
                  soln, prob, log, img_src, gifs, stack_dropdown):
    """ 
    The mega callback function essentially takes any component the gives us an 
    input/state in the app and uses runs the app from start to finsih:
        1. Dummy Outputs (for when we bail out early)
        2. Check if the problem card/posn needs updating - this could be from 
            the reload buttion, a change in problem type or change of stack
        3. Test if the input solution was correct (ignored if ENTER wasn't 
            hit in the solutions box). Then process output text/gifs
        4. If the solution was correct then we reload a new problem
        5. Delete the previous solution
        6. Maintain a rolling score
        
    NB/ In order to do this we utilise the log dictionary extensively; it is 
    stored in the layout as a dcc.Store() object """
    
    # Dummy Outputs - used if not updated during callback
    soln = "" if soln == None else soln
    result_text = "..."
    gif, gif_style = '', {'display':'none'}
    HIDDEN_STR= ""
    DEBUG_CODE= ""
    img_src = app.get_asset_url('numbers/52.png')
    
    
    ### PROBLEM UPDATING
    # NB/ NEEDS to be multiple IFs NOT if/else because we'll get an error if 
    # there have been multiple changes at once & we ignore changes to the log
    
    # Change problem if callback triggered by:
    #   1. Change of state of Problem-Type Radio
    #   2. Change of Stack from Dropdown
    #   3. Reload button
    
    # ACTION: Make more efficeint in the future 
    if log['pTypeRadio'] != pType:
        log['pTypeRadio'] = pType
        prob = _problem_setup(pd.DataFrame(stack), pType)
        
    if log['stack'] != stack_dropdown:
        log['stack'] = stack_dropdown
        prob = _problem_setup(pd.DataFrame(stack), pType)
        
    if  n_clicks == log['n_clicks']+1:
        log['n_clicks'] += 1
        prob = _problem_setup(pd.DataFrame(stack), pType)
        
    ### SOLUTIONS TESTING
    if n_submit == log['n_submits'] + 1:
        
        log['n_submits'] += 1   # add to input box counter 
        
        # see if input solution matches answers for given type
        # 0 => Index given; find Card
        # 1 => Card given; find index
        if prob['type'] == 0 and soln.upper() == prob['card']:
            RESULT = True
        elif prob['type'] == 1 and soln.upper() == str(prob['posn']):
            RESULT = True
        else:
            RESULT = False
            
        # With result +1 to wins, apply result text
        # Also update problem on a win
        # If we have silly gifs then provide a random URL
        if RESULT:
            log['wins'] += 1
            result_text= 'CORRECT'
            prob = _problem_setup(pd.DataFrame(stack), pType)           
            if gifs: 
                gif = random.choice(gif_wins)
        else:
            result_text = 'YOU ARE A FAILURE'
            if gifs:
                gif = random.choice(gif_loss)
            
        # Update GIF Stylesheet stuff & reset solution
        soln = '' 
        gif_style = {'display':'inline-block', 'max-width':'100%'}
    
    ### Update Problem Images/Index Question
    if prob['type'] == 1: 
        ref = 'cards/'+prob['card']+'.png'    # directory of selected card
    else:
        ref = 'numbers/'+str(prob['posn'])+'.png'            
    img_src = app.get_asset_url(ref)

        
    ### ROLLING SCORE
    if log['n_submits'] == 0:
        rolling_score = ''
    else:
        pc = "{0:.0%}".format(log['wins']/log['n_submits'])
        rolling_score = "{} of {} attempts".format(pc, log['n_submits'])
    
    
     ### OTHER ADMIN
    HIDDEN_STR = str(prob)+str(log)+str(pType)+DEBUG_CODE
    
    return (prob, log, img_src, result_text, soln,
            gif, gif_style, rolling_score, HIDDEN_STR)

# %% RUN APP
      
if __name__ == '__main__':
    app.run_server()
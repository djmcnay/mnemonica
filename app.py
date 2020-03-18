#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dash Based Mnemonica Training App

Built as a training toy to better understand how to use Dash-by-Plotly, as well
as to reinforce my 'loci' or 'memory palace' for the Tamariz Mnemonic Stack.

This first version allows the user to select between the 'card' or 'position'
within the stack. """
# %% DEPENDENCIES & DASH SET UP

import pandas as pd
import random
import math

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
app.title='Mnemonica Trainer'
server = app.server
    
# Image Directory
# Totally unnecessary & better of as a dictionary in future
# Should also have an option to skip this
gif_wins = ['https://media.giphy.com/media/WrBSHRLE9gEgM/giphy.gif',
            'https://media.giphy.com/media/50i6YRZxEiqkM/giphy.gif',
            'https://media.giphy.com/media/aUhEBE0T8XNHa/giphy.gif',
            'https://media.giphy.com/media/txsJLp7Z8zAic/giphy.gif',
            'https://media.giphy.com/media/tGbhyv8Wmi4EM/giphy.gif',
            'https://media.giphy.com/media/50cjS4l1tm8ne/giphy.gif',
            'https://media.giphy.com/media/e3ju7ALSHtJmM/giphy.gif',
            'https://media.giphy.com/media/13746CZnj9zQwo/giphy.gif',
            'https://media.giphy.com/media/pYRYdnMICWmti/giphy.gif',
            'https://media.giphy.com/media/xuMu0HuHlXiQ8/giphy.gif',
            'https://media.giphy.com/media/nZvxbksUffPUI/giphy.gif',
            'https://media.giphy.com/media/22ZVpCkODW36w/giphy.gif',
            'https://media.giphy.com/media/l2JhuG3G56WPngPK0/giphy.gif',
            'https://media.giphy.com/media/sVpr5Bdi9Rhm0/giphy.gif',
            'https://media.giphy.com/media/Xw6yFn7frR3Y4/giphy.gif',
            'https://media.giphy.com/media/d1vaWA1lsbIdy/giphy.gif',
            ]

gif_loss = ['https://media.giphy.com/media/jrmB4IURyv2ik/giphy.gif',
            'https://media.giphy.com/media/Qc8GJi3L3Jqko/giphy.gif',
            'https://media.giphy.com/media/fthYZQx5c7hiU/giphy.gif',
            'https://media.giphy.com/media/EPcvhM28ER9XW/giphy.gif',
            'https://media.giphy.com/media/vO4ik3XWjkQ2A/giphy.gif']

# %% MNEMONIC SPECIFICS

### Dictionaries
# Really just to assist in converting shorthand i.e. AS to Ace of Spades
suits = {'C':'Clubs',
         'H':'Hearts',
         'D':'Diamonds',
         'S':'Spades'}

values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
          'J':'Jack','Q':'Queen','K':'King', 'A':'Ace'}

### Functions
def stack2df(stack='tamariz'):
    """ Converts a named stack or list into a pd.DataFrame """
    
    # Tamariz Mnemonic Stack
    tms = ['4C','2H','7D','3C','4H','6D','AS','5H','9S','2S','QH','3D', 'QC','8H',
           '6S','5S','9H','KC','2D','JH', '3S','8S','6H','10C','5D','KD','2C','3H',
           '8D','5C', 'KS','JD','8C','10S','KH','JC','7S','10H','AD','4S', '7H','4D',
           'AC','9C','JS','QD','7C','QS','10D','6C', 'AH', '9D']
    
    # Aaronson Stack
    ars = ['JS','KC','5C','2H','9S','AS','3H','6C','8D','AC','10S','5H','2D',
           'KD','7D','8C','3S','AD','7S','5S','QD','AH','8S','3D','7H','QH',
           '5D','7C','4H','KH','4D','10D','JC','JH','10C','JD','4S','10H','6H',
           '3C','2S','9H','KS','6S','4C','8H','9C','QS','6D','QC','2C','9D']

    if stack == 'tamariz':
        x = tms 
    elif stack == 'aronson':
        x = ars
    
    idx = list(range(1, len(x)+1))
    return pd.DataFrame(list(zip(idx, x, [math.ceil((i/2)) for i in idx])),
                        columns=['index', 'card', 'loci',])

df_dummy = stack2df('tamariz')  
    
# %% MARKDOWN BLOCKS

# Note we use a hack with CSS to centralise the image!
# within the CSS I've embedded the line:
#       img[src*='#center'] {display: block; margin: auto;}

md_about = """
    The inspiration for this came from [David & Sarah Trustman]
    (https://www.trustmancreations.com/about-us) and their excellent 
    book ['The Memory Arts'](https://www.vanishingincmagic.com/magic-books/the-memory-arts-book/). 
    
    ![The Memory Arts Book](assets/originals/the-memory-arts1.jpeg#center)
    
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
    dcc.Store(id='stack_store', data=df_dummy.to_dict()),
    dcc.Store(id='problem_data'),
    
    ## HIDDEN
    # Extra Input boxes used for storage of data
    html.Div([
        dcc.Input(id='results_clicks', type='number', value=0),
        dcc.Input(id='results_wins', type='number', value=0),
    ], style={'display':'none'}), # End hidden DIV
    
    ### HEADER & RANDOM CHAT
    html.H2('Mnemonica Trainer', style={'margin-bottom':'5px',
                                        'text-align':'center'}),
    
    ### Master Tabs
    dcc.Tabs(id='tabs_master',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             children=[
    
        ### MAIN TAB
        dcc.Tab(id='tabs_main',
                className='custom-tab',
                selected_className='custom-tab--selected',
                label='MAIN',
                children=[
                        
            ## GAMEPLAY Div
            # Contains the Refresh button (new problem) & answer box
            # In due course this could have a 'hint' button as well
            html.Div([
                                
                # Play Button
                html.Button(id='button', children='REFRESH'),
                
                # Solution Box
                dcc.Input(id='solution',
                          type='text',
                          placeholder='Answer...',
                          autoComplete='off',
                          style={'height':'100%',
                                 'width':'60%',
                                 'margin-left':'5%'}),
     
            ], style={'display':'inline-block',
                      'width':'90%',
                      'margin-left':'5%',
                      'margin-top':'15px'}),    # End of Gameplay Div
   
            ## PROBLEM DIV
            # Here we have a No (position index) & Image of a card
            # No styling on either, because the 'style' gets updated in a callback
            html.Div([
                
                html.P(id='problem_number', children='',),
                html.Img(id='image_card'), 
                
                # HIDDEN IN PRODUCTION
                html.Div(id='problem_written',
                         style={'font-size':12,
                                'display':'none'})                   
            
            ], id='div_problem',
               style={'height':'175px',
                      'font-size':100,
                      'font-weight':'boldest',
                      'text-align':'center',
                      'padding-top':'25px'}),    # END of Problem Div
    
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
                
            ], style={'text-align':'center',}),    # END Results Div
    
    
        ]), # END of MAIN tab
    
        ### STACK TABLE TAB
        dcc.Tab(id='tabs_stack',
                label='STACK',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                        
            html.Div([
                    
                # These seem really easy till you style the f*ckers
                dt.DataTable(
                    id='stack_table',
                    columns=[{'name':i, 'id':i} for i in df_dummy.columns],
                    style_table={'maxHeight': '500px',    # 500px is my google browser
                                 'overflowY': 'scroll'},
                    style_as_list_view=True,
                    style_cell_conditional=[
                        {'if':{'column_id':'index'}, 'text-align':'center'},
                        {'if':{'column_id':'card'}, 'text-align':'center'},
                        {'if':{'column_id':'loci'}, 'text-align':'center'}],
                    style_data_conditional=[
                        {'if':{'row_index':'odd'}, 'backgroundColor': 'floralwhite'}],
                    style_header={'backgroundColor': 'burlywood',
                                  'fontWeight': 'bold'},
                ),
            ], className='tab-div-custom',),
        ]), # END of STACK tab
    
        ### SETUP TAB
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
                               options=[{'label':'card  ',  'value':'card'},
                                        {'label':'index ', 'value':'index'},
                                        {'label':'both  ',  'value':'both'}],
                                   value='both',
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
        
        ### NOTES TAB
        dcc.Tab(id='tab_notes',
                label='NOTES',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[dcc.Markdown(md_about,
                                       style={'margin':'2%',
                                              'font-size':'13px',
                                              'text-align':'justify'})])                     
                
    
    ]), # END of Master TABS
    
    dcc.Markdown('a Pontificating Panda Plaything from 2020',
                 className='markdown-outside-tabs')

# end master Layout
# styling of master-layout done withing 'container' in the CSS file
], className='container') 
    
# %% CALLBACKS
    
### These essentially control the interactions in the apps:
#   1. Setup stack - selected in settings & stored as dict() in dcc.Store
#   2. Setup the problem using user preferences & store in dcc.Store as dict()
#   3. Setup chain links to Update Problem - this controls the card image or
#           the numerical index; hiding the html object for the other one.
#   4. Solutions tester - checks if the answer from the inputbox was correct
#           then updates a string output, a gif thing & clicks/wins counters
#   5. Rolling tally - creates string with rolling success (could be charted)

### Setup Stack (Store & Table)
# Source df of stack from stack2df function using the name from the dropdown
# Convert to dict() twice in output; 1. for dcc.Store() and 2. for dash_table
# on dash_table need to convert with 'records' so need to do this op twice
@app.callback([dd.Output('stack_store', 'data'),
               dd.Output('stack_table', 'data')],
              [dd.Input('dropdown_stack', 'value')])
def store_selected_stack(stack):
    df = stack2df(stack=stack)      
    return df.to_dict(), df.to_dict('records')

### SETUP PROBLEM
# Pull stack from dcc.Store(); stored as dict() so convert to DataFrame
@app.callback(dd.Output('problem_data', 'data'),
              [dd.Input('button', 'n_clicks'),
               dd.Input('stack_store', 'data'),
               dd.Input('radio_type', 'value'),])
def problem_setup(n_clicks, stack_store, radio):

    df = pd.DataFrame(stack_store)    # convert to DataFrame
    
    # Get a random card from the stack
    n = df.shape[0]    # length of stack
    s = df.iloc[random.randint(0,n-1),:].to_list()
    
    # Type of game being played
    if radio == 'index': t = 0
    elif radio == 'card': t = 1
    else: t = random.randint(0,1)
    
    return {'posn':s[0], 'card':s[1], 'loci':s[2],
            'suit':s[1][-1], 'value':s[1][0:-1],
            'type':t}

## WRITTEN PROBLEM - output hidden in production but useful for testing
@app.callback(dd.Output('problem_written', 'children'),
              [dd.Input('problem_data', 'data')])
def problem_written(x):
    return str(x)

## UPDATE PROBELM PICTURE/NUMBER - based on new problem
@app.callback([dd.Output('image_card', 'src'),
               dd.Output('problem_number', 'children'),
               dd.Output('image_card', 'style'),
               dd.Output('problem_number', 'style')],
              [dd.Input('problem_data', 'data')])
def update_card_image(data):
    
    # find directory reference for current problem card
    ref = 'cards/'+data['card']+'.png'
    
    # adjust style hidden/inline depnding on if we are solving card/position
    if data['type'] == 1:
        card = {'display':'inline-block',
                      'height':'150px'}
        posn = {'display':'none'}
    else:
        card = {'display': 'none'}
        posn = {'display':'inline-block',
                     'align':'center', 
                     'width':'100%'}
    
    return app.get_asset_url(ref), data['posn'], card, posn

### SOLUTIONS TESTER
@app.callback([dd.Output('solution_written', 'children'),
               dd.Output('results_clicks', 'value'),
               dd.Output('results_wins', 'value'),
               dd.Output('image_result', 'src'),
               dd.Output('image_result', 'style')],
              [dd.Input('solution', 'value'),
               dd.Input('solution', 'n_submit')],
              [dd.State('results_clicks', 'value'),
               dd.State('problem_data', 'data'),
               dd.State('results_wins', 'value'),
               dd.State('switch_gifs', 'on')])
def solution_tester(solution, n, clicks, prob, wins, gifs):
    
    ## ADMIN
    # before we store any clicks == None NOT 0
    if clicks == None: clicks = 0
    gif = ''    # default GIF URL is blank (assumes we don't want one)
    
    ## MAIN WORK
    # if the number of submissions > stored clicks, we have an answer to test
    # otherwise typing (without confirmation) has caused callback trigger
    if n != clicks + 1:        
        text, gif_style = '...', {'display':'none'}
    else:
        
        # see if input solution matches answers for given type
        # 0 => Index given; find Card
        # 1 => Card given; find index
        if prob['type'] == 0 and solution.upper() == prob['card']:
            RESULT = True
        elif prob['type'] == 1 and solution.upper() == str(prob['posn']):
            RESULT = True
        else:
            RESULT = False
        
        # With result +1 to wins, apply result text
        # If we have silly gifs then provide a random URL
        if RESULT:
            wins += 1
            text = 'CORRECT'
            if gifs: 
                gif = random.choice(gif_wins)
        else:
            text = 'YOU ARE A FAILURE'
            if gifs:
                gif = random.choice(gif_loss)
            
        # Update GIF Stylesheet stuff
        gif_style = {'display':'inline-block', 'max-width':'100%'}
        
    return text, n, wins, gif, gif_style

## Rolling solutions
# NB/ Could just roll this into the solution callback function
@app.callback(dd.Output('rolling_score', 'children'),
              [dd.Input('results_clicks', 'value'),
               dd.Input('results_wins', 'value')])
def rolling_tally(clicks, wins):
       
    if (clicks == 0 and wins == 0) or clicks == None:
        return ""
    else:
        pc = "{0:.0%}".format(wins/clicks)
        return "{} of {} attempts".format(pc, clicks)

# %% RUN APP
      
if __name__ == '__main__':
    app.run_server(debug=True)
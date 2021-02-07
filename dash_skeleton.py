import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import math
import os
import logging


app = dash.Dash(__name__)
app.title = 'Face ID Fail'
server = app.server


# introduction text
app.layout = html.Div([
    html.Div([
        #html.H2("Face ID Fail", id='title', style={'font-family': 'Monaco'}),
        #html.H4("***This beta version works best in Chrome***", style={'font-family': 'Monaco'}),
        # purpose section
        html.Div([
#             html.H3("Purpose: ", id = 'purpose', style = {'font-weight': 'bold', 'font-family': 'Monaco'}),
#             html.P("The goal of this demo is to show you the risks of face recognition software. In the most basic terms, face recognition software attempts to match different images of faces. When images are run through face recognition software they are given a numerical value. The goal is to determine if the face in, say, Photo A belongs to the same person as in Photo B. The similarity of these photos, and whether they show the same face, is determined by the numerical value the face recognition software assigns each photo. You may have seen such software in crime and action TV shows or movies (think, CSI, Jason Bourne, Minority Report, or the Mission Impossible franchise). In these thrillers, this software is presented as error-free and foolproof. But, is it actually?"),
        ]),
        # main points section
        html.Div([
#             html.H3("Main Points: ", id = 'mainpoints', style = {'font-weight': 'bold', 'font-family': 'Monaco'}),
#             html.P("Though there are many concerns about the use of face recognition software, this demo will show two weaknesses in particular. "),
#             html.Span("First, ", style={'font-weight': 'bold'}),
#             " the demo will show you how face recognition software relies on “threshold” settings. ",
#             "The numerical value face recognition software assigns each image is compared to the values assigned to other images. ",
#             "The threshold setting is a cutoff point the user of the software selects — any images whose numerical value is below this cutoff are discarded and not considered matches. ",
#             "Any image above this threshold, or cutoff, is considered a potential match. ",
#             "Therefore, threshold settings affect the software’s accuracy, and both the selected threshold and ultimately the matches produced are judgement calls made by humans.",
                ]),
        html.Div([
#              html.P("    "),
#              html.Span("Second, ", style={"font-weight": "bold"}),
#              "  this demo shows that face recognition software misidentifies women and people of color, especially women of color, more often than white men. ",
#              "This has been shown at length in academic and policy literature. ",
#              "For darker skin toned faces especially, face recognition software is more likely to produce false positives, meaning the software shows two faces to be a match, though they are not. ",
            ]),
        # terms to know section
        html.Div([
            html.H3("Terms to Know: ", id = "terms", style = {'font-weight': 'bold', 'font-family': 'Monaco'}),
            html.P("The following are some helpful terms for better understanding this demo."),
            html.Span("Similarity Score: ", style={'font-weight': 'bold'}),
            " is a numerical value that represents how similar two faces are. Facial recognition software converts images into mathematical representations used to compare various faces and find potential matches. For purposes of this demo, the greater the similarity score, the more similar two faces are. ",
            "    ",
                ]),
        html.Div([
             html.Span("Threshold: ", style={"font-weight": "bold"}),
             "A threshold setting sets the cut-off for the similarity score that is reported as a match.",
            ]),
        html.Div([
             html.Span("False Positive: ", style={"font-weight": "bold"}),
             "occurs when images that are not of the same person are incorrectly labeled as a match.",
            ]),
        html.Div([
             html.Span("True Positive: ", style={"font-weight": "bold"}),
             "occurs when two images, which are indeed of the same person, are correctly labeled as a match. ",
            "In our demo, true positives are outlined in ",
             html.Span('green.', style={'background-color': '#00ff00', 'font-weight': 'bold'}),
            ]),
        html.Div([
            html.Span("False Negative: ", style={"font-weight": "bold"}),
            "occurs when images that are actually of the same person are incorrectly labeled as not matching.",
            ]),

        # instructions section
        html.H3('Instructions:', id='instructions', style={'font-family': 'Monaco'}),
        html.P("1. Enter full screen in your browser. You'll see the demo has 3 main sections - 'Current Subject, 'Matches', and 'Threshold'. "),
        html.Div([
            "2. Under 'Matches' you'll see those faces that have matched with the face under 'Current Subject'. Below each match is the similarity score between the 'Current Subject' and that match. For ease of interpretation, in this demo the larger the similarity score, the more similar two images are. The only true positive match is that which is outlined in green. All other matches are false positives.",
                ]),
        html.P("3. In the 'Threshold' section you'll see a slider. Move the slider by clicking on the numbered intervals. This changes the minimum similarity score required in order to be considered a match. As you move the slider, you'll see some matches fade away as their similarity score does not meet the minimum threshold you've set. "),
        html.P("4. Under 'Current Subject', you'll see a list of other options. Click through the diverse list of celebrities, playing around with the threshold slider as well. Take note of how effecitvely, or ineffectively, the software identifies true matches. "),
        html.P("5. Compare similarity scores and thresholds across 'Current Subjects' of different races, ethnicities, and genders. "),
            ]),


        # questions to consider section
#         html.Div([
#             html.H3("Questions to Consider: ", id = "questions", style = {'font-weight': 'bold', 'font-family': 'Monaco'}),
#             html.P("While you use this demo, consider the following questions."),
#             html.P("1a. What is the lowest threshold at which the software correctly identifies Aaron Piersol's face?"),
#             html.P("1b. What is the lowest threshold at which the software correctly identifies LeBron James' face?"), 
#             html.P("1c. What is the lowest threshold at which the software correctly identifies Jacqueline Edwards' face?"),
#             html.P("2. Consider whether making facial recognition software more accurate for people of color would actually make the technology safe to use. More accurate facial recognition software could help policing and surveillance among communities of color, undocumented immigrants, and others. Do you think more accurate software has a place in our society?")
#                 ]),


    # stores current subject data
    html.Div([
    html.Div(id='current_data_similarity', style={'display': 'none'}, children=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]),
    html.Div(id='current_data_names', style={'display': 'none'}, children=['','','','','','','','']),
    html.Div(id='current_match_values', style={'display': 'none'}, children=[False,False,False,False,False,False,False,False]),

#    subject and radio button options to switch subject
    html.Div([
        html.H4("Current Subject: ", id = "current", style = {'font-weight': 'bold', 'font-family': 'Monaco'}),

        html.Img(id='celeb'), dcc.RadioItems(
    options=[
        {'label': 'LeBron James', 'value': 'LeBron_James.csv'},
        {'label': 'Lisa Leslie', 'value': 'Lisa_Leslie.csv'},
        {'label': 'Paris Hilton', 'value': 'Paris_Hilton.csv'},
        {'label': 'Jennifer Lopez', 'value': 'Jennifer_Lopez.csv'},
        {'label': 'Aaron Peirsol', 'value': 'Aaron_Peirsol.csv'},
        {'label': 'Jacqueline Edwards', 'value': 'Jacqueline_Edwards.csv'},
        {'label': 'Kalpana Chawla', 'value': 'Kalpana_Chawla.csv'},
        {'label': 'Jason Campbell', 'value': 'Jason_Campbell.csv'},
        {'label': 'Katie Couric', 'value': 'Katie_Couric.csv'},
        {'label': 'Vicki Zhao Wei', 'value': 'Vicki_Zhao_Wei.csv'}
    ],
    value='LeBron_James.csv',
    labelStyle={'display': 'inline-block'},
    id = 'subject_options'
), html.Div(id="mismatch_title", className="mismatch_title"),
html.Div([
html.Div(id='subject1_mismatches', className = 'mismatches1', style={'marginBottom': '.14em'}),
html.Div(id='subject2_mismatches', className = 'mismatches2', style={'marginBottom': '.14em'}),
html.Div(id='subject3_mismatches', className = 'mismatches3', style={'marginBottom': '.14em'}),
html.Div(id='subject4_mismatches', className = 'mismatches4', style={'marginBottom': '.14em'}),
html.Div(id='subject5_mismatches', className = 'mismatches5', style={'marginBottom': '.14em'}),
html.Div(id='subject6_mismatches', className = 'mismatches6', style={'marginBottom': '.14em'}),
html.Div(id='subject7_mismatches', className = 'mismatches7', style={'marginBottom': '.14em'}),
html.Div(id='subject8_mismatches', className = 'mismatches8', style={'marginBottom': '.14em'}),
html.Div(id='subject9_mismatches', className = 'mismatches9', style={'marginBottom': '.14em'}),
html.Div(id='subject10_mismatches', className = 'mismatches10', style={'marginBottom': '.14em'})
], id="mismatches")],
id='subject'),






    # creates divs for images
    html.Div([
    html.Div([html.Div([
        html.H4("Threshold: ", id = "thresh", style = {'font-weight': 'bold', 'font-family': 'Monaco'})
        ], id = 'threshold_title'),
            dcc.Slider(
            id='threshold-slider',
            min=-0.0,
            value = 0.0
        ),
        html.Div(
         id='slider-output-container', className = 'slider'
        ), html.Div(
         id='slider-output-container2', className = 'slider'
        ),
        html.Div([
            html.H4('Current Matches:')
            ], id = 'matches')], id = 'slider'),

        html.Div([
        html.Div([
            html.Img(id='img1'), html.Figcaption(id='name1'),
            html.Figcaption(id='sim1')
            ], id='result1', className='result1'),

        html.Div([
            html.Img(id='img2'), html.Figcaption(id='name2'),
            html.Figcaption(id='sim2')
            ], id='result2', className = 'result2'),
        html.Div([
            html.Img(id='img3'), html.Figcaption(id='name3'),
            html.Figcaption(id='sim3')
            ], id='result3', className = 'result3'),
        html.Div([
            html.Img(id='img4'), html.Figcaption(id='name4'),
            html.Figcaption(id='sim4')
            ], id='result4', className = 'result4'),
        html.Div([
            html.Img(id='img5'), html.Figcaption(id='name5'),
            html.Figcaption(id='sim5')
            ], id='result5', className = 'result5'),
        html.Div([
            html.Img(id='img6'), html.Figcaption(id='name6'),
            html.Figcaption(id='sim6')
            ], id='result6', className = 'result6'),
        html.Div([
            html.Img(id='img7'), html.Figcaption(id='name7'),
            html.Figcaption(id='sim7')
            ], id='result7', className = 'result7'),
        html.Div([
            html.Img(id='img8'), html.Figcaption(id='name8'),
            html.Figcaption(id='sim8')
            ], id='result8', className = 'result8')], className = 'pics')], className = 'box')
            ], id = "interactive"),

# slider



    html.Div([
#      html.H3('Case Studies:'),
#      html.Div([

#      html.Span("ICE Uses Facial Recognition To Sift State Driver's License Record", style = {'font-weight': 'bold'}),
#      ": In July of 2019, researchers at Georgetown University Law Center found that Immigration and Customs Enforcement (ICE) agents mined millions of driver's license photographs in search of facial recognition matches to target undocumented migrants who have legally obtained driver's licenses. ICE did this illegally, as they did not have congressional approval to access DMV databases of driver's license photos.  In this scenario, the use of facial recognition technology clearly put undocumented migrants at risk. Further, increased accuracy would have only heightened the danger undocumented migrants face and increased targeting of communities of color. ",
#      dcc.Link('Read NPR news coverage of this case here.', href='https://www.npr.org/2019/07/08/739491857/ice-uses-facial-recognition-to-sift-state-drivers-license-records-researchers-sa'),
#      ]),
#      html.H4(' '),
#      html.Span('Washington County Police Department', style = {'font-weight': 'bold'}),
#      ": In 2017, the Washington County Police Department in Oregon pioneered the use of Amazon's facial recognition software tool, Rekognition, to compare surveillance footage of people's faces to a database of mug shot photos in an attempt to identify burglary suspects. Oregon Live reports that deputies are permitted to run artist sketches into the search. As our demo illustrates, the use of facial recognition software often results in false positives, putting innocent people at risk of being targeted and arrested. Given the software is less accurate on people of color and results in more false positives for people of color, this community faces heightened risk of being targeted by law enforcement. The similarity threshold that the police department uses affects their rate of false positives. Although Amazon recommends only using its Rekognition tool with a 99 percent similarity threshold when identifying suspects for law enforcement purposes, police departments are not required to follow these guidelines. ",
#      dcc.Link('Read Washington Post coverage featured in Oregon Live here, ', href='https://www.oregonlive.com/washingtoncounty/2019/05/amazons-facial-recognition-technology-is-supercharging-washington-county-police.html'),
#      dcc.Link('coverage in KGW Portland Coverage here, ', href='https://www.kgw.com/article/money/aclu-calls-out-amazon-washington-co-sheriffs-office-for-facial-recognition-tech/283-557099068'),
#      dcc.Link('and read official Amazon guidelines here', href = 'https://docs.aws.amazon.com/rekognition/latest/dg/collections.html')


    ], id = "case_studies"),

    html.Div([
#      html.H3('Resources:'),
#      html.Div([
#      html.Span("Facial Recognition Model", style = {'font-weight': 'bold'}),
#      ": We used Open Face's Open Source Facial Recognition model to run our images and determine matches. We ran Open Face's model using a Docker container. We edited Open Face's image comparison Python file to only compare one specified image against the entire dataset of images, instead of each image in the dataset to every other image.",
#      html.H4(' '),
#      html.Span("Images", style = {'font-weight': 'bold'}),
#      ": We obtained nearly of all our images from Labeled Faces in the Wild, an  open dataset of celebrity photos. For celebrity subjects who did not have more than one photo in the Labeled Faces in the Wild dataset, we supplemented with images from Google Image searches."
#      ]),
    ], id = "resources")
])

#loads all images and slider with current subject
@app.callback([Output('celeb', 'src'), Output('img1', 'src'), Output('img2', 'src'), Output('img3', 'src'), Output('img4', 'src'), Output('img5', 'src'),
Output('img6', 'src'), Output('img7', 'src'), Output('img8', 'src'), Output('threshold-slider', 'max'), Output('threshold-slider', 'step'),
Output('threshold-slider', 'marks'), Output('current_data_similarity', 'children'), Output('current_data_names', 'children'), Output('current_match_values', 'children')], [Input('subject_options', 'value')])
def update_output(value):
    print("updating output: ", value)
    #data = load_data(value)
    results = pd.read_csv(value)
    print("updated value: ", value)
    #gather names
    names = results['Name']

    #determine max similarity
    similarity = results['Similarity']

    threshold_upper = 1.4

    #determine step for threshold
    step = .1

    #download match booleans
    matches = results['Match']

    #create mark dictionary for slider
    steps = {}
    c=0
    for i in range(15):
        if round((c+step*i), 2) == 0.00:
            steps[0] = str(round(c+(step*i), 1))
        elif round((c+step*i), 2) == 1.00:
            steps[1] = str(round(c+(step*i), 1))
        else:
            steps[round((c+step*i), 2)] = str(round(c+(step*i), 2))

    # upload corresponding images
    subject_image = results["Subject_File"][0]
    images = results["File"]

    return [subject_image, images[0], images[1], images[2], images[3], images[4],
        images[5], images[6], images[7], threshold_upper,
        step, steps, similarity, names, matches]

# threshold image 1
@app.callback([Output('img1', 'style'), Output('name1', 'children'), Output('sim1', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[0] >= threshold:
        if match[0]:
            return {"border":"10px #00ff00 solid"}, names[0], str(round(similarity[0], 3))
        else:
            return {"border":"10px black solid"}, names[0], str(round(similarity[0], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[0], str(round(similarity[0], 3))

#threshold image 2
@app.callback([Output('img2', 'style'),Output('name2', 'children'), Output('sim2', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[1] >= threshold:
        if match[1]:
            return {"border":"10px #00ff00 solid"}, names[1], str(round(similarity[1], 3))
        else:
            return {"border":"10px black solid"}, names[1], str(round(similarity[1], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[1], str(round(similarity[1], 3))

#threshold image 3
@app.callback([Output('img3', 'style'),Output('name3', 'children'), Output('sim3', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[2] >= threshold:
        if match[2]:
            return {"border":"10px #00ff00 solid"}, names[2], str(round(similarity[2], 3))
        else:
            return {"border":"10px black solid"}, names[2], str(round(similarity[2], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[2], str(round(similarity[2], 3))

#threshold image 4
@app.callback([Output('img4', 'style'),Output('name4', 'children'), Output('sim4', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[3] >= threshold:
        if match[3]:
            return {"border":"10px #00ff00 solid"}, names[3], str(round(similarity[3], 3))
        else:
            return {"border":"10px black solid"}, names[3], str(round(similarity[3], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[3], str(round(similarity[3], 3))

#threshold image 5
@app.callback([Output('img5', 'style'),Output('name5', 'children'), Output('sim5', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[4] >= threshold:
        if match[4]:
            return {"border":"10px #00ff00 solid"}, names[4], str(round(similarity[4], 3))
        else:
            return {"border":"10px black solid"}, names[4], str(round(similarity[4], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[4], str(round(similarity[4], 3))

#threshold image 6
@app.callback([Output('img6', 'style'),Output('name6', 'children'), Output('sim6','children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'),
    Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[5] >= threshold:
        if match[5]:
            return {"border":"10px #00ff00 solid"}, names[5], str(round(similarity[5], 3))
        else:
            return {"border":"10px black solid"}, names[5], str(round(similarity[5], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[5], str(round(similarity[5], 3))

#threshold image 7
@app.callback([Output('img7', 'style'),Output('name7', 'children'), Output('sim7', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[6] >= threshold:
        if match[6]:
            return {"border":"10px #00ff00 solid"}, names[6], str(round(similarity[6], 3))
        else:
            return {"border":"10px black solid"}, names[6], str(round(similarity[6], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[6], str(round(similarity[6], 3))

#threshold image 8
@app.callback([Output('img8', 'style'),Output('name8', 'children'), Output('sim8', 'children')],
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    if similarity[7] >= threshold:
        if match[7]:
            return {"border":"10px #00ff00 solid"}, names[7], str(round(similarity[7], 3))
        else:
            return {"border":"10px black solid"}, names[7], str(round(similarity[7], 3))
    else:
        return {"border":"10px black solid", "opacity": "0.2"}, names[7], str(round(similarity[7], 3))

# threshold text
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')])
def update_output(value):
    return 'The minimum similarity score you have selected for a match is: {}'.format(value)

# threshold text
@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [Input('threshold-slider', 'value'), Input('current_data_similarity', 'children'), Input('current_data_names', 'children'), Input('current_match_values', 'children')])
def update_output(threshold, similarity, names, match):
    num_match = 0
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if match[i]==False:
                num_match +=1
    if num_match == 1:
        return 'This threshold results in {} mismatch for the current subject.'.format(num_match)
    else:
        return 'This threshold results in {} mismatches for the current subject.'.format(num_match)

#mismatches LeBron James
@app.callback(
    dash.dependencies.Output('subject1_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('LeBron_James.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)


#mismatches Lisa Leslie
@app.callback(
    dash.dependencies.Output('subject2_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Lisa_Leslie.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Paris Hilton
@app.callback(
    dash.dependencies.Output('subject3_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Paris_Hilton.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Jennifer_Lopez
@app.callback(
    dash.dependencies.Output('subject4_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Jennifer_Lopez.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Aaron_Peirsol
@app.callback(
    dash.dependencies.Output('subject5_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Aaron_Peirsol.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Jacqueline_Edwards
@app.callback(
    dash.dependencies.Output('subject6_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Jacqueline_Edwards.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Kalpana_Chawla
@app.callback(
    dash.dependencies.Output('subject7_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Kalpana_Chawla.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Jason_Campbell
@app.callback(
    dash.dependencies.Output('subject8_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Jason_Campbell.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)
    
#mismatches Katie_Couric
@app.callback(
    dash.dependencies.Output('subject9_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Katie_Couric.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#mismatches Vicki_Zhao_Wei
@app.callback(
    dash.dependencies.Output('subject10_mismatches', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    num_match = 0
    results1 = pd.read_csv('Vicki_Zhao_Wei.csv')
    matches = results1['Match']
    similarity = results1['Similarity']
    matches_subject = False
    for i in range(len(similarity)):
        if similarity[i] >= threshold:
            if matches[i]==False:
                num_match +=1
            else:
                matches_subject = True
    num_match_percent = int(num_match/7 * 100)
    if matches_subject==False and num_match==0:
        return 'Fails to ID anyone'
    elif num_match_percent==0:
        return 'Correctly Matches'
    else:
        return '{}% mismatches'.format(num_match_percent)

#threshhold mismatch title
@app.callback(
    dash.dependencies.Output('mismatch_title', 'children'),
    [Input('threshold-slider', 'value')])
def update_output(threshold):
    return 'Mismatches at {} threshold'.format(threshold)

if __name__ == '__main__':
    port = os.environ.get('PORT') or 8035
    debug = 'DYNO' not in os.environ
    app.run_server(port=port, debug=debug)
   # app.run_server(port=port)

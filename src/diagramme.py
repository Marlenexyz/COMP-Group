import matplotlib.pyplot as plt
import numpy as np

'Projector'
def _bright_lighting_conditions_recall_plot():
    'Bright Lighting Conditions'
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']
    values = [0.66, 0.27, 0.77, 0.85]

    # Erstelle ein Balkendiagramm
    plt.bar(labels, values)

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Bright Lighting Conditions Recall For Hand Gestures')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.show()

def _middle_lighting_conditions_recall_plot():
    'Middle Lighting Conditions'
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']
    values = [0.94,0.89,0.54,0.95]

    # Hand recall: 0.94
    # Pinch recall: 0.89
    # V recall: 0.54
    # Fist recall: 0.95
    # Erstelle ein Balkendiagramm
    plt.bar(labels, values)

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Middle Lighting Conditions Recall For Hand Gestures')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.show()

def _low_lighting_conditions_recall_plot():
    'Low Lighting Conditions'
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']
    values = [0.99,0.92,0.66,0.87]

    # Hand recall: 0.99
    # Pinch recall: 0.92
    # V recall: 0.66
    # Fist recall: 0.87

    # Erstelle ein Balkendiagramm
    plt.bar(labels, values)

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Low Lighting Conditions Recall For Hand Gestures')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.show()

'Projector'
def _combined_lighting_conditions_recall_plot():
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']
    values_bright = [0.66, 0.27, 0.77, 0.85]
    values_middle = [0.94, 0.89, 0.54, 0.95]
    values_low = [0.99, 0.92, 0.66, 0.87]

    # Breite der Balken
    bar_width = 0.25

    color_light = 'lightgray'
    color_middle = 'darkgray'
    color_dark = 'gray'

    # X-Positionen für die Balken
    bar_positions_bright = np.arange(len(labels))
    bar_positions_middle = [pos + bar_width for pos in bar_positions_bright]
    bar_positions_low = [pos + 2 * bar_width for pos in bar_positions_bright]

    # Erstelle ein kombiniertes Balkendiagramm
    plt.bar(bar_positions_bright, values_bright, width=bar_width, label='Bright Lighting', color=color_light)
    plt.bar(bar_positions_middle, values_middle, width=bar_width, label='Middle Lighting', color=color_middle)
    plt.bar(bar_positions_low, values_low, width=bar_width, label='Low Lighting', color=color_dark)

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Recall For Hand Gestures Under Different Lighting Conditions')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.xticks(bar_positions_middle, labels)
    plt.legend()
    plt.show()



def frame_matching_plot():
    labels = ['Good Lighting', 'Middle Lighting', 'Bad Lighting']
    precision_values = [0.91, 0.91, 0.93]
    recall_values = [0.92, 0.91, 0.94]

    # Breite der Balken
    bar_width = 0.35

    # X-Positionen für die Balken
    bar_positions_precision = np.arange(len(labels))
    bar_positions_recall = [pos + bar_width for pos in bar_positions_precision]

    # Erstelle ein Balkendiagramm für die Präzision und den Recall
    plt.bar(bar_positions_precision, precision_values, width=bar_width, label='Precision')#, color='lightblue')
    plt.bar(bar_positions_recall, recall_values, width=bar_width, label='Recall')#, color='lightgreen')

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Frame Matching Precision and Recall Under Different Lighting Conditions')
    plt.xlabel('Lighting Conditions')
    plt.ylabel('Score')

    # Zeige das Diagramm an
    plt.xticks(bar_positions_recall, labels)
    plt.legend()
    plt.show()

def _combined_lighting_conditions_recall_plot_home():
    'Home conditions'
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']

    values_bright = [1.0,1.0,0.18,1.0]
    values_low = [1.0,0.73,0.98,0.19]
    # -- bad lighting conditions
    # Hand recall: 1.0
    # Pinch recall: 0.73
    # V recall: 0.98
    # Fist recall: 0.19


    # -- good lighting conditions
    # Hand recall: 1.0
    # Pinch recall: 1.0
    # V recall: 0.18
    # Fist recall: 1.0

    # Breite der Balken
    bar_width = 0.25

    color_light = 'lightgray'
    # color_middle = 'darkgray'
    color_dark = 'gray'

    # X-Positionen für die Balken
    bar_positions_bright = np.arange(len(labels))
    bar_positions_middle = [pos + 0.5 * bar_width for pos in bar_positions_bright]
    bar_positions_low = [pos + bar_width for pos in bar_positions_bright]

    # Erstelle ein kombiniertes Balkendiagramm
    plt.bar(bar_positions_bright, values_bright, width=bar_width, label='Bright Lighting', color=color_light)
    # plt.bar(bar_positions_middle, values_middle, width=bar_width, label='Middle Lighting', color=color_middle)
    plt.bar(bar_positions_low, values_low, width=bar_width, label='Low Lighting', color=color_dark)

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Recall For Hand Gestures Under Different Lighting Conditions')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.xticks(bar_positions_middle,labels)
    plt.legend()
    plt.show()

def threshold_variation_Vshape():

    thresholds = [18, 25, 32] #12, 
    recalls = [90.1, 100, 88.1] #100, 

    # Scatter Plot erstellen
    plt.figure(figsize=(8, 6))
    plt.scatter(thresholds, recalls, color='blue', marker='o')

    # Achsentitel und Diagrammüberschrift hinzufügen
    plt.xlabel('Threshold')
    plt.ylabel('Recall (%)')
    plt.title('V-Shape')

    # Gitter hinzufügen
    plt.grid(True)

    # Plot anzeigen
    plt.show()
    
  
def threshold_variation_Pinch():

    # Daten für die PINCH-Geste und ihre THRESHOLD-Variationen
    thresholds_pinch = [18, 12, 9, 6]
    recalls_pinch = [100, 95.0, 98.0, 3.9]

    # Scatter Plot erstellen
    plt.figure(figsize=(8, 6))
    plt.scatter(thresholds_pinch, recalls_pinch, color='blue',marker='o')

    # Achsentitel und Diagrammüberschrift hinzufügen
    plt.xlabel('THRESHOLD')
    plt.ylabel('Recall (%)')
    plt.title('Pinch')

    # Gitter hinzufügen
    plt.grid(True)

    # Plot anzeigen
    plt.show()

def threshold_variation_Fist():

    # Daten für die PINCH-Geste und ihre THRESHOLD-Variationen
    thresholds_pinch = [70,50,40,30]
    recalls_pinch = [100, 100, 99.0,5.0]

    # FIST: 70, recall = 100%
    # FIST: 50, recall = 100%
    # FIST: 40, recall = 99,0%
    # FIST: 30, recall = 5,0%

    # Scatter Plot erstellen
    plt.figure(figsize=(8, 6))
    plt.scatter(thresholds_pinch, recalls_pinch, color='blue',marker='o')

    # Achsentitel und Diagrammüberschrift hinzufügen
    plt.xlabel('THRESHOLD')
    plt.ylabel('Recall (%)')
    plt.title('Fist')

    # Gitter hinzufügen
    plt.grid(True)

    # Plot anzeigen
    plt.show()




# Rufe die Funktion auf, um das kombinierte Diagramm zu erstellen
# _combined_lighting_conditions_recall_plot()



# _bright_lighting_conditions_recall_plot()
# _middle_lighting_conditions_recall_plot()
# _low_lighting_conditions_recall_plot()

# Rufe die Funktion auf, um das Diagramm zu erstellen
# frame_matching_plot()

# _combined_lighting_conditions_recall_plot_home()
    
# threshold_variation_Vshape()
# threshold_variation_Pinch()
threshold_variation_Fist()



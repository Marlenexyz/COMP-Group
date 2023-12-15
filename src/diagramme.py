import matplotlib.pyplot as plt


def _bright_lighting_conditions_plot():
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

def _middle_lighting_conditions_plot():
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

def _low_lighting_conditions_plot():
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

_bright_lighting_conditions_plot()
_middle_lighting_conditions_plot()
_low_lighting_conditions_plot()
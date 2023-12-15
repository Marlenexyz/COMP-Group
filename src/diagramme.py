import matplotlib.pyplot as plt


def _bright_lighting_conditions_plot():
    'Bright Lighting Conditions'
    labels = ['Hand', 'Pinch', 'V-Shape', 'Fist']
    values = [0.66, 0.27, 0.77, 0.85]

    # Erstelle ein Balkendiagramm
    plt.bar(labels, values)#, color=['blue', 'orange', 'green', 'red'])

    # Füge Titel und Achsenbeschriftungen hinzu
    plt.title('Recall for hand gestures')
    plt.xlabel('Hand Gesture')
    plt.ylabel('Recall')

    # Zeige das Diagramm an
    plt.show()

_bright_lighting_conditions_plot()
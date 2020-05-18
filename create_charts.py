import config
import json
import matplotlib.pyplot as plt
import os


DATA_DIR = os.path.expanduser("~/projects/flask_my_page/static/scraping-data/daily_sale_development_investments/")
os.makedirs(DATA_DIR, exist_ok=True)

def bar_chart(identifier, data):

    dates = data.keys()
    hits = data.values()

    plt.grid(True)
    plt.bar(dates, hits)

    plt.title(label=identifier)
    plt.xticks(rotation=80)

    plt.tight_layout()

    plot_image_filename = "%s.png" % identifier.replace(".", "-")
    plot_image_path = os.path.join(DATA_DIR, plot_image_filename)
    plt.savefig(plot_image_path)
    plt.close()
    print("PLOT", plot_image_path)



os.makedirs(config.PLOTS_DIRECTORY, exist_ok=True)

with open(config.DATA_FILE, "r") as json_file:
    data = json.load(json_file)

for identifier in sorted(data):
    bar_chart(identifier, data[identifier])

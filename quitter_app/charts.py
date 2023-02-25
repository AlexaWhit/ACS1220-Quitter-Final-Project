from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

def money_saved_chart(quit_date, avg_cigs):
    days_quit = (datetime.utcnow().date() - quit_date).days
    money_saved = round((avg_cigs / 20) * 7.50 * days_quit, 2)

    # Create a bar chart of the money saved
    plt.bar(["Money Saved"], [money_saved])
    plt.title("Total Money Saved")
    plt.ylabel("Dollars")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the chart to a BytesIO buffer and return the raw PNG data
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer.getvalue()

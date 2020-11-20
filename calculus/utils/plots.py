import matplotlib.pyplot as plt
import numpy as np
import io
# from matplotlib import rcParams
from gi.repository import GdkPixbuf, Gio

class Plots:

    def n_subplots(title, ranges, functions, labels, colors):
        x = np.linspace(ranges[0], ranges[1], 1000)
        fig, axs = plt.subplots(len(functions))
        fig.suptitle(title)

        for i, f in enumerate(functions):

            try:
                axs[i].plot(x, f(x), color=colors[i], label=labels[i])
            except TypeError:
                # If the lambda function 'f' presents something in the inner
                # logic that doesn't directly support numpy arrays,
                # calculate 'f' for every value before turning into numpy array.
                f_values = np.array([f(i) for i in x])
                axs[i].plot(x, f_values, color=colors[i], label=labels[i])


        fig.legend()
        fig.show()

    def load_pixbuff_text(txt, color):
        # dependency on LaTeX wasn't successfully configured
        # rcParams['text.usetex'] = True

        # old fixed size
        #plt.figure(figsize=(4,0.75))

        # Take figure's dpi and calculate size in inches through text size in pixels

        fig = plt.figure()
        dpi = fig.dpi
        r = fig.canvas.get_renderer()
        plt.axis('off')
        textimage = plt.text(
            0.5,
            0.5,
            txt,
            fontsize=20,
            horizontalalignment='center',
            verticalalignment='center',
            color=color)

        bb = textimage.get_window_extent(renderer=r)
        fig.set_size_inches((bb.width + 20) / dpi, bb.height / dpi)

        buff = io.BytesIO()

        plt.savefig(buff, format='png', transparent=True)
        inputStream = Gio.MemoryInputStream.new_from_data(buff.getvalue())

        plt.close()

        return GdkPixbuf.Pixbuf.new_from_stream(inputStream)

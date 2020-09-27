import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib import rcParams
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
                f_values = np.array([f(i) for i in x])
                axs[i].plot(x, f_values, color=colors[i], label=labels[i])


        fig.legend()
        fig.show()

    def load_pixbuff_text(txt, color):
        #rcParams['text.usetex'] = True

        plt.figure(figsize=(4,0.75))
        plt.axis('off')
        plt.text(0.5, 0.5, txt, fontsize=20, horizontalalignment='center', verticalalignment='center', color=color)

        buff = io.BytesIO()

        plt.savefig(buff, format='png', transparent=True)
        #sympy.preview(result, output='png', viewer='BytesIO', outputbuffer=buff)

        inputStream = Gio.MemoryInputStream.new_from_data(buff.getvalue())

        plt.close()

        return GdkPixbuf.Pixbuf.new_from_stream(inputStream)
